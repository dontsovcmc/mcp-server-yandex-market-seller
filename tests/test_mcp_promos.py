import json
import pytest
from unittest.mock import patch
from mcp.shared.memory import create_connected_server_and_client_session
from mcp_server_yandex_market_seller.server import mcp


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
