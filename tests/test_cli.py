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


# (argv_list, expected_server_function_name)
# fmt: off
CLI_COMMANDS = [
    # --- campaigns / campaign ---
    (["campaigns"], "ym_campaigns"),
    (["campaign"], "ym_campaign"),
    (["campaign-settings"], "ym_campaign_settings"),
    (["campaign-settings-update", "{}"], "ym_campaign_settings_update"),
    (["business-settings"], "ym_business_settings"),
    (["business-settings-update", "{}"], "ym_business_settings_update"),

    # --- orders ---
    (["orders"], "ym_orders"),
    (["order", "123"], "ym_order"),
    (["order-items", "123"], "ym_order_items"),
    (["order-buyer", "123"], "ym_order_buyer"),
    (["order-tracking", "123"], "ym_order_tracking"),
    (["order-status", "123", "PROCESSING"], "ym_order_status"),
    (["order-status-batch", "{}"], "ym_order_status_batch"),
    (["order-labels", "123", "/tmp/out.pdf"], "ym_order_labels"),
    (["order-labels-data", "123"], "ym_order_labels_data"),
    (["order-box-label", "1", "2", "3", "/tmp/out.pdf"], "ym_order_box_label"),
    (["order-items-update", "123", "{}"], "ym_order_items_update"),
    (["order-boxes", "123"], "ym_order_boxes"),
    (["order-boxes-update", "123", "{}"], "ym_order_boxes_update"),
    (["order-shipment-boxes", "123", "456", "{}"], "ym_order_shipment_boxes"),
    (["order-cancel-accept", "123"], "ym_order_cancel_accept"),
    (["order-delivery-date", "123", "{}"], "ym_order_delivery_date"),
    (["order-tracking-update", "123", "{}"], "ym_order_tracking_update"),
    (["order-business-buyer", "123"], "ym_order_business_buyer"),
    (["order-verify-eac", "123", "ABC"], "ym_order_verify_eac"),
    (["order-storage-limit", "123"], "ym_order_storage_limit"),
    (["order-storage-limit-update", "123", "2025-01-01"], "ym_order_storage_limit_update"),
    (["order-deliver-digital", "123", "{}"], "ym_order_deliver_digital"),
    (["order-documents", "123"], "ym_order_documents"),
    (["order-document-create", "123", "{}"], "ym_order_document_create"),
    (["business-orders", "{}"], "ym_business_orders"),
    (["order-create", "{}"], "ym_order_create"),
    (["order-update-v1", "{}"], "ym_order_update_v1"),
    (["order-update-options", "{}"], "ym_order_update_options"),

    # --- offers ---
    (["offers"], "ym_offers"),
    (["offer-cards"], "ym_offer_cards"),
    (["offers-update", "{}"], "ym_offers_update"),
    (["offers-delete", "sku1,sku2"], "ym_offers_delete"),
    (["offers-archive", "sku1,sku2"], "ym_offers_archive"),
    (["generate-barcodes", "sku1,sku2"], "ym_generate_barcodes"),

    # --- prices ---
    (["prices"], "ym_prices"),
    (["prices-update", "{}"], "ym_prices_update"),
    (["price-quarantine"], "ym_price_quarantine"),
    (["price-quarantine-confirm", "sku1,sku2"], "ym_price_quarantine_confirm"),
    (["campaign-price-quarantine"], "ym_campaign_price_quarantine"),
    (["campaign-price-quarantine-confirm", "sku1,sku2"], "ym_campaign_price_quarantine_confirm"),

    # --- stocks ---
    (["stocks"], "ym_stocks"),
    (["stocks-update", "{}"], "ym_stocks_update"),

    # --- hidden / campaign offers ---
    (["hidden-offers"], "ym_hidden_offers"),
    (["campaign-offers"], "ym_campaign_offers"),
    (["unhide-offers", "sku1,sku2"], "ym_unhide_offers"),

    # --- offer cards / recommendations ---
    (["offer-cards-update", "{}"], "ym_offer_cards_update"),
    (["offer-recommendations"], "ym_offer_recommendations"),

    # --- returns ---
    (["returns"], "ym_returns"),
    (["return", "123", "456"], "ym_return"),
    (["return-decision", "123", "456"], "ym_return_decision"),
    (["return-decision-set", "123", "456", "{}"], "ym_return_decision_set"),
    (["return-decision-submit", "123", "456"], "ym_return_decision_submit"),
    (["return-application", "123", "456", "/tmp/out.pdf"], "ym_return_application"),
    (["business-return-decisions", "{}"], "ym_business_return_decisions"),
    (["return-create", "{}"], "ym_return_create"),
    (["return-cancel", "{}"], "ym_return_cancel"),

    # --- shipments ---
    (["shipments"], "ym_shipments"),
    (["shipment", "123"], "ym_shipment"),
    (["shipments-search", "{}"], "ym_shipments_search"),
    (["shipment-update", "123", "{}"], "ym_shipment_update"),
    (["shipment-confirm", "123"], "ym_shipment_confirm"),
    (["shipment-orders", "123"], "ym_shipment_orders"),
    (["shipment-transfer", "123", "{}"], "ym_shipment_transfer"),
    (["shipment-act", "123", "/tmp/out.pdf"], "ym_shipment_act"),
    (["shipment-inbound-act", "123", "/tmp/out.pdf"], "ym_shipment_inbound_act"),
    (["shipment-waybill", "123", "/tmp/out.pdf"], "ym_shipment_waybill"),
    (["shipment-discrepancy-act", "123", "/tmp/out.pdf"], "ym_shipment_discrepancy_act"),
    (["shipment-pallets", "123"], "ym_shipment_pallets"),
    (["shipment-pallets-update", "123", "{}"], "ym_shipment_pallets_update"),
    (["shipment-pallet-labels", "123", "/tmp/out.pdf"], "ym_shipment_pallet_labels"),

    # --- feedbacks ---
    (["feedbacks"], "ym_feedbacks"),
    (["feedback-skip", "{}"], "ym_feedback_skip"),
    (["feedback-comments", "123"], "ym_feedback_comments"),
    (["feedback-comment-update", "{}"], "ym_feedback_comment_update"),
    (["feedback-comment-delete", "123"], "ym_feedback_comment_delete"),

    # --- questions ---
    (["questions"], "ym_questions"),
    (["question-answer", "{}"], "ym_question_answer"),
    (["question-update", "{}"], "ym_question_update"),

    # --- quality ---
    (["quality"], "ym_quality_rating"),
    (["quality-details"], "ym_quality_details"),

    # --- warehouses ---
    (["warehouses"], "ym_warehouses"),
    (["warehouse-status", "true"], "ym_warehouse_status"),
    (["all-warehouses"], "ym_all_warehouses"),

    # --- logistics ---
    (["logistics-points"], "ym_logistics_points"),
    (["reception-transfer-act", "/tmp/out.pdf"], "ym_reception_transfer_act"),

    # --- outlets ---
    (["outlets"], "ym_outlets"),
    (["outlet", "123"], "ym_outlet"),
    (["outlet-create", "{}"], "ym_outlet_create"),
    (["outlet-update", "123", "{}"], "ym_outlet_update"),
    (["outlet-delete", "123"], "ym_outlet_delete"),
    (["outlet-licenses"], "ym_outlet_licenses"),

    # --- delivery ---
    (["delivery-services"], "ym_delivery_services"),
    (["delivery-options", "{}"], "ym_delivery_options"),
    (["return-delivery-options", "{}"], "ym_return_delivery_options"),

    # --- regions ---
    (["regions"], "ym_regions"),
    (["region", "123"], "ym_region"),
    (["region-children", "123"], "ym_region_children"),

    # --- geo / categories ---
    (["countries"], "ym_countries"),
    (["categories"], "ym_categories"),
    (["category-params", "123"], "ym_category_params"),
    (["max-sale-quantum", "{}"], "ym_max_sale_quantum"),

    # --- tariffs ---
    (["tariffs", "{}"], "ym_tariffs"),

    # --- promos ---
    (["promos"], "ym_promos"),
    (["promo-offers", "cf_123"], "ym_promo_offers"),
    (["promo-offers-update", "{}"], "ym_promo_offers_update"),
    (["promo-offers-delete", "{}"], "ym_promo_offers_delete"),

    # --- bids ---
    (["bids"], "ym_bids"),
    (["bids-update", "{}"], "ym_bids_update"),
    (["campaign-bids"], "ym_campaign_bids"),
    (["campaign-bids-update", "{}"], "ym_campaign_bids_update"),
    (["bid-recommendations"], "ym_bid_recommendations"),

    # --- chats ---
    (["chats"], "ym_chats"),
    (["chat-history", "123"], "ym_chat_history"),
    (["chat-send", "123", "hello"], "ym_chat_send"),
    (["chat-new", "{}"], "ym_chat_new"),
    (["chat-file-send", "123", "/tmp/file.txt"], "ym_chat_file_send"),

    # --- reports ---
    (["report-status", "abc123"], "ym_report_status"),
    (["report-generate", "PRICES"], "ym_report_generate"),
    (["report-barcodes", "{}"], "ym_report_barcodes"),

    # --- stats / supply ---
    (["order-stats"], "ym_order_stats"),
    (["supply-requests"], "ym_supply_requests"),
    (["supply-request-items"], "ym_supply_request_items"),
    (["supply-request-documents", "/tmp/out.pdf"], "ym_supply_request_documents"),
    (["sku-stats"], "ym_sku_stats"),

    # --- operations ---
    (["operations"], "ym_operations"),
]
# fmt: on


def test_cli_commands_count():
    """Ensure CLI_COMMANDS covers all 131 commands."""
    assert len(CLI_COMMANDS) == 131


@pytest.mark.parametrize("argv,expected_func", CLI_COMMANDS)
def test_cli_command(argv, expected_func):
    with patch("mcp_server_yandex_market_seller.cli.server") as mock_server:
        getattr(mock_server, expected_func).return_value = '{"status":"OK"}'
        with patch("builtins.print"):
            main(argv)
        getattr(mock_server, expected_func).assert_called_once()
