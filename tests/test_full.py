import json
import pytest
from unittest.mock import patch

from mcp.shared.memory import create_connected_server_and_client_session
from mcp_server_yandex_market_seller.server import mcp


def _call(tool_name, params=None):
    """Helper: call tool, return parsed JSON."""
    async def _inner():
        with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
            inst = M.return_value
            yield inst
    return tool_name, params or {}


@pytest.mark.anyio
async def test_ym_campaigns():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_campaigns.return_value = [{"id": 1, "domain": "shop"}]
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_campaigns", {})
            assert not r.isError
            assert json.loads(r.content[0].text)[0]["id"] == 1


@pytest.mark.anyio
async def test_ym_orders():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_orders.return_value = {"orders": [{"id": 10}], "pager": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_orders", {})
            assert not r.isError
            assert len(json.loads(r.content[0].text)["orders"]) == 1


@pytest.mark.anyio
async def test_ym_order():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_order.return_value = {"id": 10, "status": "PROCESSING"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_order", {"order_id": 10})
            assert not r.isError
            assert json.loads(r.content[0].text)["status"] == "PROCESSING"


@pytest.mark.anyio
async def test_ym_offers():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_offer_mappings.return_value = {"result": {"offerMappings": [{"offer": {"offerId": "A"}}]}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_offers", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_prices():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_business_offer_prices.return_value = {"result": {"offers": []}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_prices", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_stocks():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_stocks.return_value = {"result": {"warehouses": []}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_stocks", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_returns():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_returns.return_value = {"returns": [], "pager": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_returns", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_feedbacks():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_feedbacks.return_value = {"result": {"feedbacks": []}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_feedbacks", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_warehouses():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_warehouses.return_value = {"result": {"warehouses": [{"id": 1}]}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_warehouses", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_shipments():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_shipments.return_value = {"result": {"shipments": []}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_shipments", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_logistics_points():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_logistics_points.return_value = {"result": {"logisticPoints": []}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_logistics_points", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_outlets():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_outlets.return_value = {"outlets": []}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_outlets", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_delivery_services():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_delivery_services.return_value = {"deliveryServices": []}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_delivery_services", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_questions():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_questions.return_value = {"result": {"questions": []}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_questions", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_report_status():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_report_status.return_value = {"status": "DONE", "file": "url"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_report_status", {"report_id": "abc"})
            assert not r.isError
            assert json.loads(r.content[0].text)["status"] == "DONE"


@pytest.mark.anyio
async def test_ym_quality_rating():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_quality_ratings.return_value = {"result": {"ratings": []}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_quality_rating", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_promos():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_promos.return_value = {"result": {"promos": []}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_promos", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_bids():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_bids.return_value = {"result": {"bids": []}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_bids", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_chats():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_chats.return_value = {"result": {"chats": []}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_chats", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_regions():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_regions.return_value = {"regions": [{"id": 213, "name": "Москва"}]}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_regions", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_categories():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_categories_tree.return_value = {"result": {"children": []}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_categories", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_sku_stats():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_sku_stats.return_value = {"result": {"shopSkus": []}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_sku_stats", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_operations():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_operations.return_value = {"result": {"operations": []}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_operations", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_countries():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_countries.return_value = {"regions": [{"id": 225, "name": "Россия"}]}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_countries", {})
            assert not r.isError
            assert json.loads(r.content[0].text)["regions"][0]["name"] == "Россия"


# ── Campaigns & Settings ────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_campaign():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_campaign.return_value = {"id": 1, "domain": "shop"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_campaign", {"campaign_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_campaign_settings():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_campaign_settings.return_value = {"settings": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_campaign_settings", {"campaign_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_campaign_settings_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_campaign_settings.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_campaign_settings_update", {"settings_json": "{}", "campaign_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_business_settings():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_business_settings.return_value = {"settings": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_business_settings", {"business_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_business_settings_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_business_settings.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_business_settings_update", {"settings_json": "{}", "business_id": 1})
            assert not r.isError


# ── Orders v2 ───────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_order_status():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_order_status.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_order_status", {"order_id": 1, "status": "DELIVERY"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_status_batch():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.batch_update_order_statuses.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_order_status_batch", {"updates_json": "[]"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_labels():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_order_labels.return_value = b"PDF"
        with patch("builtins.open", create=True):
            async with create_connected_server_and_client_session(mcp._mcp_server) as s:
                r = await s.call_tool("ym_order_labels", {"order_id": 1, "output_path": "/tmp/out.pdf"})
                assert not r.isError


@pytest.mark.anyio
async def test_ym_order_labels_data():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_order_labels_data.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_order_labels_data", {"order_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_box_label():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_order_box_label.return_value = b"PDF"
        with patch("builtins.open", create=True):
            async with create_connected_server_and_client_session(mcp._mcp_server) as s:
                r = await s.call_tool("ym_order_box_label", {"order_id": 1, "shipment_id": 1, "box_id": 1, "output_path": "/tmp/out.pdf"})
                assert not r.isError


@pytest.mark.anyio
async def test_ym_order_items():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_order_items.return_value = {"items": []}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_order_items", {"order_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_items_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_order_items.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_order_items_update", {"order_id": 1, "items_json": "[]"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_boxes():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_order_boxes.return_value = {"boxes": []}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_order_boxes", {"order_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_boxes_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_order_boxes.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_order_boxes_update", {"order_id": 1, "boxes_json": "[]"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_shipment_boxes():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.set_shipment_boxes.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_order_shipment_boxes", {"order_id": 1, "shipment_id": 1, "boxes_json": "[]"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_cancel_accept():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.accept_order_cancellation.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_order_cancel_accept", {"order_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_delivery_date():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.set_order_delivery_date.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_order_delivery_date", {"order_id": 1, "dates_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_tracking():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_order_tracking.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_order_tracking", {"order_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_tracking_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.set_order_tracking.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_order_tracking_update", {"order_id": 1, "tracks_json": "[]"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_buyer():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_order_buyer.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_order_buyer", {"order_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_business_buyer():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_order_business_buyer.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_order_business_buyer", {"order_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_verify_eac():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.verify_order_eac.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_order_verify_eac", {"order_id": 1, "code": "1234"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_storage_limit():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_order_storage_limit.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_order_storage_limit", {"order_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_storage_limit_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.set_order_storage_limit.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_order_storage_limit_update", {"order_id": 1, "date": "2026-01-01"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_deliver_digital():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.deliver_digital_goods.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_order_deliver_digital", {"order_id": 1, "items_json": "[]"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_documents():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_order_documents.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_order_documents", {"order_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_document_create():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.create_order_document.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_order_document_create", {"order_id": 1, "document_json": "{}"})
            assert not r.isError


# ── Orders v1 ───────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_business_orders():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_business_orders.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_business_orders", {"payload_json": "{}", "business_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_create():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.create_order_v1.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_order_create", {"order_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_update_v1():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_order_v1.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_order_update_v1", {"order_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_update_options():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_order_options.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_order_update_options", {"options_json": "{}"})
            assert not r.isError


# ── Returns ─────────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_return():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_return.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_return", {"order_id": 1, "return_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_return_decision():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_return_decision.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_return_decision", {"order_id": 1, "return_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_return_decision_set():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.set_return_decision.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_return_decision_set", {"order_id": 1, "return_id": 1, "decision_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_return_decision_submit():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.submit_return_decision.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_return_decision_submit", {"order_id": 1, "return_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_return_application():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_return_application.return_value = b"PDF"
        with patch("builtins.open", create=True):
            async with create_connected_server_and_client_session(mcp._mcp_server) as s:
                r = await s.call_tool("ym_return_application", {"order_id": 1, "return_id": 1, "output_path": "/tmp/out.pdf"})
                assert not r.isError


@pytest.mark.anyio
async def test_ym_business_return_decisions():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_business_return_decisions.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_business_return_decisions", {"payload_json": "{}", "business_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_return_create():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.create_return_v1.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_return_create", {"return_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_return_cancel():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.cancel_return_v1.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_return_cancel", {"return_json": "{}"})
            assert not r.isError


# ── First-Mile Shipments ────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_shipments_search():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.search_shipments.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_shipments_search", {"payload_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_shipment.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_shipment", {"shipment_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_shipment.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_shipment_update", {"shipment_id": 1, "payload_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_confirm():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.confirm_shipment.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_shipment_confirm", {"shipment_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_orders():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_shipment_orders.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_shipment_orders", {"shipment_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_transfer():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.transfer_shipment_orders.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_shipment_transfer", {"shipment_id": 1, "payload_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_act():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_shipment_act.return_value = b"PDF"
        with patch("builtins.open", create=True):
            async with create_connected_server_and_client_session(mcp._mcp_server) as s:
                r = await s.call_tool("ym_shipment_act", {"shipment_id": 1, "output_path": "/tmp/out.pdf"})
                assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_inbound_act():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_shipment_inbound_act.return_value = b"PDF"
        with patch("builtins.open", create=True):
            async with create_connected_server_and_client_session(mcp._mcp_server) as s:
                r = await s.call_tool("ym_shipment_inbound_act", {"shipment_id": 1, "output_path": "/tmp/out.pdf"})
                assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_waybill():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_shipment_waybill.return_value = b"PDF"
        with patch("builtins.open", create=True):
            async with create_connected_server_and_client_session(mcp._mcp_server) as s:
                r = await s.call_tool("ym_shipment_waybill", {"shipment_id": 1, "output_path": "/tmp/out.pdf"})
                assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_discrepancy_act():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_shipment_discrepancy_act.return_value = b"PDF"
        with patch("builtins.open", create=True):
            async with create_connected_server_and_client_session(mcp._mcp_server) as s:
                r = await s.call_tool("ym_shipment_discrepancy_act", {"shipment_id": 1, "output_path": "/tmp/out.pdf"})
                assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_pallets():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_shipment_pallets.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_shipment_pallets", {"shipment_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_pallets_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.set_shipment_pallets.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_shipment_pallets_update", {"shipment_id": 1, "pallets_json": "[]"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_pallet_labels():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_shipment_pallet_labels.return_value = b"PDF"
        with patch("builtins.open", create=True):
            async with create_connected_server_and_client_session(mcp._mcp_server) as s:
                r = await s.call_tool("ym_shipment_pallet_labels", {"shipment_id": 1, "output_path": "/tmp/out.pdf"})
                assert not r.isError


# ── Warehouses ──────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_all_warehouses():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_all_warehouses.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_all_warehouses", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_warehouse_status():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.set_warehouse_status.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_warehouse_status", {"enabled": True})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_reception_transfer_act():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_reception_transfer_act.return_value = b"PDF"
        with patch("builtins.open", create=True):
            async with create_connected_server_and_client_session(mcp._mcp_server) as s:
                r = await s.call_tool("ym_reception_transfer_act", {"output_path": "/tmp/out.pdf"})
                assert not r.isError


# ── Offers (products) ──────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_offers_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_offer_mappings.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_offers_update", {"offers_json": "[]"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_offers_delete():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.delete_offer_mappings.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_offers_delete", {"offer_ids": "SKU1"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_offers_archive():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.archive_offer_mappings.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_offers_archive", {"offer_ids": "SKU1"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_generate_barcodes():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.generate_barcodes.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_generate_barcodes", {"offer_ids": "SKU1"})
            assert not r.isError


# ── Prices ──────────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_prices_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_business_offer_prices.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_prices_update", {"prices_json": "[]"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_price_quarantine():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_price_quarantine.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_price_quarantine", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_price_quarantine_confirm():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.confirm_price_quarantine.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_price_quarantine_confirm", {"offer_ids": "SKU1"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_campaign_price_quarantine():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_campaign_price_quarantine.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_campaign_price_quarantine", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_campaign_price_quarantine_confirm():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.confirm_campaign_price_quarantine.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_campaign_price_quarantine_confirm", {"offer_ids": "SKU1"})
            assert not r.isError


# ── Stocks ──────────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_stocks_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_stocks.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_stocks_update", {"stocks_json": "[]"})
            assert not r.isError


# ── Campaign Offers ─────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_campaign_offers():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_campaign_offers.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_campaign_offers", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_hidden_offers():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_hidden_offers.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_hidden_offers", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_unhide_offers():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.unhide_offers.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_unhide_offers", {"offer_ids": "SKU1"})
            assert not r.isError


# ── Offer Cards ─────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_offer_cards():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_offer_cards.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_offer_cards", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_offer_cards_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_offer_cards.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_offer_cards_update", {"cards_json": "[]"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_offer_recommendations():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_offer_recommendations.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_offer_recommendations", {})
            assert not r.isError


# ── Delivery ────────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_delivery_options():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_delivery_options.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_delivery_options", {"payload_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_return_delivery_options():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_return_delivery_options.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_return_delivery_options", {"payload_json": "{}"})
            assert not r.isError


# ── Feedbacks ───────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_feedback_skip():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.skip_feedback_reaction.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_feedback_skip", {"feedback_ids_json": "[]"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_feedback_comments():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_feedback_comments.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_feedback_comments", {"feedback_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_feedback_comment_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_feedback_comment.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_feedback_comment_update", {"comment_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_feedback_comment_delete():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.delete_feedback_comment.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_feedback_comment_delete", {"comment_id": 1})
            assert not r.isError


# ── Q&A ─────────────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_question_answer():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.answer_question.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_question_answer", {"answer_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_question_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_question_answer.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_question_update", {"update_json": "{}"})
            assert not r.isError


# ── Quality Rating ──────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_quality_details():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_quality_details.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_quality_details", {})
            assert not r.isError


# ── Promos ──────────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_promo_offers():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_promo_offers.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_promo_offers", {"promo_id": "test"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_promo_offers_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_promo_offers.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_promo_offers_update", {"payload_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_promo_offers_delete():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.delete_promo_offers.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_promo_offers_delete", {"payload_json": "{}"})
            assert not r.isError


# ── Bids ────────────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_bids_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_bids.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_bids_update", {"bids_json": "[]"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_campaign_bids():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_campaign_bids.return_value = {"result": {"bids": []}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_campaign_bids", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_campaign_bids_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_campaign_bids.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_campaign_bids_update", {"bids_json": "[]"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_bid_recommendations():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_bid_recommendations.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_bid_recommendations", {})
            assert not r.isError


# ── Outlets ─────────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_outlet():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_outlet.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_outlet", {"outlet_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_outlet_create():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.create_outlet.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_outlet_create", {"outlet_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_outlet_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_outlet.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_outlet_update", {"outlet_id": 1, "outlet_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_outlet_delete():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.delete_outlet.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_outlet_delete", {"outlet_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_outlet_licenses():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_outlet_licenses.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_outlet_licenses", {})
            assert not r.isError


# ── Regions ─────────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_region():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_region.return_value = {"id": 213, "name": "Москва"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_region", {"region_id": 213})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_region_children():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_region_children.return_value = {"regions": []}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_region_children", {"region_id": 213})
            assert not r.isError


# ── Categories ──────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_category_params():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_category_parameters.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_category_params", {"category_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_max_sale_quantum():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_max_sale_quantum.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_max_sale_quantum", {"payload_json": "{}"})
            assert not r.isError


# ── Tariffs ─────────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_tariffs():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.calculate_tariffs.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_tariffs", {"offers_json": "[]"})
            assert not r.isError


# ── Chats ───────────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_chat_history():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_chat_history.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_chat_history", {"chat_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_chat_send():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.send_chat_message.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_chat_send", {"chat_id": 1, "message": "hello"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_chat_new():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.create_chat.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_chat_new", {"payload_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_chat_file_send():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.send_chat_file.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_chat_file_send", {"chat_id": 1, "file_path": "/tmp/file.txt"})
            assert not r.isError


# ── Reports ─────────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_report_generate():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.generate_report.return_value = {"result": {"reportId": "abc"}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_report_generate", {"report_type": "united-netting"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_report_barcodes():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.generate_barcodes_report.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_report_barcodes", {"payload_json": "{}"})
            assert not r.isError


# ── Stats ───────────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_order_stats():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_order_stats.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_order_stats", {})
            assert not r.isError


# ── Supply Requests ─────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_supply_requests():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_supply_requests.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_supply_requests", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_supply_request_items():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_supply_request_items.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_supply_request_items", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_supply_request_documents():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_supply_request_documents.return_value = b"PDF"
        with patch("builtins.open", create=True):
            async with create_connected_server_and_client_session(mcp._mcp_server) as s:
                r = await s.call_tool("ym_supply_request_documents", {"output_path": "/tmp/out.pdf"})
                assert not r.isError
