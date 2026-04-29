"""MCP server for Yandex Market Partner API."""

import json
import logging
import os
import sys
import tempfile

from mcp.server.fastmcp import FastMCP

from .ym_api import YandexMarketAPI

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", stream=sys.stderr)
log = logging.getLogger(__name__)

mcp = FastMCP("yandex-market-seller")


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


# ── Campaigns & Settings ────────────────────────────────────────────


@mcp.tool()
def ym_campaigns() -> str:
    """List all Yandex Market campaigns (shops)."""
    return _to_json(_get_api().get_campaigns())


@mcp.tool()
def ym_campaign(campaign_id: int = 0) -> str:
    """Get campaign info. Args: campaign_id (default env)."""
    return _to_json(_get_api().get_campaign(campaign_id or _get_campaign_id()))


@mcp.tool()
def ym_campaign_settings(campaign_id: int = 0) -> str:
    """Get campaign settings."""
    return _to_json(_get_api().get_campaign_settings(campaign_id or _get_campaign_id()))


@mcp.tool()
def ym_campaign_settings_update(settings_json: str, campaign_id: int = 0) -> str:
    """Update campaign settings. Args: settings_json — JSON object."""
    return _to_json(_get_api().update_campaign_settings(
        campaign_id or _get_campaign_id(), _parse_json(settings_json, "settings_json")))


@mcp.tool()
def ym_business_settings(business_id: int = 0) -> str:
    """Get business settings."""
    return _to_json(_get_api().get_business_settings(business_id or _get_business_id()))


@mcp.tool()
def ym_business_settings_update(settings_json: str, business_id: int = 0) -> str:
    """Update business settings. Args: settings_json — JSON object."""
    return _to_json(_get_api().update_business_settings(
        business_id or _get_business_id(), _parse_json(settings_json, "settings_json")))


# ── Orders v2 ───────────────────────────────────────────────────────


@mcp.tool()
def ym_orders(status: str = "", page: int = 1, page_size: int = 50, campaign_id: int = 0) -> str:
    """List orders. Statuses: PROCESSING, DELIVERY, PICKUP, DELIVERED, CANCELLED, UNPAID."""
    return _to_json(_get_api().get_orders(campaign_id or _get_campaign_id(), status=status, page=page, page_size=page_size))


@mcp.tool()
def ym_order(order_id: int, campaign_id: int = 0) -> str:
    """Get order details."""
    return _to_json(_get_api().get_order(campaign_id or _get_campaign_id(), order_id))


@mcp.tool()
def ym_order_status(order_id: int, status: str, substatus: str = "", campaign_id: int = 0) -> str:
    """Update order status (e.g. PROCESSING→DELIVERY)."""
    return _to_json(_get_api().update_order_status(campaign_id or _get_campaign_id(), order_id, status, substatus))


@mcp.tool()
def ym_order_status_batch(updates_json: str, campaign_id: int = 0) -> str:
    """Batch update order statuses. Args: updates_json — JSON array of {orderId, status, substatus}."""
    return _to_json(_get_api().batch_update_order_statuses(campaign_id or _get_campaign_id(), _parse_json(updates_json, "updates_json")))


@mcp.tool()
def ym_order_labels(order_id: int, output_path: str, campaign_id: int = 0) -> str:
    """Download order shipping labels (PDF)."""
    return _save_bytes(_get_api().get_order_labels(campaign_id or _get_campaign_id(), order_id), output_path)


@mcp.tool()
def ym_order_labels_data(order_id: int, campaign_id: int = 0) -> str:
    """Get order label data (JSON, not PDF)."""
    return _to_json(_get_api().get_order_labels_data(campaign_id or _get_campaign_id(), order_id))


@mcp.tool()
def ym_order_box_label(order_id: int, shipment_id: int, box_id: int, output_path: str, campaign_id: int = 0) -> str:
    """Download box label (PDF)."""
    return _save_bytes(_get_api().get_order_box_label(campaign_id or _get_campaign_id(), order_id, shipment_id, box_id), output_path)


@mcp.tool()
def ym_order_items(order_id: int, campaign_id: int = 0) -> str:
    """Get order line items."""
    return _to_json(_get_api().get_order_items(campaign_id or _get_campaign_id(), order_id))


@mcp.tool()
def ym_order_items_update(order_id: int, items_json: str, campaign_id: int = 0) -> str:
    """Update order items. Args: items_json — JSON array."""
    return _to_json(_get_api().update_order_items(campaign_id or _get_campaign_id(), order_id, _parse_json(items_json, "items_json")))


@mcp.tool()
def ym_order_boxes(order_id: int, campaign_id: int = 0) -> str:
    """Get order boxes."""
    return _to_json(_get_api().get_order_boxes(campaign_id or _get_campaign_id(), order_id))


