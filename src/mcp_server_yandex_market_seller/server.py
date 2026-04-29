"""MCP server for Yandex Market Partner API."""

import json
import logging
import os
import sys
import tempfile

from mcp.server.fastmcp import FastMCP

from .actions import ACTIONS
from .ym_api import YandexMarketAPI

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", stream=sys.stderr)
log = logging.getLogger(__name__)

mcp = FastMCP(
    "yandex-market-seller",
    instructions=(
        "Yandex Market Partner API server. Two ID levels: "
        "campaign_id = shop (orders, stocks, campaign prices, shipments), "
        "business_id = business (offers, cards, business prices, bids, reviews, chats). "
        "Both can be set via env (YM_CAMPAIGN_ID, YM_BUSINESS_ID) or passed per tool call. "
        "Order statuses: UNPAID → PROCESSING → DELIVERY → PICKUP → DELIVERED | CANCELLED. "
        "Use ym_search to discover available actions and their parameter schemas. "
        "Use ym_execute / ym_execute_file to run actions by ID."
    ),
)


_api_instance: YandexMarketAPI | None = None


def _get_api() -> YandexMarketAPI:
    global _api_instance
    if _api_instance is None:
        token = os.getenv("YM_TOKEN")
        if not token:
            raise RuntimeError("YM_TOKEN environment variable is required")
        auth_type = os.getenv("YM_AUTH_TYPE", "api-key")
        _api_instance = YandexMarketAPI(token, auth_type)
    return _api_instance


def _get_campaign_id() -> int:
    val = os.getenv("YM_CAMPAIGN_ID", "")
    if not val:
        raise RuntimeError("YM_CAMPAIGN_ID environment variable is required")
    return int(val)


def _get_optional_campaign_id() -> int | None:
    val = os.getenv("YM_CAMPAIGN_ID", "")
    return int(val) if val else None


def _get_business_id() -> int:
    val = os.getenv("YM_BUSINESS_ID", "")
    if not val:
        raise RuntimeError("YM_BUSINESS_ID environment variable is required")
    return int(val)


def _to_json(data) -> str:
    return json.dumps(data, ensure_ascii=False)


def _parse_json(s: str, label: str = "input"):
    """Парсить JSON-строку с понятным сообщением об ошибке."""
    try:
        return json.loads(s)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {label}: {e}") from e


def _safe_path(path: str) -> str:
    """Resolve and validate output path — only home or system temp allowed."""
    resolved = os.path.realpath(path)
    home = os.path.realpath(os.path.expanduser("~"))

    tmp_dirs = {os.path.realpath(tempfile.gettempdir())}
    if os.path.isdir("/tmp"):
        tmp_dirs.add(os.path.realpath("/tmp"))

    is_under_home = resolved.startswith(home + os.sep)
    is_under_tmp = any(resolved.startswith(d + os.sep) for d in tmp_dirs)

    if not (is_under_home or is_under_tmp):
        raise ValueError(f"Output path must be under home or temp directory: {path}")

    if is_under_home and os.sep + "." in resolved[len(home):]:
        raise ValueError(f"Writing to hidden files/directories is not allowed: {path}")

    return resolved


def _save_bytes(data: bytes, path: str) -> str:
    safe = _safe_path(path)
    with open(safe, "wb") as f:
        f.write(data)
    return _to_json({"path": safe, "size": len(data)})


# ── Action dispatch ────────────────────────────────────────────────


def _resolve_id(id_type: str, raw: dict) -> int | None:
    """Extract campaign_id/business_id from raw params, fallback to env."""
    if id_type == "campaign":
        return raw.pop("campaign_id", 0) or _get_campaign_id()
    elif id_type == "business":
        return raw.pop("business_id", 0) or _get_business_id()
    return None


def execute_action(action_id: str, raw_params: dict) -> str:
    """Validate params and execute a non-file action. Returns JSON string."""
    act = ACTIONS.get(action_id)
    if not act:
        raise ValueError(f"Unknown action: {action_id}. Use ym_search to find actions.")
    if act.is_file:
        raise ValueError(f"Action '{action_id}' downloads a file. Use ym_execute_file instead.")

    id_val = _resolve_id(act.id_type, raw_params)

    if act.params_model:
        validated = act.params_model.model_validate(raw_params)
        params = validated.model_dump()
    else:
        params = raw_params

    result = act.call_fn(_get_api(), id_val, params)
    return _to_json(result)


