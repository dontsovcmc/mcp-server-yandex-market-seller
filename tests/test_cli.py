"""Tests for CLI interface — all 131 commands."""

import re
from pathlib import Path
from unittest.mock import patch

import pytest

from mcp_server_yandex_market_seller.cli import main


def test_cli_parity():
    src = (Path(__file__).parent.parent / "src/mcp_server_yandex_market_seller/cli.py").read_text()
    parsers = set(re.findall(r'sub\.add_parser\("([^"]+)"', src))
    handlers = set(re.findall(r'"([^"]+)":\s*lambda', src))
    assert parsers == handlers
    assert len(parsers) == 131


# (argv_list, expected_call_type, expected_call_arg)
# call_type: "promoted" -> calls server.ym_*, "action" -> calls server.execute_action, "file" -> server.execute_file_action
# fmt: off
CLI_COMMANDS = [
    # --- campaigns ---
    (["campaigns"], "action", "campaigns"),
    (["campaign"], "action", "campaign"),
    (["campaign-settings"], "action", "campaign_settings"),
    (["campaign-settings-update", "{}"], "action", "campaign_settings_update"),
    (["business-settings"], "action", "business_settings"),
    (["business-settings-update", "{}"], "action", "business_settings_update"),

    # --- orders ---
    (["orders"], "promoted", "ym_orders"),
    (["order", "123"], "promoted", "ym_order"),
    (["order-items", "123"], "action", "order_items"),
    (["order-buyer", "123"], "action", "order_buyer"),
    (["order-tracking", "123"], "action", "order_tracking"),
    (["order-status", "123", "PROCESSING"], "promoted", "ym_order_status"),
    (["order-status-batch", "[]"], "action", "order_status_batch"),
    (["order-labels", "123", "/tmp/out.pdf"], "file", "order_labels"),
    (["order-labels-data", "123"], "action", "order_labels_data"),
    (["order-box-label", "1", "2", "3", "/tmp/out.pdf"], "file", "order_box_label"),
    (["order-items-update", "123", "[]"], "action", "order_items_update"),
    (["order-boxes", "123"], "action", "order_boxes"),
    (["order-boxes-update", "123", "[]"], "action", "order_boxes_update"),
    (["order-shipment-boxes", "123", "456", "[]"], "action", "order_shipment_boxes"),
    (["order-cancel-accept", "123"], "action", "order_cancel_accept"),
    (["order-delivery-date", "123", "{}"], "action", "order_delivery_date"),
    (["order-tracking-update", "123", "[]"], "action", "order_tracking_update"),
    (["order-business-buyer", "123"], "action", "order_business_buyer"),
    (["order-verify-eac", "123", "ABC"], "action", "order_verify_eac"),
    (["order-storage-limit", "123"], "action", "order_storage_limit"),
    (["order-storage-limit-update", "123", "2025-01-01"], "action", "order_storage_limit_update"),
    (["order-deliver-digital", "123", "[]"], "action", "order_deliver_digital"),
    (["order-documents", "123"], "action", "order_documents"),
    (["order-document-create", "123", "{}"], "action", "order_document_create"),
    (["business-orders", "{}"], "action", "business_orders"),
    (["order-create", "{}"], "action", "order_create"),
    (["order-update-v1", "{}"], "action", "order_update_v1"),
    (["order-update-options", "{}"], "action", "order_update_options"),

    # --- offers ---
    (["offers"], "promoted", "ym_offers"),
    (["offer-cards"], "action", "offer_cards"),
    (["offers-update", "[]"], "action", "offers_update"),
    (["offers-delete", "sku1,sku2"], "action", "offers_delete"),
    (["offers-archive", "sku1,sku2"], "action", "offers_archive"),
    (["generate-barcodes", "sku1,sku2"], "action", "generate_barcodes"),

    # --- prices ---
    (["prices"], "promoted", "ym_prices"),
    (["prices-update", "[]"], "promoted", "ym_prices_update"),
    (["price-quarantine"], "action", "price_quarantine"),
    (["price-quarantine-confirm", "sku1,sku2"], "action", "price_quarantine_confirm"),
    (["campaign-price-quarantine"], "action", "campaign_price_quarantine"),
    (["campaign-price-quarantine-confirm", "sku1,sku2"], "action", "campaign_price_quarantine_confirm"),

    # --- stocks ---
    (["stocks"], "promoted", "ym_stocks"),
    (["stocks-update", "[]"], "promoted", "ym_stocks_update"),

    # --- hidden / campaign offers ---
    (["hidden-offers"], "action", "hidden_offers"),
    (["campaign-offers"], "action", "campaign_offers"),
    (["unhide-offers", "sku1,sku2"], "action", "unhide_offers"),

    # --- offer cards ---
    (["offer-cards-update", "[]"], "action", "offer_cards_update"),
    (["offer-recommendations"], "action", "offer_recommendations"),

    # --- returns ---
    (["returns"], "promoted", "ym_returns"),
    (["return", "123", "456"], "action", "return"),
    (["return-decision", "123", "456"], "action", "return_decision"),
    (["return-decision-set", "123", "456", "{}"], "action", "return_decision_set"),
    (["return-decision-submit", "123", "456"], "action", "return_decision_submit"),
    (["return-application", "123", "456", "/tmp/out.pdf"], "file", "return_application"),
    (["business-return-decisions", "{}"], "action", "business_return_decisions"),
    (["return-create", "{}"], "action", "return_create"),
    (["return-cancel", "{}"], "action", "return_cancel"),

    # --- shipments ---
    (["shipments"], "promoted", "ym_shipments"),
    (["shipment", "123"], "action", "shipment"),
    (["shipments-search", "{}"], "action", "shipments_search"),
    (["shipment-update", "123", "{}"], "action", "shipment_update"),
    (["shipment-confirm", "123"], "action", "shipment_confirm"),
    (["shipment-orders", "123"], "action", "shipment_orders"),
    (["shipment-transfer", "123", "{}"], "action", "shipment_transfer"),
    (["shipment-act", "123", "/tmp/out.pdf"], "file", "shipment_act"),
    (["shipment-inbound-act", "123", "/tmp/out.pdf"], "file", "shipment_inbound_act"),
    (["shipment-waybill", "123", "/tmp/out.pdf"], "file", "shipment_waybill"),
    (["shipment-discrepancy-act", "123", "/tmp/out.pdf"], "file", "shipment_discrepancy_act"),
    (["shipment-pallets", "123"], "action", "shipment_pallets"),
    (["shipment-pallets-update", "123", "[]"], "action", "shipment_pallets_update"),
    (["shipment-pallet-labels", "123", "/tmp/out.pdf"], "file", "shipment_pallet_labels"),

    # --- feedbacks ---
    (["feedbacks"], "promoted", "ym_feedbacks"),
    (["feedback-skip", "[1,2]"], "action", "feedback_skip"),
    (["feedback-comments", "123"], "action", "feedback_comments"),
    (["feedback-comment-update", "{}"], "action", "feedback_comment_update"),
    (["feedback-comment-delete", "123"], "action", "feedback_comment_delete"),

    # --- questions ---
    (["questions"], "action", "questions"),
    (["question-answer", "{}"], "action", "question_answer"),
    (["question-update", "{}"], "action", "question_update"),

    # --- quality ---
    (["quality"], "action", "quality_rating"),
    (["quality-details"], "action", "quality_details"),

    # --- warehouses ---
    (["warehouses"], "action", "warehouses"),
    (["warehouse-status", "true"], "action", "warehouse_status"),
    (["all-warehouses"], "action", "all_warehouses"),

    # --- logistics ---
    (["logistics-points"], "action", "logistics_points"),
    (["reception-transfer-act", "/tmp/out.pdf"], "file", "reception_transfer_act"),

    # --- outlets ---
    (["outlets"], "action", "outlets"),
    (["outlet", "123"], "action", "outlet"),
    (["outlet-create", "{}"], "action", "outlet_create"),
    (["outlet-update", "123", "{}"], "action", "outlet_update"),
    (["outlet-delete", "123"], "action", "outlet_delete"),
    (["outlet-licenses"], "action", "outlet_licenses"),

    # --- delivery ---
    (["delivery-services"], "action", "delivery_services"),
    (["delivery-options", "{}"], "action", "delivery_options"),
    (["return-delivery-options", "{}"], "action", "return_delivery_options"),

    # --- regions ---
    (["regions"], "action", "regions"),
    (["region", "123"], "action", "region"),
    (["region-children", "123"], "action", "region_children"),

    # --- geo / categories ---
    (["countries"], "action", "countries"),
    (["categories"], "action", "categories"),
    (["category-params", "123"], "action", "category_params"),
    (["max-sale-quantum", "{}"], "action", "max_sale_quantum"),

    # --- tariffs ---
    (["tariffs", "[]"], "action", "tariffs"),

    # --- promos ---
    (["promos"], "action", "promos"),
    (["promo-offers", "cf_123"], "action", "promo_offers"),
    (["promo-offers-update", "{}"], "action", "promo_offers_update"),
    (["promo-offers-delete", "{}"], "action", "promo_offers_delete"),

    # --- bids ---
    (["bids"], "promoted", "ym_bids"),
    (["bids-update", "[]"], "action", "bids_update"),
    (["campaign-bids"], "action", "campaign_bids"),
    (["campaign-bids-update", "[]"], "action", "campaign_bids_update"),
    (["bid-recommendations"], "action", "bid_recommendations"),

    # --- chats ---
    (["chats"], "promoted", "ym_chats"),
    (["chat-history", "123"], "action", "chat_history"),
    (["chat-send", "123", "hello"], "action", "chat_send"),
    (["chat-new", "{}"], "action", "chat_new"),
    (["chat-file-send", "123", "/tmp/file.txt"], "action", "chat_file_send"),

    # --- reports ---
    (["report-status", "abc123"], "action", "report_status"),
    (["report-generate", "PRICES"], "promoted", "ym_report_generate"),
    (["report-barcodes", "{}"], "action", "report_barcodes"),

    # --- stats / supply ---
    (["order-stats"], "action", "order_stats"),
    (["supply-requests"], "action", "supply_requests"),
    (["supply-request-items"], "action", "supply_request_items"),
    (["supply-request-documents", "/tmp/out.pdf"], "file", "supply_request_documents"),
    (["sku-stats"], "action", "sku_stats"),

    # --- operations ---
    (["operations"], "action", "operations"),
]
# fmt: on


