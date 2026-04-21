"""MCP server for Yandex Market Partner API."""

import json
import logging
import os
import sys

from mcp.server.fastmcp import FastMCP

from .ym_api import YandexMarketAPI

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", stream=sys.stderr)
log = logging.getLogger(__name__)

mcp = FastMCP("yandex-market-seller")


def _get_api() -> YandexMarketAPI:
    token = os.getenv("YM_TOKEN")
    if not token:
        raise RuntimeError("YM_TOKEN environment variable is required")
    auth_type = os.getenv("YM_AUTH_TYPE", "api-key")
    return YandexMarketAPI(token, auth_type)


def _get_campaign_id() -> int:
    val = os.getenv("YM_CAMPAIGN_ID", "")
    if not val:
        raise RuntimeError("YM_CAMPAIGN_ID environment variable is required")
    return int(val)


def _get_business_id() -> int:
    val = os.getenv("YM_BUSINESS_ID", "")
    if not val:
        raise RuntimeError("YM_BUSINESS_ID environment variable is required")
    return int(val)


# ── Campaigns ───────────────────────────────────────────────────────


@mcp.tool()
def ym_campaigns() -> str:
    """List all Yandex Market campaigns (shops) for this account.

    Returns JSON array of campaigns with id, domain, clientId, state.
    """
    api = _get_api()
    campaigns = api.get_campaigns()
    return json.dumps(campaigns, ensure_ascii=False)


@mcp.tool()
def ym_campaign(campaign_id: int = 0) -> str:
    """Get info about a specific campaign.

    Args:
        campaign_id: Campaign ID (default: from YM_CAMPAIGN_ID env)
    """
    api = _get_api()
    cid = campaign_id or _get_campaign_id()
    data = api.get_campaign(cid)
    return json.dumps(data, ensure_ascii=False)


# ── Orders ──────────────────────────────────────────────────────────


@mcp.tool()
def ym_orders(status: str = "", page: int = 1, page_size: int = 50,
              campaign_id: int = 0) -> str:
    """List orders for a campaign.

    Common statuses: PROCESSING, DELIVERY, PICKUP, DELIVERED, CANCELLED, UNPAID.

    Args:
        status: Filter by status (optional, e.g. "PROCESSING")
        page: Page number (default 1)
        page_size: Orders per page (default 50, max 50)
        campaign_id: Campaign ID (default: from YM_CAMPAIGN_ID env)
    """
    api = _get_api()
    cid = campaign_id or _get_campaign_id()
    data = api.get_orders(cid, status=status, page=page, page_size=page_size)
    return json.dumps(data, ensure_ascii=False)


@mcp.tool()
def ym_order(order_id: int, campaign_id: int = 0) -> str:
    """Get detailed info about a specific order.

    Args:
        order_id: Order ID
        campaign_id: Campaign ID (default: from YM_CAMPAIGN_ID env)
    """
    api = _get_api()
    cid = campaign_id or _get_campaign_id()
    data = api.get_order(cid, order_id)
    return json.dumps(data, ensure_ascii=False)


@mcp.tool()
def ym_order_status(order_id: int, status: str, substatus: str = "",
                    campaign_id: int = 0) -> str:
    """Update order status.

    Common status transitions:
    - PROCESSING -> DELIVERY (shipped)
    - DELIVERY -> DELIVERED
    - PROCESSING -> CANCELLED (with substatus: SHOP_FAILED, REPLACING_ORDER, etc.)

    Args:
        order_id: Order ID
        status: New status (PROCESSING, DELIVERY, PICKUP, DELIVERED, CANCELLED)
        substatus: Sub-status (optional, e.g. "SHOP_FAILED" for cancellation)
        campaign_id: Campaign ID (default: from YM_CAMPAIGN_ID env)
    """
    api = _get_api()
    cid = campaign_id or _get_campaign_id()
    data = api.update_order_status(cid, order_id, status, substatus)
    return json.dumps(data, ensure_ascii=False)


