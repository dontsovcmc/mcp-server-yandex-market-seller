import json
import pytest
from unittest.mock import patch

from mcp.shared.memory import create_connected_server_and_client_session
from mcp_server_yandex_market_seller.server import mcp


MOCK_OFFERS = {
    "result": {
        "offerMappings": [
            {"offer": {"offerId": "SKU1", "name": "Товар 1"}},
            {"offer": {"offerId": "SKU2", "name": "Товар 2"}},
        ],
        "paging": {"nextPageToken": ""},
    }
}

MOCK_CAMPAIGNS = [
    {"id": 12345, "domain": "test-shop.market.yandex.ru", "state": 1},
]


@pytest.mark.anyio
async def test_ym_offers():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as MockAPI:
        instance = MockAPI.return_value
        instance.get_offer_mappings.return_value = MOCK_OFFERS

        async with create_connected_server_and_client_session(mcp._mcp_server) as session:
            result = await session.call_tool("ym_offers", {})
            assert not result.isError
            data = json.loads(result.content[0].text)
            assert len(data["result"]["offerMappings"]) == 2


@pytest.mark.anyio
async def test_ym_campaigns():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as MockAPI:
        instance = MockAPI.return_value
        instance.get_campaigns.return_value = MOCK_CAMPAIGNS

        async with create_connected_server_and_client_session(mcp._mcp_server) as session:
            result = await session.call_tool("ym_campaigns", {})
            assert not result.isError
            data = json.loads(result.content[0].text)
            assert len(data) == 1
            assert data[0]["id"] == 12345
