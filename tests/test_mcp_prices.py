import json

import pytest
from unittest.mock import patch
from mcp.shared.memory import create_connected_server_and_client_session
from mcp_server_yandex_market_seller.server import mcp


@pytest.mark.anyio
async def test_ym_prices():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_business_offer_prices.return_value = {"result": {"offers": []}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_prices", {})
            assert not r.isError


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
            r = await s.call_tool("ym_execute", {
                "action": "price_quarantine",
                "params_json": "{}"
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_price_quarantine_confirm():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.confirm_price_quarantine.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "price_quarantine_confirm",
                "params_json": json.dumps({"offer_ids": ["SKU1"]})
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_campaign_price_quarantine():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_campaign_price_quarantine.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "campaign_price_quarantine",
                "params_json": "{}"
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_campaign_price_quarantine_confirm():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.confirm_campaign_price_quarantine.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "campaign_price_quarantine_confirm",
                "params_json": json.dumps({"offer_ids": ["SKU1"]})
            })
            assert not r.isError