@mcp.tool()
def ym_order_labels(order_id: int, output_path: str, campaign_id: int = 0) -> str:
    """Download order shipping labels (PDF).

    Args:
        order_id: Order ID
        output_path: Absolute path to save PDF (e.g. /tmp/labels_12345.pdf)
        campaign_id: Campaign ID (default: from YM_CAMPAIGN_ID env)
    """
    api = _get_api()
    cid = campaign_id or _get_campaign_id()
    pdf = api.get_order_labels(cid, order_id)
    with open(output_path, "wb") as f:
        f.write(pdf)
    return json.dumps({"path": os.path.abspath(output_path), "order_id": order_id}, ensure_ascii=False)


# ── Offers (products) ──────────────────────────────────────────────


@mcp.tool()
def ym_offers(offer_ids: str = "", page_token: str = "", limit: int = 200,
              business_id: int = 0) -> str:
    """List products (offer mappings) in business catalog.

    Args:
        offer_ids: Comma-separated offer IDs to filter (optional, e.g. "SKU1,SKU2")
        page_token: Pagination token for next page
        limit: Max items per page (default 200)
        business_id: Business ID (default: from YM_BUSINESS_ID env)
    """
    api = _get_api()
    bid = business_id or _get_business_id()
    ids = [s.strip() for s in offer_ids.split(",") if s.strip()] if offer_ids else None
    data = api.get_offer_mappings(bid, offer_ids=ids, page_token=page_token, limit=limit)
    return json.dumps(data, ensure_ascii=False)


@mcp.tool()
def ym_offers_update(offers_json: str, business_id: int = 0) -> str:
    """Update product descriptions and parameters.

    Args:
        offers_json: JSON array of offer mapping objects to update
        business_id: Business ID (default: from YM_BUSINESS_ID env)
    """
    api = _get_api()
    bid = business_id or _get_business_id()
    offers = json.loads(offers_json)
    data = api.update_offer_mappings(bid, offers)
    return json.dumps(data, ensure_ascii=False)


@mcp.tool()
def ym_offers_delete(offer_ids: str, business_id: int = 0) -> str:
    """Delete products from catalog.

    Args:
        offer_ids: Comma-separated offer IDs to delete (e.g. "SKU1,SKU2")
        business_id: Business ID (default: from YM_BUSINESS_ID env)
    """
    api = _get_api()
    bid = business_id or _get_business_id()
    ids = [s.strip() for s in offer_ids.split(",")]
    data = api.delete_offer_mappings(bid, ids)
    return json.dumps(data, ensure_ascii=False)


@mcp.tool()
def ym_offers_archive(offer_ids: str, archive: bool = True, business_id: int = 0) -> str:
    """Archive or unarchive products.

    Args:
        offer_ids: Comma-separated offer IDs (e.g. "SKU1,SKU2")
        archive: True to archive, False to unarchive (default True)
        business_id: Business ID (default: from YM_BUSINESS_ID env)
    """
    api = _get_api()
    bid = business_id or _get_business_id()
    ids = [s.strip() for s in offer_ids.split(",")]
    if archive:
        data = api.archive_offer_mappings(bid, ids)
    else:
        data = api.unarchive_offer_mappings(bid, ids)
    return json.dumps(data, ensure_ascii=False)


# ── Prices ──────────────────────────────────────────────────────────


@mcp.tool()
def ym_prices(offer_ids: str = "", page_token: str = "", limit: int = 200,
              business_id: int = 0) -> str:
    """Get product prices.

    Args:
        offer_ids: Comma-separated offer IDs to filter (optional)
        page_token: Pagination token for next page
        limit: Max items per page (default 200)
        business_id: Business ID (default: from YM_BUSINESS_ID env)
    """
    api = _get_api()
    bid = business_id or _get_business_id()
    ids = [s.strip() for s in offer_ids.split(",") if s.strip()] if offer_ids else None
    data = api.get_business_offer_prices(bid, offer_ids=ids, page_token=page_token, limit=limit)
    return json.dumps(data, ensure_ascii=False)


