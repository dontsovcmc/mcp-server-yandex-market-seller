import json
import pytest
from unittest.mock import patch
from mcp.shared.memory import create_connected_server_and_client_session
from mcp_server_yandex_market_seller.server import mcp


@pytest.mark.anyio
async def test_ym_orders():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_orders.return_value = {"orders": [{"id": 10}], "pager": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_orders", {})
            assert not r.isError
            assert len(json.loads(r.content[0].text)["orders"]) == 1


@pytest.mark.anyio
async def test_ym_order():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_order.return_value = {"id": 10, "status": "PROCESSING"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_order", {"order_id": 10})
            assert not r.isError
            assert json.loads(r.content[0].text)["status"] == "PROCESSING"


@pytest.mark.anyio
async def test_ym_order_status():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_order_status.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_order_status", {"order_id": 1, "status": "DELIVERY"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_status_batch():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.batch_update_order_statuses.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "order_status_batch", "params_json": json.dumps({"orders": []})})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_labels():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_order_labels.return_value = b"PDF"
        with patch("builtins.open", create=True):
            async with create_connected_server_and_client_session(mcp._mcp_server) as s:
                r = await s.call_tool("ym_execute_file", {"action": "order_labels", "output_path": "/tmp/out.pdf", "params_json": json.dumps({"order_id": 1})})
                assert not r.isError


@pytest.mark.anyio
async def test_ym_order_labels_data():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_order_labels_data.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "order_labels_data", "params_json": json.dumps({"order_id": 1})})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_box_label():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_order_box_label.return_value = b"PDF"
        with patch("builtins.open", create=True):
            async with create_connected_server_and_client_session(mcp._mcp_server) as s:
                r = await s.call_tool("ym_execute_file", {"action": "order_box_label", "output_path": "/tmp/out.pdf", "params_json": json.dumps({"order_id": 1, "shipment_id": 1, "box_id": 1})})
                assert not r.isError


@pytest.mark.anyio
async def test_ym_order_items():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_order_items.return_value = {"items": []}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "order_items", "params_json": json.dumps({"order_id": 1})})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_items_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_order_items.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "order_items_update", "params_json": json.dumps({"order_id": 1, "items": []})})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_boxes():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_order_boxes.return_value = {"boxes": []}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "order_boxes", "params_json": json.dumps({"order_id": 1})})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_boxes_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_order_boxes.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "order_boxes_update", "params_json": json.dumps({"order_id": 1, "boxes": []})})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_shipment_boxes():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.set_shipment_boxes.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "order_shipment_boxes", "params_json": json.dumps({"order_id": 1, "shipment_id": 1, "boxes": []})})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_cancel_accept():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.accept_order_cancellation.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "order_cancel_accept", "params_json": json.dumps({"order_id": 1})})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_delivery_date():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.set_order_delivery_date.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "order_delivery_date", "params_json": json.dumps({"order_id": 1, "dates": {}})})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_tracking():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_order_tracking.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "order_tracking", "params_json": json.dumps({"order_id": 1})})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_tracking_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.set_order_tracking.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "order_tracking_update", "params_json": json.dumps({"order_id": 1, "tracks": []})})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_buyer():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_order_buyer.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "order_buyer", "params_json": json.dumps({"order_id": 1})})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_business_buyer():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_order_business_buyer.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "order_business_buyer", "params_json": json.dumps({"order_id": 1})})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_verify_eac():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.verify_order_eac.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "order_verify_eac", "params_json": json.dumps({"order_id": 1, "code": "1234"})})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_storage_limit():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_order_storage_limit.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "order_storage_limit", "params_json": json.dumps({"order_id": 1})})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_storage_limit_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.set_order_storage_limit.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "order_storage_limit_update", "params_json": json.dumps({"order_id": 1, "date": "2026-01-01"})})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_deliver_digital():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.deliver_digital_goods.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "order_deliver_digital", "params_json": json.dumps({"order_id": 1, "items": []})})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_documents():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_order_documents.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "order_documents", "params_json": json.dumps({"order_id": 1})})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_document_create():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.create_order_document.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "order_document_create", "params_json": json.dumps({"order_id": 1, "document": {}})})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_business_orders():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_business_orders.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "business_orders", "params_json": json.dumps({"business_id": 1})})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_create():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.create_order_v1.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "order_create", "params_json": json.dumps({})})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_update_v1():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_order_v1.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "order_update_v1", "params_json": json.dumps({})})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_update_options():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_order_options.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "order_update_options", "params_json": json.dumps({})})
            assert not r.isError
