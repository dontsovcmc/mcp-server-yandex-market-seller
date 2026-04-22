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
