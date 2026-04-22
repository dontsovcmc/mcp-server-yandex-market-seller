import json
import pytest
from unittest.mock import patch
from mcp.shared.memory import create_connected_server_and_client_session
from mcp_server_yandex_market_seller.server import mcp


@pytest.mark.anyio
async def test_ym_shipments():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_shipments.return_value = {"result": {"shipments": []}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_shipments", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_shipments_search():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.search_shipments.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_shipments_search", {"payload_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_shipment.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_shipment", {"shipment_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_shipment.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_shipment_update", {"shipment_id": 1, "payload_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_confirm():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.confirm_shipment.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_shipment_confirm", {"shipment_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_orders():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_shipment_orders.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_shipment_orders", {"shipment_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_transfer():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.transfer_shipment_orders.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_shipment_transfer", {"shipment_id": 1, "payload_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_act():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_shipment_act.return_value = b"PDF"
        with patch("builtins.open", create=True):
            async with create_connected_server_and_client_session(mcp._mcp_server) as s:
                r = await s.call_tool("ym_shipment_act", {"shipment_id": 1, "output_path": "/tmp/out.pdf"})
                assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_inbound_act():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_shipment_inbound_act.return_value = b"PDF"
        with patch("builtins.open", create=True):
            async with create_connected_server_and_client_session(mcp._mcp_server) as s:
                r = await s.call_tool("ym_shipment_inbound_act", {"shipment_id": 1, "output_path": "/tmp/out.pdf"})
                assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_waybill():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_shipment_waybill.return_value = b"PDF"
        with patch("builtins.open", create=True):
            async with create_connected_server_and_client_session(mcp._mcp_server) as s:
                r = await s.call_tool("ym_shipment_waybill", {"shipment_id": 1, "output_path": "/tmp/out.pdf"})
                assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_discrepancy_act():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_shipment_discrepancy_act.return_value = b"PDF"
        with patch("builtins.open", create=True):
            async with create_connected_server_and_client_session(mcp._mcp_server) as s:
                r = await s.call_tool("ym_shipment_discrepancy_act", {"shipment_id": 1, "output_path": "/tmp/out.pdf"})
                assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_pallets():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_shipment_pallets.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_shipment_pallets", {"shipment_id": 1})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_pallets_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.set_shipment_pallets.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_shipment_pallets_update", {"shipment_id": 1, "pallets_json": "[]"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_shipment_pallet_labels():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_shipment_pallet_labels.return_value = b"PDF"
        with patch("builtins.open", create=True):
            async with create_connected_server_and_client_session(mcp._mcp_server) as s:
                r = await s.call_tool("ym_shipment_pallet_labels", {"shipment_id": 1, "output_path": "/tmp/out.pdf"})
                assert not r.isError