def execute_file_action(action_id: str, raw_params: dict, output_path: str) -> str:
    """Validate params and execute a file-download action. Returns JSON string."""
    act = ACTIONS.get(action_id)
    if not act:
        raise ValueError(f"Unknown action: {action_id}. Use ym_search to find actions.")
    if not act.is_file:
        raise ValueError(f"Action '{action_id}' does not download a file. Use ym_execute instead.")

    id_val = _resolve_id(act.id_type, raw_params)

    if act.params_model:
        validated = act.params_model.model_validate(raw_params)
        params = validated.model_dump()
    else:
        params = raw_params

    data = act.call_fn(_get_api(), id_val, params)
    return _save_bytes(data, output_path)


def _search_actions(query: str, domain: str = "", max_results: int = 10) -> list[dict]:
    """Search actions by query with optional domain filter."""
    query_lower = query.lower()
    tokens = query_lower.split()

    scored: list[tuple[int, dict]] = []
    for action in ACTIONS.values():
        if domain and action.domain != domain:
            continue

        score = 0

        if query_lower == action.id:
            score = 1000

        for token in tokens:
            if token in action.id:
                score += 10
            if token in action.description.lower():
                score += 5
            for kw in action.keywords:
                if token in kw:
                    score += 8
            if token == action.domain:
                score += 3

        if score > 0:
            entry: dict = {
                "id": action.id,
                "domain": action.domain,
                "description": action.description,
                "id_type": action.id_type,
                "is_file": action.is_file,
                "is_destructive": action.is_destructive,
            }
            if action.params_model:
                entry["params_schema"] = action.params_model.model_json_schema()
            scored.append((score, entry))

    scored.sort(key=lambda x: -x[0])
    return [entry for _, entry in scored[:max_results]]


# ── Meta-tools ─────────────────────────────────────────────────────


@mcp.tool(annotations={"readOnlyHint": True})
def ym_search(query: str, domain: str = "") -> str:
    """Find available actions by intent. Optional domain filter:
    orders, offers, prices, stocks, shipments, returns, feedbacks,
    chats, reports, bids, outlets, campaigns, geo, categories,
    warehouses, promos, quality, tariffs, supply, operations, delivery, logistics.
    Returns action ID, description, and JSON Schema of parameters."""
    return _to_json(_search_actions(query, domain))


@mcp.tool(annotations={"readOnlyHint": False})
def ym_execute(action: str, params_json: str = "{}") -> str:
    """Execute action by ID. params_json validated against action schema.
    Use ym_search to discover actions and their schemas first."""
    raw = _parse_json(params_json, "params_json")
    return execute_action(action, raw)


@mcp.tool(annotations={"readOnlyHint": False})
def ym_execute_file(action: str, output_path: str, params_json: str = "{}") -> str:
    """Execute action that downloads a file (PDF/binary).
    output_path must be under ~/... or /tmp/..."""
    raw = _parse_json(params_json, "params_json")
    return execute_file_action(action, raw, output_path)


# ── Promoted tools ─────────────────────────────────────────────────


@mcp.tool(annotations={"readOnlyHint": True})
def ym_campaigns() -> str:
    """List all campaigns (shops) in the account. Returns array of {id, domain, placementType}. Use ym_campaign for details of a single campaign."""
    return execute_action("campaigns", {})


@mcp.tool(annotations={"readOnlyHint": True})
def ym_orders(status: str = "", page: int = 1, page_size: int = 50, campaign_id: int = 0) -> str:
    """List orders with optional status filter. Statuses: UNPAID, PROCESSING, DELIVERY, PICKUP, DELIVERED, CANCELLED. Returns paginated list. Use ym_order for single order details."""
    return execute_action("orders", {"status": status, "page": page, "page_size": page_size, "campaign_id": campaign_id})


@mcp.tool(annotations={"readOnlyHint": True})
def ym_order(order_id: int, campaign_id: int = 0) -> str:
    """Get full order details: items, delivery, buyer info, status history. Use ym_orders to search/filter multiple orders."""
    return execute_action("order", {"order_id": order_id, "campaign_id": campaign_id})


@mcp.tool(annotations={"readOnlyHint": False})
def ym_order_status(order_id: int, status: str, substatus: str = "", campaign_id: int = 0) -> str:
    """Update order status. Typical flow: PROCESSING → DELIVERY → DELIVERED. Args: status, substatus (optional). Use ym_execute with action order_status_batch for multiple orders."""
    return execute_action("order_status", {"order_id": order_id, "status": status, "substatus": substatus, "campaign_id": campaign_id})