@mcp.tool()
def ym_prices_update(prices_json: str, business_id: int = 0) -> str:
    """Update product prices.

    Args:
        prices_json: JSON array of price updates, e.g. [{"offerId": "SKU1", "price": {"value": 1000, "currencyId": "RUR"}}]
        business_id: Business ID (default: from YM_BUSINESS_ID env)
    """
    api = _get_api()
    bid = business_id or _get_business_id()
    prices = json.loads(prices_json)
    data = api.update_business_offer_prices(bid, prices)
    return json.dumps(data, ensure_ascii=False)


# ── Stocks ──────────────────────────────────────────────────────────


@mcp.tool()
def ym_stocks(page_token: str = "", limit: int = 200, campaign_id: int = 0) -> str:
    """Get product stocks (inventory levels).

    Args:
        page_token: Pagination token for next page
        limit: Max items per page (default 200)
        campaign_id: Campaign ID (default: from YM_CAMPAIGN_ID env)
    """
    api = _get_api()
    cid = campaign_id or _get_campaign_id()
    data = api.get_stocks(cid, page_token=page_token, limit=limit)
    return json.dumps(data, ensure_ascii=False)


@mcp.tool()
def ym_stocks_update(stocks_json: str, campaign_id: int = 0) -> str:
    """Update product stocks.

    Args:
        stocks_json: JSON array, e.g. [{"offerId": "SKU1", "stocks": [{"type": "FIT", "count": 10, "warehouseId": 123}]}]
        campaign_id: Campaign ID (default: from YM_CAMPAIGN_ID env)
    """
    api = _get_api()
    cid = campaign_id or _get_campaign_id()
    stocks = json.loads(stocks_json)
    data = api.update_stocks(cid, stocks)
    return json.dumps(data, ensure_ascii=False)


# ── Campaign offers ─────────────────────────────────────────────────


@mcp.tool()
def ym_campaign_offers(page_token: str = "", limit: int = 200,
                       campaign_id: int = 0) -> str:
    """Get campaign offers with prices and stock info.

    Args:
        page_token: Pagination token for next page
        limit: Max items per page (default 200)
        campaign_id: Campaign ID (default: from YM_CAMPAIGN_ID env)
    """
    api = _get_api()
    cid = campaign_id or _get_campaign_id()
    data = api.get_campaign_offers(cid, page_token=page_token, limit=limit)
    return json.dumps(data, ensure_ascii=False)


@mcp.tool()
def ym_hidden_offers(page_token: str = "", limit: int = 200,
                     campaign_id: int = 0) -> str:
    """Get hidden (disabled) offers in campaign.

    Args:
        page_token: Pagination token for next page
        limit: Max items per page (default 200)
        campaign_id: Campaign ID (default: from YM_CAMPAIGN_ID env)
    """
    api = _get_api()
    cid = campaign_id or _get_campaign_id()
    data = api.get_hidden_offers(cid, page_token=page_token, limit=limit)
    return json.dumps(data, ensure_ascii=False)


@mcp.tool()
def ym_unhide_offers(offer_ids: str, campaign_id: int = 0) -> str:
    """Unhide (enable) offers in campaign.

    Args:
        offer_ids: Comma-separated offer IDs to unhide
        campaign_id: Campaign ID (default: from YM_CAMPAIGN_ID env)
    """
    api = _get_api()
    cid = campaign_id or _get_campaign_id()
    ids = [s.strip() for s in offer_ids.split(",")]
    data = api.unhide_offers(cid, ids)
    return json.dumps(data, ensure_ascii=False)


# ── Warehouses ──────────────────────────────────────────────────────


@mcp.tool()
def ym_warehouses(business_id: int = 0) -> str:
    """Get warehouses for business.

    Args:
        business_id: Business ID (default: from YM_BUSINESS_ID env)
    """
    api = _get_api()
    bid = business_id or _get_business_id()
    data = api.get_warehouses(bid)
    return json.dumps(data, ensure_ascii=False)