@mcp.tool()
def ym_order_boxes_update(order_id: int, boxes_json: str, campaign_id: int = 0) -> str:
    """Update order boxes. Args: boxes_json — JSON array."""
    return _to_json(_get_api().update_order_boxes(campaign_id or _get_campaign_id(), order_id, _parse_json(boxes_json, "boxes_json")))


@mcp.tool()
def ym_order_shipment_boxes(order_id: int, shipment_id: int, boxes_json: str, campaign_id: int = 0) -> str:
    """Set shipment boxes. Args: boxes_json — JSON array."""
    return _to_json(_get_api().set_shipment_boxes(campaign_id or _get_campaign_id(), order_id, shipment_id, _parse_json(boxes_json, "boxes_json")))


@mcp.tool()
def ym_order_cancel_accept(order_id: int, campaign_id: int = 0) -> str:
    """Accept order cancellation."""
    return _to_json(_get_api().accept_order_cancellation(campaign_id or _get_campaign_id(), order_id))


@mcp.tool()
def ym_order_delivery_date(order_id: int, dates_json: str, campaign_id: int = 0) -> str:
    """Set delivery date. Args: dates_json — {fromDate, toDate}."""
    return _to_json(_get_api().set_order_delivery_date(campaign_id or _get_campaign_id(), order_id, _parse_json(dates_json, "dates_json")))


@mcp.tool()
def ym_order_tracking(order_id: int, campaign_id: int = 0) -> str:
    """Get order tracking info."""
    return _to_json(_get_api().get_order_tracking(campaign_id or _get_campaign_id(), order_id))


@mcp.tool()
def ym_order_tracking_update(order_id: int, tracks_json: str, campaign_id: int = 0) -> str:
    """Set tracking numbers. Args: tracks_json — JSON array of {trackCode, deliveryServiceId}."""
    return _to_json(_get_api().set_order_tracking(campaign_id or _get_campaign_id(), order_id, _parse_json(tracks_json, "tracks_json")))


@mcp.tool()
def ym_order_buyer(order_id: int, campaign_id: int = 0) -> str:
    """Get buyer info."""
    return _to_json(_get_api().get_order_buyer(campaign_id or _get_campaign_id(), order_id))


@mcp.tool()
def ym_order_business_buyer(order_id: int, campaign_id: int = 0) -> str:
    """Get business buyer (legal entity) info."""
    return _to_json(_get_api().get_order_business_buyer(campaign_id or _get_campaign_id(), order_id))


@mcp.tool()
def ym_order_verify_eac(order_id: int, code: str, campaign_id: int = 0) -> str:
    """Verify EAC code."""
    return _to_json(_get_api().verify_order_eac(campaign_id or _get_campaign_id(), order_id, code))


@mcp.tool()
def ym_order_storage_limit(order_id: int, campaign_id: int = 0) -> str:
    """Get order storage limit."""
    return _to_json(_get_api().get_order_storage_limit(campaign_id or _get_campaign_id(), order_id))


@mcp.tool()
def ym_order_storage_limit_update(order_id: int, date: str, campaign_id: int = 0) -> str:
    """Set order storage limit. Args: date — YYYY-MM-DD."""
    return _to_json(_get_api().set_order_storage_limit(campaign_id or _get_campaign_id(), order_id, date))


@mcp.tool()
def ym_order_deliver_digital(order_id: int, items_json: str, campaign_id: int = 0) -> str:
    """Deliver digital goods. Args: items_json — JSON array."""
    return _to_json(_get_api().deliver_digital_goods(campaign_id or _get_campaign_id(), order_id, _parse_json(items_json, "items_json")))


@mcp.tool()
def ym_order_documents(order_id: int, campaign_id: int = 0) -> str:
    """Get order documents."""
    return _to_json(_get_api().get_order_documents(campaign_id or _get_campaign_id(), order_id))


@mcp.tool()
def ym_order_document_create(order_id: int, document_json: str, campaign_id: int = 0) -> str:
    """Create order document."""
    return _to_json(_get_api().create_order_document(campaign_id or _get_campaign_id(), order_id, _parse_json(document_json, "document_json")))


# ── Orders v1 ───────────────────────────────────────────────────────


@mcp.tool()
def ym_business_orders(payload_json: str, business_id: int = 0) -> str:
    """Get business-level orders (v1). Args: payload_json — filter criteria."""
    return _to_json(_get_api().get_business_orders(business_id or _get_business_id(), _parse_json(payload_json, "payload_json")))


@mcp.tool()
def ym_order_create(order_json: str, campaign_id: int = 0) -> str:
    """Create order (v1)."""
    return _to_json(_get_api().create_order_v1(campaign_id or _get_campaign_id(), _parse_json(order_json, "order_json")))


