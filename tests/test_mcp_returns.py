import pytest
from unittest.mock import patch
from mcp.shared.memory import create_connected_server_and_client_session
from mcp_server_yandex_market_seller.server import mcp


@pytest.mark.anyio
async def test_ym_returns():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_returns.return_value = {"returns": [], "pager": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_returns", {})
            assert not r.isError


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


@pytest.mark.anyio
async def test_ym_return_delivery_options():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_return_delivery_options.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_return_delivery_options", {"payload_json": "{}"})
            assert not r.isError
