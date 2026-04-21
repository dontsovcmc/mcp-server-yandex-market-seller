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