@mcp.tool()
def ym_order_update_v1(order_json: str, campaign_id: int = 0) -> str:
    """Update order (v1)."""
    return _to_json(_get_api().update_order_v1(campaign_id or _get_campaign_id(), _parse_json(order_json, "order_json")))


@mcp.tool()
def ym_order_update_options(options_json: str, campaign_id: int = 0) -> str:
    """Update order options (v1)."""
    return _to_json(_get_api().update_order_options(campaign_id or _get_campaign_id(), _parse_json(options_json, "options_json")))


# ── Returns ─────────────────────────────────────────────────────────


@mcp.tool()
def ym_returns(page: int = 1, page_size: int = 50, campaign_id: int = 0) -> str:
    """List returns."""
    return _to_json(_get_api().get_returns(campaign_id or _get_campaign_id(), page=page, page_size=page_size))


@mcp.tool()
def ym_return(order_id: int, return_id: int, campaign_id: int = 0) -> str:
    """Get return details."""
    return _to_json(_get_api().get_return(campaign_id or _get_campaign_id(), order_id, return_id))


@mcp.tool()
def ym_return_decision(order_id: int, return_id: int, campaign_id: int = 0) -> str:
    """Get return decision."""
    return _to_json(_get_api().get_return_decision(campaign_id or _get_campaign_id(), order_id, return_id))


@mcp.tool()
def ym_return_decision_set(order_id: int, return_id: int, decision_json: str, campaign_id: int = 0) -> str:
    """Set return decision."""
    return _to_json(_get_api().set_return_decision(campaign_id or _get_campaign_id(), order_id, return_id, _parse_json(decision_json, "decision_json")))


@mcp.tool()
def ym_return_decision_submit(order_id: int, return_id: int, campaign_id: int = 0) -> str:
    """Submit return decision."""
    return _to_json(_get_api().submit_return_decision(campaign_id or _get_campaign_id(), order_id, return_id))


@mcp.tool()
def ym_return_application(order_id: int, return_id: int, output_path: str, campaign_id: int = 0) -> str:
    """Download return application (PDF)."""
    return _save_bytes(_get_api().get_return_application(campaign_id or _get_campaign_id(), order_id, return_id), output_path)


@mcp.tool()
def ym_business_return_decisions(payload_json: str, business_id: int = 0) -> str:
    """Get business return decisions (v1)."""
    return _to_json(_get_api().get_business_return_decisions(business_id or _get_business_id(), _parse_json(payload_json, "payload_json")))


@mcp.tool()
def ym_return_create(return_json: str, campaign_id: int = 0) -> str:
    """Create return (v1)."""
    return _to_json(_get_api().create_return_v1(campaign_id or _get_campaign_id(), _parse_json(return_json, "return_json")))


@mcp.tool()
def ym_return_cancel(return_json: str, campaign_id: int = 0) -> str:
    """Cancel return (v1)."""
    return _to_json(_get_api().cancel_return_v1(campaign_id or _get_campaign_id(), _parse_json(return_json, "return_json")))


# ── First-Mile Shipments ────────────────────────────────────────────


@mcp.tool()
def ym_shipments(campaign_id: int = 0) -> str:
    """List first-mile shipments."""
    return _to_json(_get_api().get_shipments(campaign_id or _get_campaign_id()))


@mcp.tool()
def ym_shipments_search(payload_json: str, campaign_id: int = 0) -> str:
    """Search shipments. Args: payload_json — filter criteria."""
    return _to_json(_get_api().search_shipments(campaign_id or _get_campaign_id(), _parse_json(payload_json, "payload_json")))


@mcp.tool()
def ym_shipment(shipment_id: int, campaign_id: int = 0) -> str:
    """Get shipment details."""
    return _to_json(_get_api().get_shipment(campaign_id or _get_campaign_id(), shipment_id))


@mcp.tool()
def ym_shipment_update(shipment_id: int, payload_json: str, campaign_id: int = 0) -> str:
    """Update shipment."""
    return _to_json(_get_api().update_shipment(campaign_id or _get_campaign_id(), shipment_id, _parse_json(payload_json, "payload_json")))


@mcp.tool()
def ym_shipment_confirm(shipment_id: int, campaign_id: int = 0) -> str:
    """Confirm shipment."""
    return _to_json(_get_api().confirm_shipment(campaign_id or _get_campaign_id(), shipment_id))


@mcp.tool()
def ym_shipment_orders(shipment_id: int, campaign_id: int = 0) -> str:
    """Get orders in shipment."""
    return _to_json(_get_api().get_shipment_orders(campaign_id or _get_campaign_id(), shipment_id))