# ── Returns ─────────────────────────────────────────────────────────


@mcp.tool()
def ym_returns(page: int = 1, page_size: int = 50, campaign_id: int = 0) -> str:
    """List returns for a campaign.

    Args:
        page: Page number (default 1)
        page_size: Items per page (default 50)
        campaign_id: Campaign ID (default: from YM_CAMPAIGN_ID env)
    """
    api = _get_api()
    cid = campaign_id or _get_campaign_id()
    data = api.get_returns(cid, page=page, page_size=page_size)
    return json.dumps(data, ensure_ascii=False)


@mcp.tool()
def ym_return(order_id: int, return_id: int, campaign_id: int = 0) -> str:
    """Get detailed info about a specific return.

    Args:
        order_id: Order ID
        return_id: Return ID
        campaign_id: Campaign ID (default: from YM_CAMPAIGN_ID env)
    """
    api = _get_api()
    cid = campaign_id or _get_campaign_id()
    data = api.get_return(cid, order_id, return_id)
    return json.dumps(data, ensure_ascii=False)


# ── Feedbacks ───────────────────────────────────────────────────────


@mcp.tool()
def ym_feedbacks(page_token: str = "", limit: int = 200,
                 business_id: int = 0) -> str:
    """Get product feedbacks (reviews).

    Args:
        page_token: Pagination token for next page
        limit: Max items per page (default 200)
        business_id: Business ID (default: from YM_BUSINESS_ID env)
    """
    api = _get_api()
    bid = business_id or _get_business_id()
    data = api.get_feedbacks(bid, page_token=page_token, limit=limit)
    return json.dumps(data, ensure_ascii=False)


# ── Quality Rating ──────────────────────────────────────────────────


@mcp.tool()
def ym_quality_rating(business_id: int = 0, campaign_id: int = 0) -> str:
    """Get quality rating for campaigns.

    Args:
        business_id: Business ID (default: from YM_BUSINESS_ID env)
        campaign_id: Campaign ID to filter (optional, default: from YM_CAMPAIGN_ID env)
    """
    api = _get_api()
    bid = business_id or _get_business_id()
    cid = campaign_id or int(os.getenv("YM_CAMPAIGN_ID", "0"))
    campaign_ids = [cid] if cid else None
    data = api.get_quality_ratings(bid, campaign_ids=campaign_ids)
    return json.dumps(data, ensure_ascii=False)


# ── Promos ──────────────────────────────────────────────────────────


@mcp.tool()
def ym_promos(business_id: int = 0) -> str:
    """Get active promotions.

    Args:
        business_id: Business ID (default: from YM_BUSINESS_ID env)
    """
    api = _get_api()
    bid = business_id or _get_business_id()
    data = api.get_promos(bid)
    return json.dumps(data, ensure_ascii=False)


# ── Bids ────────────────────────────────────────────────────────────


@mcp.tool()
def ym_bids(offer_ids: str = "", page_token: str = "", limit: int = 200,
            business_id: int = 0) -> str:
    """Get bids for offers.

    Args:
        offer_ids: Comma-separated offer IDs to filter (optional)
        page_token: Pagination token for next page
        limit: Max items per page (default 200)
        business_id: Business ID (default: from YM_BUSINESS_ID env)
    """
    api = _get_api()
    bid = business_id or _get_business_id()
    ids = [s.strip() for s in offer_ids.split(",") if s.strip()] if offer_ids else None
    data = api.get_bids(bid, offer_ids=ids, page_token=page_token, limit=limit)
    return json.dumps(data, ensure_ascii=False)


@mcp.tool()
def ym_bids_update(bids_json: str, business_id: int = 0) -> str:
    """Update bids for offers.

    Args:
        bids_json: JSON array of bid updates, e.g. [{"offerId": "SKU1", "bid": 50}]
        business_id: Business ID (default: from YM_BUSINESS_ID env)
    """
    api = _get_api()
    bid = business_id or _get_business_id()
    bids = json.loads(bids_json)
    data = api.update_bids(bid, bids)
    return json.dumps(data, ensure_ascii=False)


