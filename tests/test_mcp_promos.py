import json

import pytest
from unittest.mock import patch
from mcp.shared.memory import create_connected_server_and_client_session
from mcp_server_yandex_market_seller.server import mcp


@pytest.mark.anyio
async def test_ym_promos():
    """ym_promos → ym_execute(action="promos")"""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_promos.return_value = {"result": {"promos": []}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "promos",
                "params_json": json.dumps({}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_bids():
    """ym_bids is a promoted tool — called directly."""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_bids.return_value = {"result": {"bids": []}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_bids", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_promo_offers():
    """ym_promo_offers → ym_execute(action="promo_offers")"""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_promo_offers.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "promo_offers",
                "params_json": json.dumps({"promo_id": "test"}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_promo_offers_update():
    """ym_promo_offers_update → ym_execute(action="promo_offers_update")"""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_promo_offers.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "promo_offers_update",
                "params_json": json.dumps({}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_promo_offers_delete():
    """ym_promo_offers_delete → ym_execute(action="promo_offers_delete")"""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.delete_promo_offers.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "promo_offers_delete",
                "params_json": json.dumps({}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_bids_update():
    """ym_bids_update → ym_execute(action="bids_update")"""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_bids.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "bids_update",
                "params_json": json.dumps({"bids": []}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_campaign_bids():
    """ym_campaign_bids → ym_execute(action="campaign_bids")"""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_campaign_bids.return_value = {"result": {"bids": []}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "campaign_bids",
                "params_json": json.dumps({}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_campaign_bids_update():
    """ym_campaign_bids_update → ym_execute(action="campaign_bids_update")"""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_campaign_bids.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "campaign_bids_update",
                "params_json": json.dumps({"bids": []}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_bid_recommendations():
    """ym_bid_recommendations → ym_execute(action="bid_recommendations")"""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_bid_recommendations.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "bid_recommendations",
                "params_json": json.dumps({}),
            })
            assert not r.isError
