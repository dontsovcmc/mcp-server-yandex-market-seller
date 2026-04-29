import json

import pytest
from unittest.mock import patch
from mcp.shared.memory import create_connected_server_and_client_session
from mcp_server_yandex_market_seller.server import mcp


@pytest.mark.anyio
async def test_ym_returns():
    """ym_returns is a promoted tool — called directly."""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_returns.return_value = {"returns": [], "pager": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_returns", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_return():
    """ym_return → ym_execute(action="return")"""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_return.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "return",
                "params_json": json.dumps({"order_id": 1, "return_id": 1}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_return_decision():
    """ym_return_decision → ym_execute(action="return_decision")"""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_return_decision.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "return_decision",
                "params_json": json.dumps({"order_id": 1, "return_id": 1}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_return_decision_set():
    """ym_return_decision_set → ym_execute(action="return_decision_set")"""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.set_return_decision.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "return_decision_set",
                "params_json": json.dumps({"order_id": 1, "return_id": 1, "decision": {}}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_return_decision_submit():
    """ym_return_decision_submit → ym_execute(action="return_decision_submit")"""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.submit_return_decision.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "return_decision_submit",
                "params_json": json.dumps({"order_id": 1, "return_id": 1}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_return_application():
    """ym_return_application is a file tool → ym_execute_file(action="return_application")"""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_return_application.return_value = b"PDF"
        with patch("builtins.open", create=True):
            async with create_connected_server_and_client_session(mcp._mcp_server) as s:
                r = await s.call_tool("ym_execute_file", {
                    "action": "return_application",
                    "output_path": "/tmp/out.pdf",
                    "params_json": json.dumps({"order_id": 1, "return_id": 1}),
                })
                assert not r.isError


@pytest.mark.anyio
async def test_ym_business_return_decisions():
    """ym_business_return_decisions → ym_execute(action="business_return_decisions")"""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_business_return_decisions.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "business_return_decisions",
                "params_json": json.dumps({"business_id": 1}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_return_create():
    """ym_return_create → ym_execute(action="return_create")"""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.create_return_v1.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "return_create",
                "params_json": json.dumps({}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_return_cancel():
    """ym_return_cancel → ym_execute(action="return_cancel")"""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.cancel_return_v1.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "return_cancel",
                "params_json": json.dumps({}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_return_delivery_options():
    """ym_return_delivery_options → ym_execute(action="return_delivery_options")"""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_return_delivery_options.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "return_delivery_options",
                "params_json": json.dumps({}),
            })
            assert not r.isError
