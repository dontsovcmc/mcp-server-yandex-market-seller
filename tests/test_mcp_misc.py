import json
import os
import pytest
from unittest.mock import patch
from mcp.shared.memory import create_connected_server_and_client_session
from mcp_server_yandex_market_seller.server import mcp


# ── Promoted tools ────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_feedbacks():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_feedbacks.return_value = {"result": {"feedbacks": []}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_feedbacks", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_chats():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_chats.return_value = {"result": {"chats": []}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_chats", {})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_report_generate():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.generate_report.return_value = {"result": {"reportId": "abc"}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_report_generate", {"report_type": "united-netting"})
            assert not r.isError


# ── Non-promoted tools via ym_execute ─────────────────────────────


@pytest.mark.anyio
async def test_ym_warehouses():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_warehouses.return_value = {"result": {"warehouses": [{"id": 1}]}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "warehouses", "params_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_logistics_points():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_logistics_points.return_value = {"result": {"logisticPoints": []}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "logistics_points", "params_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_outlets():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_outlets.return_value = {"outlets": []}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "outlets", "params_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_delivery_services():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_delivery_services.return_value = {"deliveryServices": []}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "delivery_services", "params_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_questions():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_questions.return_value = {"result": {"questions": []}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "questions", "params_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_report_status():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_report_status.return_value = {"status": "DONE", "file": "url"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "report_status",
                "params_json": json.dumps({"report_id": "abc"}),
            })
            assert not r.isError
            assert json.loads(r.content[0].text)["status"] == "DONE"


