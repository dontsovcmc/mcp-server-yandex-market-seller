import json

import pytest
from unittest.mock import patch
from mcp.shared.memory import create_connected_server_and_client_session
from mcp_server_yandex_market_seller.server import mcp


@pytest.mark.anyio
async def test_ym_offers():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_offer_mappings.return_value = {"result": {"offerMappings": [{"offer": {"offerId": "A"}}]}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_offers", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_stocks():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_stocks.return_value = {"result": {"warehouses": []}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_stocks", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_offers_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_offer_mappings.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "offers_update",
                "params_json": json.dumps({"offerMappings": []})
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_offers_delete():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.delete_offer_mappings.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "offers_delete",
                "params_json": json.dumps({"offer_ids": ["SKU1"]})
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_offers_archive():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.archive_offer_mappings.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "offers_archive",
                "params_json": json.dumps({"offer_ids": ["SKU1"], "archive": True})
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_generate_barcodes():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.generate_barcodes.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "generate_barcodes",
                "params_json": json.dumps({"offer_ids": ["SKU1"]})
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_stocks_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_stocks.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_stocks_update", {"stocks_json": "[]"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_campaign_offers():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_campaign_offers.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "campaign_offers",
                "params_json": "{}"
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_hidden_offers():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_hidden_offers.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "hidden_offers",
                "params_json": "{}"
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_unhide_offers():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.unhide_offers.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "unhide_offers",
                "params_json": json.dumps({"offer_ids": ["SKU1"]})
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_offer_cards():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_offer_cards.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "offer_cards",
                "params_json": "{}"
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_offer_cards_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_offer_cards.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "offer_cards_update",
                "params_json": json.dumps({"offerCards": []})
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_offer_recommendations():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_offer_recommendations.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "offer_recommendations",
                "params_json": "{}"
            })
            assert not r.isError