def test_cli_commands_count():
    """Ensure CLI_COMMANDS covers all 131 commands."""
    assert len(CLI_COMMANDS) == 131


@pytest.mark.parametrize("argv,call_type,call_arg", CLI_COMMANDS)
def test_cli_command(argv, call_type, call_arg):
    with patch("mcp_server_yandex_market_seller.cli.server") as mock_server:
        mock_server.execute_action.return_value = '{"status":"OK"}'
        mock_server.execute_file_action.return_value = '{"path":"/tmp/x","size":3}'
        # Mock promoted tools
        for name in ["ym_orders", "ym_order", "ym_order_status", "ym_offers",
                     "ym_stocks", "ym_stocks_update", "ym_prices", "ym_prices_update",
                     "ym_returns", "ym_shipments", "ym_feedbacks", "ym_chats",
                     "ym_bids", "ym_report_generate", "ym_campaigns"]:
            getattr(mock_server, name).return_value = '{"status":"OK"}'
        with patch("builtins.print"):
            main(argv)
        if call_type == "promoted":
            getattr(mock_server, call_arg).assert_called_once()
        elif call_type == "action":
            mock_server.execute_action.assert_called_once()
            assert mock_server.execute_action.call_args[0][0] == call_arg
        elif call_type == "file":
            mock_server.execute_file_action.assert_called_once()
            assert mock_server.execute_file_action.call_args[0][0] == call_arg