@pytest.mark.anyio
async def test_ym_quality_rating():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_quality_ratings.return_value = {"result": {"ratings": []}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "quality_rating", "params_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_regions():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_regions.return_value = {"regions": [{"id": 213, "name": "Москва"}]}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "regions", "params_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_categories():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_categories_tree.return_value = {"result": {"children": []}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "categories", "params_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_sku_stats():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_sku_stats.return_value = {"result": {"shopSkus": []}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "sku_stats", "params_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_operations():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_operations.return_value = {"result": {"operations": []}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "operations", "params_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_countries():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_countries.return_value = {"regions": [{"id": 225, "name": "Россия"}]}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "countries", "params_json": "{}"})
            assert not r.isError
            assert json.loads(r.content[0].text)["regions"][0]["name"] == "Россия"


@pytest.mark.anyio
async def test_ym_all_warehouses():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_all_warehouses.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "all_warehouses", "params_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_warehouse_status():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.set_warehouse_status.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "warehouse_status",
                "params_json": json.dumps({"enabled": True}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_reception_transfer_act():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_reception_transfer_act.return_value = b"PDF"
        with patch("builtins.open", create=True):
            async with create_connected_server_and_client_session(mcp._mcp_server) as s:
                r = await s.call_tool("ym_execute_file", {
                    "action": "reception_transfer_act",
                    "output_path": "/tmp/out.pdf",
                    "params_json": "{}",
                })
                assert not r.isError


@pytest.mark.anyio
async def test_ym_delivery_options():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_delivery_options.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "delivery_options", "params_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_feedback_skip():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.skip_feedback_reaction.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "feedback_skip", "params_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_feedback_comments():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_feedback_comments.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "feedback_comments",
                "params_json": json.dumps({"feedback_id": 1}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_feedback_comment_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_feedback_comment.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "feedback_comment_update", "params_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_feedback_comment_delete():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.delete_feedback_comment.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "feedback_comment_delete",
                "params_json": json.dumps({"comment_id": 1}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_question_answer():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.answer_question.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "question_answer", "params_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_question_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_question_answer.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "question_update", "params_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_quality_details():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_quality_details.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "quality_details", "params_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_outlet():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_outlet.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "outlet",
                "params_json": json.dumps({"outlet_id": 1}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_outlet_create():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.create_outlet.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "outlet_create", "params_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_outlet_update():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.update_outlet.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "outlet_update",
                "params_json": json.dumps({"outlet_id": 1, "outlet": {}}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_outlet_delete():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.delete_outlet.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "outlet_delete",
                "params_json": json.dumps({"outlet_id": 1}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_outlet_licenses():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_outlet_licenses.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "outlet_licenses", "params_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_region():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_region.return_value = {"id": 213, "name": "Москва"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "region",
                "params_json": json.dumps({"region_id": 213}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_region_children():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_region_children.return_value = {"regions": []}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "region_children",
                "params_json": json.dumps({"region_id": 213}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_category_params():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_category_parameters.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "category_params",
                "params_json": json.dumps({"category_id": 1}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_max_sale_quantum():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_max_sale_quantum.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "max_sale_quantum", "params_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_tariffs():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.calculate_tariffs.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "tariffs",
                "params_json": json.dumps({"offers": []}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_chat_history():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_chat_history.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "chat_history",
                "params_json": json.dumps({"chat_id": 1}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_chat_send():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.send_chat_message.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "chat_send",
                "params_json": json.dumps({"chat_id": 1, "message": "hello"}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_chat_new():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.create_chat.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "chat_new", "params_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_chat_file_send():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.send_chat_file.return_value = {"status": "OK"}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "chat_file_send",
                "params_json": json.dumps({"chat_id": 1, "file_path": "/tmp/file.txt"}),
            })
            assert not r.isError


@pytest.mark.anyio
async def test_ym_report_barcodes():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.generate_barcodes_report.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "report_barcodes", "params_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_order_stats():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_order_stats.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "order_stats", "params_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_supply_requests():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_supply_requests.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "supply_requests", "params_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_supply_request_items():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_supply_request_items.return_value = {"result": {}}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "supply_request_items", "params_json": "{}"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_supply_request_documents():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_supply_request_documents.return_value = b"PDF"
        with patch("builtins.open", create=True):
            async with create_connected_server_and_client_session(mcp._mcp_server) as s:
                r = await s.call_tool("ym_execute_file", {
                    "action": "supply_request_documents",
                    "output_path": "/tmp/out.pdf",
                    "params_json": "{}",
                })
                assert not r.isError


# ── Security: path traversal ───────────────────────────────────────


@pytest.mark.anyio
async def test_order_labels_unsafe_path():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_order_labels.return_value = b"PDF"
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute_file", {
                "action": "order_labels",
                "output_path": "/etc/evil.pdf",
                "params_json": json.dumps({"order_id": 1}),
            })
            assert r.isError
            assert "home or temp" in r.content[0].text.lower()


@pytest.mark.anyio
async def test_reception_transfer_act_unsafe_path():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_reception_transfer_act.return_value = b"PDF"
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute_file", {
                "action": "reception_transfer_act",
                "output_path": "/var/evil.pdf",
                "params_json": "{}",
            })
            assert r.isError


@pytest.mark.anyio
async def test_chat_file_send_unsafe_path():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI"):
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "chat_file_send",
                "params_json": json.dumps({"chat_id": 1, "file_path": "/etc/passwd"}),
            })
            assert r.isError


@pytest.mark.anyio
async def test_order_labels_hidden_file():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_order_labels.return_value = b"PDF"
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            home = os.path.expanduser("~")
            r = await s.call_tool("ym_execute_file", {
                "action": "order_labels",
                "output_path": f"{home}/.ssh/evil.pdf",
                "params_json": json.dumps({"order_id": 1}),
            })
            assert r.isError
            assert "hidden" in r.content[0].text.lower()


# ── Security: invalid JSON ─────────────────────────────────────────


@pytest.mark.anyio
async def test_offers_update_invalid_json():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI"):
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "offers_update",
                "params_json": "not-json",
            })
            assert r.isError
            assert "Invalid JSON" in r.content[0].text


@pytest.mark.anyio
async def test_stocks_update_invalid_json():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI"):
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_stocks_update", {"stocks_json": "{{bad"})
            assert r.isError
            assert "Invalid JSON" in r.content[0].text


@pytest.mark.anyio
async def test_delivery_options_invalid_json():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI"):
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "delivery_options",
                "params_json": "[invalid",
            })
            assert r.isError
            assert "Invalid JSON" in r.content[0].text


# ── API errors ──────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_orders_api_error():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_orders.side_effect = RuntimeError("GET /orders -> 500")
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_orders", {})
            assert r.isError
            assert "500" in r.content[0].text


@pytest.mark.anyio
async def test_feedbacks_api_error():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_feedbacks.side_effect = RuntimeError("GET /feedbacks -> 403")
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_feedbacks", {})
            assert r.isError
            assert "403" in r.content[0].text


@pytest.mark.anyio
async def test_warehouses_api_error():
    with patch("mcp_server_yandex_market_seller.server.YandexMarketAPI") as M:
        M.return_value.get_warehouses.side_effect = RuntimeError("GET /warehouses -> 401")
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {"action": "warehouses", "params_json": "{}"})
            assert r.isError
            assert "401" in r.content[0].text