# ── Regions ─────────────────────────────────────────────────────────


@mcp.tool()
def ym_regions(name: str = "", page: int = 1) -> str:
    """Search regions by name.

    Args:
        name: Region name to search (e.g. "Москва")
        page: Page number (default 1)
    """
    api = _get_api()
    data = api.get_regions(name=name, page=page)
    return json.dumps(data, ensure_ascii=False)


# ── Categories ──────────────────────────────────────────────────────


@mcp.tool()
def ym_categories() -> str:
    """Get Yandex Market category tree."""
    api = _get_api()
    data = api.get_categories_tree()
    return json.dumps(data, ensure_ascii=False)


@mcp.tool()
def ym_category_params(category_id: int) -> str:
    """Get parameters/attributes for a category.

    Args:
        category_id: Category ID from ym_categories
    """
    api = _get_api()
    data = api.get_category_parameters(category_id)
    return json.dumps(data, ensure_ascii=False)


# ── Tariffs ─────────────────────────────────────────────────────────


@mcp.tool()
def ym_tariffs(offers_json: str, campaign_id: int = 0) -> str:
    """Calculate marketplace service tariffs for offers.

    Args:
        offers_json: JSON array of offers, e.g. [{"offerId": "SKU1", "price": 1000, "categoryId": 123}]
        campaign_id: Campaign ID (optional)
    """
    api = _get_api()
    offers = json.loads(offers_json)
    cid = campaign_id or int(os.getenv("YM_CAMPAIGN_ID", "0")) or None
    data = api.calculate_tariffs(offers, campaign_id=cid)
    return json.dumps(data, ensure_ascii=False)


# ── Chats ───────────────────────────────────────────────────────────


@mcp.tool()
def ym_chats(page_token: str = "", limit: int = 50, business_id: int = 0) -> str:
    """List chats with customers.

    Args:
        page_token: Pagination token for next page
        limit: Max chats per page (default 50)
        business_id: Business ID (default: from YM_BUSINESS_ID env)
    """
    api = _get_api()
    bid = business_id or _get_business_id()
    data = api.get_chats(bid, page_token=page_token, limit=limit)
    return json.dumps(data, ensure_ascii=False)


@mcp.tool()
def ym_chat_history(chat_id: int, page_token: str = "", limit: int = 50,
                    business_id: int = 0) -> str:
    """Get chat message history.

    Args:
        chat_id: Chat ID from ym_chats
        page_token: Pagination token for next page
        limit: Max messages per page (default 50)
        business_id: Business ID (default: from YM_BUSINESS_ID env)
    """
    api = _get_api()
    bid = business_id or _get_business_id()
    data = api.get_chat_history(bid, chat_id, page_token=page_token, limit=limit)
    return json.dumps(data, ensure_ascii=False)


@mcp.tool()
def ym_chat_send(chat_id: int, message: str, business_id: int = 0) -> str:
    """Send a message in a chat.

    Args:
        chat_id: Chat ID from ym_chats
        message: Message text
        business_id: Business ID (default: from YM_BUSINESS_ID env)
    """
    api = _get_api()
    bid = business_id or _get_business_id()
    data = api.send_chat_message(bid, chat_id, message)
    return json.dumps(data, ensure_ascii=False)


# ── Order Stats ─────────────────────────────────────────────────────


@mcp.tool()
def ym_order_stats(date_from: str = "", date_to: str = "",
                   campaign_id: int = 0) -> str:
    """Get order statistics.

    Args:
        date_from: Start date YYYY-MM-DD (optional)
        date_to: End date YYYY-MM-DD (optional)
        campaign_id: Campaign ID (default: from YM_CAMPAIGN_ID env)
    """
    api = _get_api()
    cid = campaign_id or _get_campaign_id()
    data = api.get_order_stats(cid, date_from=date_from, date_to=date_to)
    return json.dumps(data, ensure_ascii=False)