@mcp.tool()
def ym_shipment_transfer(shipment_id: int, payload_json: str, campaign_id: int = 0) -> str:
    """Transfer orders to shipment."""
    return _to_json(_get_api().transfer_shipment_orders(campaign_id or _get_campaign_id(), shipment_id, _parse_json(payload_json, "payload_json")))


@mcp.tool()
def ym_shipment_act(shipment_id: int, output_path: str, campaign_id: int = 0) -> str:
    """Download shipment act (PDF)."""
    return _save_bytes(_get_api().get_shipment_act(campaign_id or _get_campaign_id(), shipment_id), output_path)


@mcp.tool()
def ym_shipment_inbound_act(shipment_id: int, output_path: str, campaign_id: int = 0) -> str:
    """Download inbound act (PDF)."""
    return _save_bytes(_get_api().get_shipment_inbound_act(campaign_id or _get_campaign_id(), shipment_id), output_path)


@mcp.tool()
def ym_shipment_waybill(shipment_id: int, output_path: str, campaign_id: int = 0) -> str:
    """Download transportation waybill (PDF)."""
    return _save_bytes(_get_api().get_shipment_waybill(campaign_id or _get_campaign_id(), shipment_id), output_path)


@mcp.tool()
def ym_shipment_discrepancy_act(shipment_id: int, output_path: str, campaign_id: int = 0) -> str:
    """Download discrepancy act (PDF)."""
    return _save_bytes(_get_api().get_shipment_discrepancy_act(campaign_id or _get_campaign_id(), shipment_id), output_path)


@mcp.tool()
def ym_shipment_pallets(shipment_id: int, campaign_id: int = 0) -> str:
    """Get shipment pallets."""
    return _to_json(_get_api().get_shipment_pallets(campaign_id or _get_campaign_id(), shipment_id))


@mcp.tool()
def ym_shipment_pallets_update(shipment_id: int, pallets_json: str, campaign_id: int = 0) -> str:
    """Set shipment pallets."""
    return _to_json(_get_api().set_shipment_pallets(campaign_id or _get_campaign_id(), shipment_id, _parse_json(pallets_json, "pallets_json")))


@mcp.tool()
def ym_shipment_pallet_labels(shipment_id: int, output_path: str, campaign_id: int = 0) -> str:
    """Download pallet labels (PDF)."""
    return _save_bytes(_get_api().get_shipment_pallet_labels(campaign_id or _get_campaign_id(), shipment_id), output_path)


# ── Warehouses ──────────────────────────────────────────────────────


@mcp.tool()
def ym_warehouses(business_id: int = 0) -> str:
    """Get business warehouses."""
    return _to_json(_get_api().get_warehouses(business_id or _get_business_id()))


@mcp.tool()
def ym_all_warehouses() -> str:
    """Get all Yandex Market warehouses."""
    return _to_json(_get_api().get_all_warehouses())


@mcp.tool()
def ym_warehouse_status(enabled: bool, campaign_id: int = 0) -> str:
    """Enable/disable warehouse. Args: enabled — true/false."""
    return _to_json(_get_api().set_warehouse_status(campaign_id or _get_campaign_id(), enabled))


@mcp.tool()
def ym_reception_transfer_act(output_path: str, campaign_id: int = 0) -> str:
    """Download reception-transfer act (PDF)."""
    return _save_bytes(_get_api().get_reception_transfer_act(campaign_id or _get_campaign_id()), output_path)


# ── Offers (products) ──────────────────────────────────────────────


@mcp.tool()
def ym_offers(offer_ids: str = "", page_token: str = "", limit: int = 200, business_id: int = 0) -> str:
    """List products (offer mappings)."""
    ids = [s.strip() for s in offer_ids.split(",") if s.strip()] if offer_ids else None
    return _to_json(_get_api().get_offer_mappings(business_id or _get_business_id(), offer_ids=ids, page_token=page_token, limit=limit))


@mcp.tool()
def ym_offers_update(offers_json: str, business_id: int = 0) -> str:
    """Update product descriptions."""
    return _to_json(_get_api().update_offer_mappings(business_id or _get_business_id(), _parse_json(offers_json, "offers_json")))


@mcp.tool()
def ym_offers_delete(offer_ids: str, business_id: int = 0) -> str:
    """Delete products. Args: offer_ids — comma-separated."""
    return _to_json(_get_api().delete_offer_mappings(business_id or _get_business_id(), [s.strip() for s in offer_ids.split(",")]))


@mcp.tool()
def ym_offers_archive(offer_ids: str, archive: bool = True, business_id: int = 0) -> str:
    """Archive or unarchive products."""
    ids = [s.strip() for s in offer_ids.split(",")]
    bid = business_id or _get_business_id()
    if archive:
        return _to_json(_get_api().archive_offer_mappings(bid, ids))
    return _to_json(_get_api().unarchive_offer_mappings(bid, ids))


