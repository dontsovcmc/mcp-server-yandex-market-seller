import json
import pytest
from unittest.mock import patch
from mcp.shared.memory import create_connected_server_and_client_session
from mcp_server_yandex_market_seller.server import mcp


@pytest.mark.anyio
async def test_ym_campaigns():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_campaigns.return_value = [{"id": 1, "domain": "shop"}]
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_campaigns", {})
            assert not r.isError
            assert json.loads(r.content[0].text)[0]["id"] == 1


@pytest.mark.anyio
async def test_ym_campaign():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_campaign.return_value = {"id": 1, "domain": "shop"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "campaign", "params_json": json.dumps({"campaign_id": 1})})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_campaign_settings():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_campaign_settings.return_value = {"settings": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "campaign_settings", "params_json": json.dumps({"campaign_id": 1})})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_campaign_settings_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_campaign_settings.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "campaign_settings_update", "params_json": json.dumps({"settings_json": "{}", "campaign_id": 1})})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_business_settings():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_business_settings.return_value = {"settings": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "business_settings", "params_json": json.dumps({"business_id": 1})})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_business_settings_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_business_settings.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "business_settings_update", "params_json": json.dumps({"settings_json": "{}", "business_id": 1})})
            assert not r.isError
