import json
import pytest
from unittest.mock import patch

from mcp.shared.memory import create_connected_server_and_client_session
from mcp_server_yandex_market_seller.server import mcp


MOCK_ORDERS = {
    "orders": [
        {"id": 111, "status": "PROCESSING", "creationDate": "2026-04-20"},
        {"id": 222, "status": "DELIVERY", "creationDate": "2026-04-19"},
    ],
    "pager": {"total": 2, "from": 1, "to": 2},
}

MOCK_ORDER = {
    "id": 111,
    "status": "PROCESSING",
    "creationDate": "2026-04-20",
    "items": [{"offerId": "SKU1", "count": 1, "price": 1000}],
}


@pytest.mark.anyio
async def test_ym_orders():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as MockAPI:
        instance = MockAPI.return_value
        instance.get_orders.return_value = MOCK_ORDERS

        async with create_connected_server_and_client_session(mcp._mcp_server) as session:
            result = await session.call_tool("ym_orders", {})
            assert not result.isError
            data = json.loads(result.content[0].text)
            assert len(data["orders"]) == 2


@pytest.mark.anyio
async def test_ym_order():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as MockAPI:
        instance = MockAPI.return_value
        instance.get_order.return_value = MOCK_ORDER

        async with create_connected_server_and_client_session(mcp._mcp_server) as session:
            result = await session.call_tool("ym_order", {"order_id": 111})
            assert not result.isError
            data = json.loads(result.content[0].text)
            assert data["id"] == 111
            assert data["status"] == "PROCESSING"