@mcp.tool()
def ym_generate_barcodes(offer_ids: str, business_id: int = 0) -> str:
    """Generate barcodes for offers."""
    return _to_json(_get_api().generate_barcodes(business_id or _get_business_id(), [s.strip() for s in offer_ids.split(",")]))


# ── Prices ──────────────────────────────────────────────────────────


@mcp.tool()
def ym_prices(offer_ids: str = "", page_token: str = "", limit: int = 200, business_id: int = 0) -> str:
    """Get product prices."""
    ids = [s.strip() for s in offer_ids.split(",") if s.strip()] if offer_ids else None
    return _to_json(_get_api().get_business_offer_prices(business_id or _get_business_id(), offer_ids=ids, page_token=page_token, limit=limit))


@mcp.tool()
def ym_prices_update(prices_json: str, business_id: int = 0) -> str:
    """Update product prices."""
    return _to_json(_get_api().update_business_offer_prices(business_id or _get_business_id(), _parse_json(prices_json, "prices_json")))


@mcp.tool()
def ym_price_quarantine(payload_json: str = "{}", business_id: int = 0) -> str:
    """Get offers in price quarantine."""
    return _to_json(_get_api().get_price_quarantine(business_id or _get_business_id(), _parse_json(payload_json, "payload_json")))


@mcp.tool()
def ym_price_quarantine_confirm(offer_ids: str, business_id: int = 0) -> str:
    """Confirm quarantine prices."""
    return _to_json(_get_api().confirm_price_quarantine(business_id or _get_business_id(), [s.strip() for s in offer_ids.split(",")]))


@mcp.tool()
def ym_campaign_price_quarantine(payload_json: str = "{}", campaign_id: int = 0) -> str:
    """Get campaign price quarantine."""
    return _to_json(_get_api().get_campaign_price_quarantine(campaign_id or _get_campaign_id(), _parse_json(payload_json, "payload_json")))


@mcp.tool()
def ym_campaign_price_quarantine_confirm(offer_ids: str, campaign_id: int = 0) -> str:
    """Confirm campaign quarantine prices."""
    return _to_json(_get_api().confirm_campaign_price_quarantine(campaign_id or _get_campaign_id(), [s.strip() for s in offer_ids.split(",")]))


# ── Stocks ──────────────────────────────────────────────────────────


@mcp.tool()
def ym_stocks(page_token: str = "", limit: int = 200, campaign_id: int = 0) -> str:
    """Get product stocks."""
    return _to_json(_get_api().get_stocks(campaign_id or _get_campaign_id(), page_token=page_token, limit=limit))


@mcp.tool()
def ym_stocks_update(stocks_json: str, campaign_id: int = 0) -> str:
    """Update product stocks."""
    return _to_json(_get_api().update_stocks(campaign_id or _get_campaign_id(), _parse_json(stocks_json, "stocks_json")))


# ── Campaign Offers ─────────────────────────────────────────────────


@mcp.tool()
def ym_campaign_offers(page_token: str = "", limit: int = 200, campaign_id: int = 0) -> str:
    """Get campaign offers with prices and stock."""
    return _to_json(_get_api().get_campaign_offers(campaign_id or _get_campaign_id(), page_token=page_token, limit=limit))


@mcp.tool()
def ym_hidden_offers(page_token: str = "", limit: int = 200, campaign_id: int = 0) -> str:
    """Get hidden offers."""
    return _to_json(_get_api().get_hidden_offers(campaign_id or _get_campaign_id(), page_token=page_token, limit=limit))


@mcp.tool()
def ym_unhide_offers(offer_ids: str, campaign_id: int = 0) -> str:
    """Unhide offers."""
    return _to_json(_get_api().unhide_offers(campaign_id or _get_campaign_id(), [s.strip() for s in offer_ids.split(",")]))


# ── Offer Cards ─────────────────────────────────────────────────────


@mcp.tool()
def ym_offer_cards(offer_ids: str = "", page_token: str = "", limit: int = 200, business_id: int = 0) -> str:
    """Get offer cards."""
    ids = [s.strip() for s in offer_ids.split(",") if s.strip()] if offer_ids else None
    return _to_json(_get_api().get_offer_cards(business_id or _get_business_id(), offer_ids=ids, page_token=page_token, limit=limit))


@mcp.tool()
def ym_offer_cards_update(cards_json: str, business_id: int = 0) -> str:
    """Update offer cards."""
    return _to_json(_get_api().update_offer_cards(business_id or _get_business_id(), _parse_json(cards_json, "cards_json")))


