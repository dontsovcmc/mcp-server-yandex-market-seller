import json

import pytest
from unittest.mock import patch
from mcp.shared.memory import create_connected_server_and_client_session
from mcp_server_yandex_market_seller.server import mcp


@pytest.mark.anyio
async def test_ym_shipments():
    """ym_shipments is a promoted tool — called directly."""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_shipments.return_value = {"result": {"shipments": []}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_shipments", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_shipments_search():
    """ym_shipments_search → ym_execute(action="shipments_search")"""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.search_shipments.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "shipments_search",
                "params_json": json.dumps({}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment():
    """ym_shipment → ym_execute(action="shipment")"""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_shipment.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "shipment",
                "params_json": json.dumps({"shipment_id": 1}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_update():
    """ym_shipment_update → ym_execute(action="shipment_update")"""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_shipment.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "shipment_update",
                "params_json": json.dumps({"shipment_id": 1, "payload": {}}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_confirm():
    """ym_shipment_confirm → ym_execute(action="shipment_confirm")"""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.confirm_shipment.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "shipment_confirm",
                "params_json": json.dumps({"shipment_id": 1}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_orders():
    """ym_shipment_orders → ym_execute(action="shipment_orders")"""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_shipment_orders.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "shipment_orders",
                "params_json": json.dumps({"shipment_id": 1}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_transfer():
    """ym_shipment_transfer → ym_execute(action="shipment_transfer")"""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.transfer_shipment_orders.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "shipment_transfer",
                "params_json": json.dumps({"shipment_id": 1, "payload": {}}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_act():
    """ym_shipment_act is a file tool → ym_execute_file(action="shipment_act")"""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_shipment_act.return_value = b"PDF"
        with patch("builtins.open", create=True):
            async with create_connected_server_and_client_session(mcp._mcp_server) as s:
                r = await s.call_tool("ym_execute_file", {
                    "action": "shipment_act",
                    "output_path": "/tmp/out.pdf",
                    "params_json": json.dumps({"shipment_id": 1}),
                })
                assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_inbound_act():
    """ym_shipment_inbound_act is a file tool → ym_execute_file(action="shipment_inbound_act")"""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_shipment_inbound_act.return_value = b"PDF"
        with patch("builtins.open", create=True):
            async with create_connected_server_and_client_session(mcp._mcp_server) as s:
                r = await s.call_tool("ym_execute_file", {
                    "action": "shipment_inbound_act",
                    "output_path": "/tmp/out.pdf",
                    "params_json": json.dumps({"shipment_id": 1}),
                })
                assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_waybill():
    """ym_shipment_waybill is a file tool → ym_execute_file(action="shipment_waybill")"""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_shipment_waybill.return_value = b"PDF"
        with patch("builtins.open", create=True):
            async with create_connected_server_and_client_session(mcp._mcp_server) as s:
                r = await s.call_tool("ym_execute_file", {
                    "action": "shipment_waybill",
                    "output_path": "/tmp/out.pdf",
                    "params_json": json.dumps({"shipment_id": 1}),
                })
                assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_discrepancy_act():
    """ym_shipment_discrepancy_act is a file tool → ym_execute_file(action="shipment_discrepancy_act")"""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_shipment_discrepancy_act.return_value = b"PDF"
        with patch("builtins.open", create=True):
            async with create_connected_server_and_client_session(mcp._mcp_server) as s:
                r = await s.call_tool("ym_execute_file", {
                    "action": "shipment_discrepancy_act",
                    "output_path": "/tmp/out.pdf",
                    "params_json": json.dumps({"shipment_id": 1}),
                })
                assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_pallets():
    """ym_shipment_pallets → ym_execute(action="shipment_pallets")"""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_shipment_pallets.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "shipment_pallets",
                "params_json": json.dumps({"shipment_id": 1}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_pallets_update():
    """ym_shipment_pallets_update → ym_execute(action="shipment_pallets_update")"""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.set_shipment_pallets.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "shipment_pallets_update",
                "params_json": json.dumps({"shipment_id": 1, "pallets": []}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_pallet_labels():
    """ym_shipment_pallet_labels is a file tool → ym_execute_file(action="shipment_pallet_labels")"""
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_shipment_pallet_labels.return_value = b"PDF"
        with patch("builtins.open", create=True):
            async with create_connected_server_and_client_session(mcp._mcp_server) as s:
                r = await s.call_tool("ym_execute_file", {
                    "action": "shipment_pallet_labels",
                    "output_path": "/tmp/out.pdf",
                    "params_json": json.dumps({"shipment_id": 1}),
                })
                assert not r.isError