@mcp.tool(annotations={"readOnlyHint": True})
def ym_offers(offer_ids: str = "", page_token: str = "", limit: int = 200, business_id: int = 0) -> str:
    """List products (offer mappings) at business level. Returns SKU, name, category, mapping status. Paginated. Use ym_execute with action campaign_offers for campaign-level offers."""
    ids = [s.strip() for s in offer_ids.split(",") if s.strip()] if offer_ids else None
    return execute_action("offers", {"offer_ids": ids, "page_token": page_token, "limit": limit, "business_id": business_id})


@mcp.tool(annotations={"readOnlyHint": True})
def ym_stocks(page_token: str = "", limit: int = 200, campaign_id: int = 0) -> str:
    """Get product stocks for a campaign. Returns warehouse stocks per SKU. Use ym_execute with action stocks_update to change stock quantities."""
    return execute_action("stocks", {"page_token": page_token, "limit": limit, "campaign_id": campaign_id})


@mcp.tool(annotations={"readOnlyHint": False})
def ym_stocks_update(stocks_json: str, campaign_id: int = 0) -> str:
    """Update product stocks. Args: stocks_json — JSON array of {sku, warehouseId, items: [{count, type, updatedAt}]}."""
    raw = _parse_json(stocks_json, "stocks_json")
    return execute_action("stocks_update", {"skus": raw, "campaign_id": campaign_id})


@mcp.tool(annotations={"readOnlyHint": True})
def ym_prices(offer_ids: str = "", page_token: str = "", limit: int = 200, business_id: int = 0) -> str:
    """Get product prices at business level. Returns current prices, currency. Use ym_execute with action campaign_offers for campaign-level prices."""
    ids = [s.strip() for s in offer_ids.split(",") if s.strip()] if offer_ids else None
    return execute_action("prices", {"offer_ids": ids, "page_token": page_token, "limit": limit, "business_id": business_id})


@mcp.tool(annotations={"readOnlyHint": False})
def ym_prices_update(prices_json: str, business_id: int = 0) -> str:
    """Update product prices. Args: prices_json — JSON array of {offerId, price {value, currencyId}}. Business-level operation."""
    raw = _parse_json(prices_json, "prices_json")
    return execute_action("prices_update", {"offers": raw, "business_id": business_id})


@mcp.tool(annotations={"readOnlyHint": True})
def ym_returns(page: int = 1, page_size: int = 50, campaign_id: int = 0) -> str:
    """List returns for a campaign. Paginated. Use ym_execute with action return for single return details."""
    return execute_action("returns", {"page": page, "page_size": page_size, "campaign_id": campaign_id})


@mcp.tool(annotations={"readOnlyHint": True})
def ym_shipments(campaign_id: int = 0) -> str:
    """List first-mile shipments. Use ym_execute with action shipments_search for advanced filtering."""
    return execute_action("shipments", {"campaign_id": campaign_id})


@mcp.tool(annotations={"readOnlyHint": True})
def ym_feedbacks(page_token: str = "", limit: int = 200, business_id: int = 0) -> str:
    """Get product reviews/feedbacks. Paginated. Use ym_execute with action feedback_comments for comments on a review."""
    return execute_action("feedbacks", {"page_token": page_token, "limit": limit, "business_id": business_id})


@mcp.tool(annotations={"readOnlyHint": True})
def ym_chats(page_token: str = "", limit: int = 50, business_id: int = 0) -> str:
    """List buyer chats. Use ym_execute with action chat_history for messages, chat_send to reply."""
    return execute_action("chats", {"page_token": page_token, "limit": limit, "business_id": business_id})


@mcp.tool(annotations={"readOnlyHint": True})
def ym_bids(offer_ids: str = "", page_token: str = "", limit: int = 200, business_id: int = 0) -> str:
    """Get current bids at business level. Use ym_execute with action bid_recommendations for suggested values, bids_update to change."""
    ids = [s.strip() for s in offer_ids.split(",") if s.strip()] if offer_ids else None
    return execute_action("bids", {"offer_ids": ids, "page_token": page_token, "limit": limit, "business_id": business_id})


@mcp.tool(annotations={"readOnlyHint": False})
def ym_report_generate(report_type: str, payload_json: str = "{}") -> str:
    """Start async report generation. Returns reportId for polling with ym_execute action report_status. Types: united-netting, united-marketplace-services, united-orders, united-returns, goods-realization, stocks-on-warehouses, goods-movement, shows-sales."""
    payload = _parse_json(payload_json, "payload_json")
    return execute_action("report_generate", {"report_type": report_type, "payload": payload})