@mcp.tool()
def ym_offer_recommendations(payload_json: str = "{}", business_id: int = 0) -> str:
    """Get offer recommendations."""
    return _to_json(_get_api().get_offer_recommendations(business_id or _get_business_id(), _parse_json(payload_json, "payload_json")))


# ── Delivery ────────────────────────────────────────────────────────


@mcp.tool()
def ym_delivery_services() -> str:
    """List delivery services."""
    return _to_json(_get_api().get_delivery_services())


@mcp.tool()
def ym_delivery_options(payload_json: str, campaign_id: int = 0) -> str:
    """Get delivery options."""
    return _to_json(_get_api().get_delivery_options(campaign_id or _get_campaign_id(), _parse_json(payload_json, "payload_json")))


@mcp.tool()
def ym_return_delivery_options(payload_json: str, campaign_id: int = 0) -> str:
    """Get return delivery options."""
    return _to_json(_get_api().get_return_delivery_options(campaign_id or _get_campaign_id(), _parse_json(payload_json, "payload_json")))


# ── Logistics Points ───────────────────────────────────────────────


@mcp.tool()
def ym_logistics_points(payload_json: str = "{}", business_id: int = 0) -> str:
    """Get logistics/drop-off points. Args: payload_json — optional filter {warehouseIds: [...]}."""
    return _to_json(_get_api().get_logistics_points(business_id or _get_business_id(), _parse_json(payload_json, "payload_json")))


# ── Feedbacks ───────────────────────────────────────────────────────


@mcp.tool()
def ym_feedbacks(page_token: str = "", limit: int = 200, business_id: int = 0) -> str:
    """Get product feedbacks."""
    return _to_json(_get_api().get_feedbacks(business_id or _get_business_id(), page_token=page_token, limit=limit))


@mcp.tool()
def ym_feedback_skip(feedback_ids_json: str, business_id: int = 0) -> str:
    """Skip feedback reaction. Args: feedback_ids_json — JSON array of IDs."""
    return _to_json(_get_api().skip_feedback_reaction(business_id or _get_business_id(), _parse_json(feedback_ids_json, "feedback_ids_json")))


@mcp.tool()
def ym_feedback_comments(feedback_id: int, business_id: int = 0) -> str:
    """Get feedback comments."""
    return _to_json(_get_api().get_feedback_comments(business_id or _get_business_id(), feedback_id))


@mcp.tool()
def ym_feedback_comment_update(comment_json: str, business_id: int = 0) -> str:
    """Update feedback comment."""
    return _to_json(_get_api().update_feedback_comment(business_id or _get_business_id(), _parse_json(comment_json, "comment_json")))


@mcp.tool()
def ym_feedback_comment_delete(comment_id: int, business_id: int = 0) -> str:
    """Delete feedback comment."""
    return _to_json(_get_api().delete_feedback_comment(business_id or _get_business_id(), comment_id))


# ── Q&A ─────────────────────────────────────────────────────────────


@mcp.tool()
def ym_questions(payload_json: str = "{}", business_id: int = 0) -> str:
    """Get product questions."""
    return _to_json(_get_api().get_questions(business_id or _get_business_id(), _parse_json(payload_json, "payload_json")))


@mcp.tool()
def ym_question_answer(answer_json: str, business_id: int = 0) -> str:
    """Answer a question."""
    return _to_json(_get_api().answer_question(business_id or _get_business_id(), _parse_json(answer_json, "answer_json")))


@mcp.tool()
def ym_question_update(update_json: str, business_id: int = 0) -> str:
    """Update an answer."""
    return _to_json(_get_api().update_question_answer(business_id or _get_business_id(), _parse_json(update_json, "update_json")))


# ── Quality Rating ──────────────────────────────────────────────────


@mcp.tool()
def ym_quality_rating(business_id: int = 0, campaign_id: int = 0) -> str:
    """Get quality rating."""
    bid = business_id or _get_business_id()
    cid = campaign_id or _get_optional_campaign_id()
    campaign_ids = [cid] if cid else None
    return _to_json(_get_api().get_quality_ratings(bid, campaign_ids=campaign_ids))


@mcp.tool()
def ym_quality_details(campaign_id: int = 0) -> str:
    """Get quality rating details."""
    return _to_json(_get_api().get_quality_details(campaign_id or _get_campaign_id()))


# ── Promos ──────────────────────────────────────────────────────────


@mcp.tool()
def ym_promos(business_id: int = 0) -> str:
    """Get active promotions."""
    return _to_json(_get_api().get_promos(business_id or _get_business_id()))


@mcp.tool()
def ym_promo_offers(promo_id: str, payload_json: str = "{}", business_id: int = 0) -> str:
    """Get offers in a promotion."""
    return _to_json(_get_api().get_promo_offers(business_id or _get_business_id(), promo_id, _parse_json(payload_json, "payload_json")))


@mcp.tool()
def ym_promo_offers_update(payload_json: str, business_id: int = 0) -> str:
    """Update promo offers."""
    return _to_json(_get_api().update_promo_offers(business_id or _get_business_id(), _parse_json(payload_json, "payload_json")))


@mcp.tool()
def ym_promo_offers_delete(payload_json: str, business_id: int = 0) -> str:
    """Delete promo offers."""
    return _to_json(_get_api().delete_promo_offers(business_id or _get_business_id(), _parse_json(payload_json, "payload_json")))


# ── Bids ────────────────────────────────────────────────────────────


@mcp.tool()
def ym_bids(offer_ids: str = "", page_token: str = "", limit: int = 200, business_id: int = 0) -> str:
    """Get bids (business)."""
    ids = [s.strip() for s in offer_ids.split(",") if s.strip()] if offer_ids else None
    return _to_json(_get_api().get_bids(business_id or _get_business_id(), offer_ids=ids, page_token=page_token, limit=limit))


@mcp.tool()
def ym_bids_update(bids_json: str, business_id: int = 0) -> str:
    """Update bids (business)."""
    return _to_json(_get_api().update_bids(business_id or _get_business_id(), _parse_json(bids_json, "bids_json")))


@mcp.tool()
def ym_campaign_bids(offer_ids: str = "", page_token: str = "", limit: int = 200, campaign_id: int = 0) -> str:
    """Get bids (campaign)."""
    ids = [s.strip() for s in offer_ids.split(",") if s.strip()] if offer_ids else None
    return _to_json(_get_api().get_campaign_bids(campaign_id or _get_campaign_id(), offer_ids=ids, page_token=page_token, limit=limit))


@mcp.tool()
def ym_campaign_bids_update(bids_json: str, campaign_id: int = 0) -> str:
    """Update bids (campaign)."""
    return _to_json(_get_api().update_campaign_bids(campaign_id or _get_campaign_id(), _parse_json(bids_json, "bids_json")))


@mcp.tool()
def ym_bid_recommendations(payload_json: str = "{}", business_id: int = 0) -> str:
    """Get bid recommendations."""
    return _to_json(_get_api().get_bid_recommendations(business_id or _get_business_id(), _parse_json(payload_json, "payload_json")))


# ── Outlets ─────────────────────────────────────────────────────────


@mcp.tool()
def ym_outlets(campaign_id: int = 0) -> str:
    """List outlets (pickup points)."""
    return _to_json(_get_api().get_outlets(campaign_id or _get_campaign_id()))


@mcp.tool()
def ym_outlet(outlet_id: int, campaign_id: int = 0) -> str:
    """Get outlet details."""
    return _to_json(_get_api().get_outlet(campaign_id or _get_campaign_id(), outlet_id))


@mcp.tool()
def ym_outlet_create(outlet_json: str, campaign_id: int = 0) -> str:
    """Create outlet."""
    return _to_json(_get_api().create_outlet(campaign_id or _get_campaign_id(), _parse_json(outlet_json, "outlet_json")))


@mcp.tool()
def ym_outlet_update(outlet_id: int, outlet_json: str, campaign_id: int = 0) -> str:
    """Update outlet."""
    return _to_json(_get_api().update_outlet(campaign_id or _get_campaign_id(), outlet_id, _parse_json(outlet_json, "outlet_json")))


@mcp.tool()
def ym_outlet_delete(outlet_id: int, campaign_id: int = 0) -> str:
    """Delete outlet."""
    return _to_json(_get_api().delete_outlet(campaign_id or _get_campaign_id(), outlet_id))


@mcp.tool()
def ym_outlet_licenses(campaign_id: int = 0) -> str:
    """Get outlet licenses."""
    return _to_json(_get_api().get_outlet_licenses(campaign_id or _get_campaign_id()))


# ── Regions ─────────────────────────────────────────────────────────


@mcp.tool()
def ym_regions(name: str = "", page: int = 1) -> str:
    """Search regions."""
    return _to_json(_get_api().get_regions(name=name, page=page))


@mcp.tool()
def ym_region(region_id: int) -> str:
    """Get region by ID."""
    return _to_json(_get_api().get_region(region_id))


@mcp.tool()
def ym_region_children(region_id: int, page: int = 1) -> str:
    """Get child regions."""
    return _to_json(_get_api().get_region_children(region_id, page=page))


@mcp.tool()
def ym_countries() -> str:
    """Get countries list."""
    return _to_json(_get_api().get_countries())


# ── Categories ──────────────────────────────────────────────────────


@mcp.tool()
def ym_categories() -> str:
    """Get category tree."""
    return _to_json(_get_api().get_categories_tree())


@mcp.tool()
def ym_category_params(category_id: int) -> str:
    """Get category parameters."""
    return _to_json(_get_api().get_category_parameters(category_id))


@mcp.tool()
def ym_max_sale_quantum(payload_json: str) -> str:
    """Get max sale quantum for categories."""
    return _to_json(_get_api().get_max_sale_quantum(_parse_json(payload_json, "payload_json")))


# ── Tariffs ─────────────────────────────────────────────────────────


@mcp.tool()
def ym_tariffs(offers_json: str, campaign_id: int = 0) -> str:
    """Calculate marketplace tariffs."""
    cid = campaign_id or _get_optional_campaign_id()
    return _to_json(_get_api().calculate_tariffs(_parse_json(offers_json, "offers_json"), campaign_id=cid))


# ── Chats ───────────────────────────────────────────────────────────


@mcp.tool()
def ym_chats(page_token: str = "", limit: int = 50, business_id: int = 0) -> str:
    """List chats."""
    return _to_json(_get_api().get_chats(business_id or _get_business_id(), page_token=page_token, limit=limit))


@mcp.tool()
def ym_chat_history(chat_id: int, page_token: str = "", limit: int = 50, business_id: int = 0) -> str:
    """Get chat history."""
    return _to_json(_get_api().get_chat_history(business_id or _get_business_id(), chat_id, page_token=page_token, limit=limit))


@mcp.tool()
def ym_chat_send(chat_id: int, message: str, business_id: int = 0) -> str:
    """Send chat message."""
    return _to_json(_get_api().send_chat_message(business_id or _get_business_id(), chat_id, message))


@mcp.tool()
def ym_chat_new(payload_json: str, business_id: int = 0) -> str:
    """Create new chat."""
    return _to_json(_get_api().create_chat(business_id or _get_business_id(), _parse_json(payload_json, "payload_json")))


@mcp.tool()
def ym_chat_file_send(chat_id: int, file_path: str, business_id: int = 0) -> str:
    """Send file in chat."""
    safe = _safe_path(file_path)
    return _to_json(_get_api().send_chat_file(business_id or _get_business_id(), chat_id, safe))


# ── Reports ─────────────────────────────────────────────────────────


@mcp.tool()
def ym_report_status(report_id: str) -> str:
    """Check report generation status."""
    return _to_json(_get_api().get_report_status(report_id))


@mcp.tool()
def ym_report_generate(report_type: str, payload_json: str = "{}") -> str:
    """Generate a report. report_type: united-netting, united-marketplace-services, united-orders, united-returns, goods-realization, stocks-on-warehouses, goods-movement, shows-sales, competitors-position, goods-prices, goods-turnover, boost-consolidated, documents/shipment-list, shelf-statistics, documents/labels, goods-feedback, shows-boost, banners-statistics, closure-documents, jewelry-fiscal, sales-geography, key-indicators, closure-documents/detalization."""
    return _to_json(_get_api().generate_report(report_type, _parse_json(payload_json, "payload_json")))


@mcp.tool()
def ym_report_barcodes(payload_json: str) -> str:
    """Generate barcodes report (v1)."""
    return _to_json(_get_api().generate_barcodes_report(_parse_json(payload_json, "payload_json")))


# ── Stats ───────────────────────────────────────────────────────────


@mcp.tool()
def ym_order_stats(date_from: str = "", date_to: str = "", campaign_id: int = 0) -> str:
    """Get order statistics."""
    return _to_json(_get_api().get_order_stats(campaign_id or _get_campaign_id(), date_from=date_from, date_to=date_to))


@mcp.tool()
def ym_sku_stats(campaign_id: int = 0) -> str:
    """Get SKU performance stats."""
    return _to_json(_get_api().get_sku_stats(campaign_id or _get_campaign_id()))


# ── Supply Requests ─────────────────────────────────────────────────


@mcp.tool()
def ym_supply_requests(campaign_id: int = 0) -> str:
    """List supply requests."""
    return _to_json(_get_api().get_supply_requests(campaign_id or _get_campaign_id()))


@mcp.tool()
def ym_supply_request_items(campaign_id: int = 0) -> str:
    """Get supply request items."""
    return _to_json(_get_api().get_supply_request_items(campaign_id or _get_campaign_id()))


@mcp.tool()
def ym_supply_request_documents(output_path: str, campaign_id: int = 0) -> str:
    """Download supply request documents (PDF)."""
    return _save_bytes(_get_api().get_supply_request_documents(campaign_id or _get_campaign_id()), output_path)


# ── Operations ──────────────────────────────────────────────────────


@mcp.tool()
def ym_operations(business_id: int = 0) -> str:
    """Get async operations."""
    return _to_json(_get_api().get_operations(business_id or _get_business_id()))
