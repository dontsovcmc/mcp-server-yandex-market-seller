"""Action catalog — maps 131 actions to YandexMarketAPI methods."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Callable

from .models import (
    CategoryIdParams,
    ChatFileSendParams,
    ChatHistoryParams,
    ChatSendParams,
    CommentIdParams,
    FeedbackIdParams,
    GenericPayload,
    OfferIdsParams,
    OffersArchiveParams,
    OffersListParams,
    OrderBoxesUpdateParams,
    OrderBoxLabelParams,
    OrderDeliverDigitalParams,
    OrderDeliveryDateParams,
    OrderDocumentCreateParams,
    OrderIdParams,
    OrderShipmentBoxesParams,
    OrdersListParams,
    OrderStatsParams,
    OrderStatusParams,
    OrderStorageLimitParams,
    OrderTrackingUpdateParams,
    OrderVerifyEacParams,
    OutletIdParams,
    OutletUpdateParams,
    PaginatedParams,
    PromoOffersParams,
    QualityRatingParams,
    RegionChildrenParams,
    RegionIdParams,
    RegionsParams,
    ReportGenerateParams,
    ReportStatusParams,
    ReturnDecisionSetParams,
    ReturnParams,
    ReturnsListParams,
    ShipmentIdParams,
    ShipmentPalletsUpdateParams,
    ShipmentPayloadParams,
    TariffsParams,
    WarehouseStatusParams,
    OrderItemsUpdateParams,
)

if TYPE_CHECKING:
    from pydantic import BaseModel


@dataclass(frozen=True, slots=True)
class Action:
    id: str
    domain: str
    description: str
    params_model: type[BaseModel] | None
    id_type: str  # "campaign" | "business" | "none"
    call_fn: Callable[[Any, int | None, dict], Any]
    is_destructive: bool = False
    is_file: bool = False
    keywords: list[str] = field(default_factory=list)


def _safe_path(path: str) -> str:
    """Validate input path for chat file send."""
    import tempfile
    resolved = os.path.realpath(path)
    home = os.path.realpath(os.path.expanduser("~"))
    tmp_dirs = {os.path.realpath(tempfile.gettempdir())}
    if os.path.isdir("/tmp"):
        tmp_dirs.add(os.path.realpath("/tmp"))
    is_under_home = resolved.startswith(home + os.sep)
    is_under_tmp = any(resolved.startswith(d + os.sep) for d in tmp_dirs)
    if not (is_under_home or is_under_tmp):
        raise ValueError(f"Path must be under home or temp directory: {path}")
    return resolved


# ── Action list ────────────────────────────────────────────────────

_ACTIONS_LIST: list[Action] = [
    # ── Campaigns & Settings ───────────────────────────────────────
    Action(
        id="campaigns", domain="campaigns",
        description="List all campaigns (shops) in the account",
        params_model=None, id_type="none",
        call_fn=lambda api, _, p: api.get_campaigns(),
        keywords=["campaigns", "shops", "list"],
    ),
    Action(
        id="campaign", domain="campaigns",
        description="Get single campaign details by ID",
        params_model=None, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_campaign(cid),
        keywords=["campaign", "shop", "details"],
    ),
    Action(
        id="campaign_settings", domain="campaigns",
        description="Get campaign settings",
        params_model=None, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_campaign_settings(cid),
        keywords=["campaign", "settings"],
    ),
    Action(
        id="campaign_settings_update", domain="campaigns",
        description="Update campaign settings",
        params_model=GenericPayload, id_type="campaign",
        call_fn=lambda api, cid, p: api.update_campaign_settings(cid, p),
        keywords=["campaign", "settings", "update"],
    ),
    Action(
        id="business_settings", domain="campaigns",
        description="Get business settings",
        params_model=None, id_type="business",
        call_fn=lambda api, bid, p: api.get_business_settings(bid),
        keywords=["business", "settings"],
    ),
    Action(
        id="business_settings_update", domain="campaigns",
        description="Update business settings",
        params_model=GenericPayload, id_type="business",
        call_fn=lambda api, bid, p: api.update_business_settings(bid, p),
        keywords=["business", "settings", "update"],
    ),

    # ── Orders v2 ──────────────────────────────────────────────────
    Action(
        id="orders", domain="orders",
        description="List orders with optional status filter",
        params_model=OrdersListParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_orders(
            cid, status=p.get("status", ""),
            page=p.get("page", 1), page_size=p.get("page_size", 50)),
        keywords=["orders", "list", "status", "filter"],
    ),
    Action(
        id="order", domain="orders",
        description="Get full order details: items, delivery, buyer info, status",
        params_model=OrderIdParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_order(cid, p["order_id"]),
        keywords=["order", "details", "info"],
    ),
    Action(
        id="order_status", domain="orders",
        description="Update order status. Typical flow: PROCESSING → DELIVERY → DELIVERED",
        params_model=OrderStatusParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.update_order_status(
            cid, p["order_id"], p["status"], p.get("substatus", "")),
        keywords=["order", "status", "update", "change"],
    ),
    Action(
        id="order_status_batch", domain="orders",
        description="Batch update order statuses",
        params_model=GenericPayload, id_type="campaign",
        call_fn=lambda api, cid, p: api.batch_update_order_statuses(cid, p.get("orders", [])),
        keywords=["order", "status", "batch", "bulk"],
    ),
    Action(
        id="order_labels", domain="orders",
        description="Download shipping labels as PDF file",
        params_model=OrderIdParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_order_labels(cid, p["order_id"]),
        is_file=True,
        keywords=["order", "labels", "pdf", "download"],
    ),
    Action(
        id="order_labels_data", domain="orders",
        description="Get label data as JSON (parcel dimensions, tracking)",
        params_model=OrderIdParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_order_labels_data(cid, p["order_id"]),
        keywords=["order", "labels", "data"],
    ),
    Action(
        id="order_box_label", domain="orders",
        description="Download box label (PDF)",
        params_model=OrderBoxLabelParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_order_box_label(
            cid, p["order_id"], p["shipment_id"], p["box_id"]),
        is_file=True,
        keywords=["order", "box", "label", "pdf"],
    ),
    Action(
        id="order_items", domain="orders",
        description="Get order line items",
        params_model=OrderIdParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_order_items(cid, p["order_id"]),
        keywords=["order", "items", "products"],
    ),
    Action(
        id="order_items_update", domain="orders",
        description="Update order line items",
        params_model=OrderItemsUpdateParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.update_order_items(cid, p["order_id"], p["items"]),
        keywords=["order", "items", "update"],
    ),
    Action(
        id="order_boxes", domain="orders",
        description="Get order boxes",
        params_model=OrderIdParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_order_boxes(cid, p["order_id"]),
        keywords=["order", "boxes"],
    ),
    Action(
        id="order_boxes_update", domain="orders",
        description="Update order boxes",
        params_model=OrderBoxesUpdateParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.update_order_boxes(cid, p["order_id"], p["boxes"]),
        keywords=["order", "boxes", "update"],
    ),
    Action(
        id="order_shipment_boxes", domain="orders",
        description="Set shipment boxes for an order",
        params_model=OrderShipmentBoxesParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.set_shipment_boxes(
            cid, p["order_id"], p["shipment_id"], p["boxes"]),
        keywords=["order", "shipment", "boxes"],
    ),
    Action(
        id="order_cancel_accept", domain="orders",
        description="Accept order cancellation",
        params_model=OrderIdParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.accept_order_cancellation(cid, p["order_id"]),
        is_destructive=True,
        keywords=["order", "cancel", "accept"],
    ),
    Action(
        id="order_delivery_date", domain="orders",
        description="Set delivery date for an order",
        params_model=OrderDeliveryDateParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.set_order_delivery_date(
            cid, p["order_id"], p["dates"]),
        keywords=["order", "delivery", "date"],
    ),
    Action(
        id="order_tracking", domain="orders",
        description="Get order tracking info",
        params_model=OrderIdParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_order_tracking(cid, p["order_id"]),
        keywords=["order", "tracking", "track"],
    ),
    Action(
        id="order_tracking_update", domain="orders",
        description="Set tracking numbers for an order",
        params_model=OrderTrackingUpdateParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.set_order_tracking(
            cid, p["order_id"], p["tracks"]),
        keywords=["order", "tracking", "update"],
    ),
    Action(
        id="order_buyer", domain="orders",
        description="Get buyer info for an order",
        params_model=OrderIdParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_order_buyer(cid, p["order_id"]),
        keywords=["order", "buyer", "customer"],
    ),
    Action(
        id="order_business_buyer", domain="orders",
        description="Get business buyer (legal entity) info",
        params_model=OrderIdParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_order_business_buyer(cid, p["order_id"]),
        keywords=["order", "business", "buyer", "legal"],
    ),
    Action(
        id="order_verify_eac", domain="orders",
        description="Verify EAC code for an order",
        params_model=OrderVerifyEacParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.verify_order_eac(cid, p["order_id"], p["code"]),
        keywords=["order", "eac", "verify", "code"],
    ),
    Action(
        id="order_storage_limit", domain="orders",
        description="Get order storage limit",
        params_model=OrderIdParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_order_storage_limit(cid, p["order_id"]),
        keywords=["order", "storage", "limit"],
    ),
    Action(
        id="order_storage_limit_update", domain="orders",
        description="Set order storage limit date",
        params_model=OrderStorageLimitParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.set_order_storage_limit(
            cid, p["order_id"], p["date"]),
        keywords=["order", "storage", "limit", "update"],
    ),
    Action(
        id="order_deliver_digital", domain="orders",
        description="Deliver digital goods for an order",
        params_model=OrderDeliverDigitalParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.deliver_digital_goods(
            cid, p["order_id"], p["items"]),
        keywords=["order", "digital", "deliver"],
    ),
    Action(
        id="order_documents", domain="orders",
        description="Get order documents",
        params_model=OrderIdParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_order_documents(cid, p["order_id"]),
        keywords=["order", "documents"],
    ),
    Action(
        id="order_document_create", domain="orders",
        description="Create order document",
        params_model=OrderDocumentCreateParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.create_order_document(
            cid, p["order_id"], p["document"]),
        keywords=["order", "document", "create"],
    ),

    # ── Orders v1 ──────────────────────────────────────────────────
    Action(
        id="business_orders", domain="orders",
        description="Get business-level orders (v1)",
        params_model=GenericPayload, id_type="business",
        call_fn=lambda api, bid, p: api.get_business_orders(bid, p),
        keywords=["business", "orders"],
    ),
    Action(
        id="order_create", domain="orders",
        description="Create order (v1)",
        params_model=GenericPayload, id_type="campaign",
        call_fn=lambda api, cid, p: api.create_order_v1(cid, p),
        keywords=["order", "create", "new"],
    ),
    Action(
        id="order_update_v1", domain="orders",
        description="Update order (v1)",
        params_model=GenericPayload, id_type="campaign",
        call_fn=lambda api, cid, p: api.update_order_v1(cid, p),
        keywords=["order", "update"],
    ),
    Action(
        id="order_update_options", domain="orders",
        description="Update order options (v1)",
        params_model=GenericPayload, id_type="campaign",
        call_fn=lambda api, cid, p: api.update_order_options(cid, p),
        keywords=["order", "update", "options"],
    ),

    # ── Returns ────────────────────────────────────────────────────
    Action(
        id="returns", domain="returns",
        description="List returns for a campaign",
        params_model=ReturnsListParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_returns(
            cid, page=p.get("page", 1), page_size=p.get("page_size", 50)),
        keywords=["returns", "list", "refund"],
    ),
    Action(
        id="return", domain="returns",
        description="Get return details",
        params_model=ReturnParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_return(cid, p["order_id"], p["return_id"]),
        keywords=["return", "details"],
    ),
    Action(
        id="return_decision", domain="returns",
        description="Get return decision",
        params_model=ReturnParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_return_decision(
            cid, p["order_id"], p["return_id"]),
        keywords=["return", "decision"],
    ),
    Action(
        id="return_decision_set", domain="returns",
        description="Set return decision",
        params_model=ReturnDecisionSetParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.set_return_decision(
            cid, p["order_id"], p["return_id"], p["decision"]),
        keywords=["return", "decision", "set"],
    ),
    Action(
        id="return_decision_submit", domain="returns",
        description="Submit return decision",
        params_model=ReturnParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.submit_return_decision(
            cid, p["order_id"], p["return_id"]),
        keywords=["return", "decision", "submit", "confirm"],
    ),
    Action(
        id="return_application", domain="returns",
        description="Download return application (PDF)",
        params_model=ReturnParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_return_application(
            cid, p["order_id"], p["return_id"]),
        is_file=True,
        keywords=["return", "application", "pdf", "download"],
    ),
    Action(
        id="business_return_decisions", domain="returns",
        description="Get business return decisions (v1)",
        params_model=GenericPayload, id_type="business",
        call_fn=lambda api, bid, p: api.get_business_return_decisions(bid, p),
        keywords=["business", "return", "decisions"],
    ),
    Action(
        id="return_create", domain="returns",
        description="Create return (v1)",
        params_model=GenericPayload, id_type="campaign",
        call_fn=lambda api, cid, p: api.create_return_v1(cid, p),
        keywords=["return", "create"],
    ),
    Action(
        id="return_cancel", domain="returns",
        description="Cancel return (v1)",
        params_model=GenericPayload, id_type="campaign",
        call_fn=lambda api, cid, p: api.cancel_return_v1(cid, p),
        is_destructive=True,
        keywords=["return", "cancel"],
    ),

    # ── Shipments ──────────────────────────────────────────────────
    Action(
        id="shipments", domain="shipments",
        description="List first-mile shipments",
        params_model=None, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_shipments(cid),
        keywords=["shipments", "list", "first-mile"],
    ),
    Action(
        id="shipments_search", domain="shipments",
        description="Search shipments with filters",
        params_model=GenericPayload, id_type="campaign",
        call_fn=lambda api, cid, p: api.search_shipments(cid, p),
        keywords=["shipments", "search", "filter"],
    ),
    Action(
        id="shipment", domain="shipments",
        description="Get shipment details",
        params_model=ShipmentIdParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_shipment(cid, p["shipment_id"]),
        keywords=["shipment", "details"],
    ),
    Action(
        id="shipment_update", domain="shipments",
        description="Update shipment",
        params_model=ShipmentPayloadParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.update_shipment(
            cid, p["shipment_id"], p["payload"]),
        keywords=["shipment", "update"],
    ),
    Action(
        id="shipment_confirm", domain="shipments",
        description="Confirm shipment",
        params_model=ShipmentIdParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.confirm_shipment(cid, p["shipment_id"]),
        keywords=["shipment", "confirm"],
    ),
    Action(
        id="shipment_orders", domain="shipments",
        description="Get orders in shipment",
        params_model=ShipmentIdParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_shipment_orders(cid, p["shipment_id"]),
        keywords=["shipment", "orders"],
    ),
    Action(
        id="shipment_transfer", domain="shipments",
        description="Transfer orders to shipment",
        params_model=ShipmentPayloadParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.transfer_shipment_orders(
            cid, p["shipment_id"], p["payload"]),
        keywords=["shipment", "transfer", "orders"],
    ),
    Action(
        id="shipment_act", domain="shipments",
        description="Download shipment act (PDF)",
        params_model=ShipmentIdParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_shipment_act(cid, p["shipment_id"]),
        is_file=True,
        keywords=["shipment", "act", "pdf", "download"],
    ),
    Action(
        id="shipment_inbound_act", domain="shipments",
        description="Download inbound act (PDF)",
        params_model=ShipmentIdParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_shipment_inbound_act(cid, p["shipment_id"]),
        is_file=True,
        keywords=["shipment", "inbound", "act", "pdf"],
    ),
    Action(
        id="shipment_waybill", domain="shipments",
        description="Download transportation waybill (PDF)",
        params_model=ShipmentIdParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_shipment_waybill(cid, p["shipment_id"]),
        is_file=True,
        keywords=["shipment", "waybill", "pdf"],
    ),
    Action(
        id="shipment_discrepancy_act", domain="shipments",
        description="Download discrepancy act (PDF)",
        params_model=ShipmentIdParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_shipment_discrepancy_act(
            cid, p["shipment_id"]),
        is_file=True,
        keywords=["shipment", "discrepancy", "act", "pdf"],
    ),
    Action(
        id="shipment_pallets", domain="shipments",
        description="Get shipment pallets",
        params_model=ShipmentIdParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_shipment_pallets(cid, p["shipment_id"]),
        keywords=["shipment", "pallets"],
    ),
    Action(
        id="shipment_pallets_update", domain="shipments",
        description="Set shipment pallets",
        params_model=ShipmentPalletsUpdateParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.set_shipment_pallets(
            cid, p["shipment_id"], p["pallets"]),
        keywords=["shipment", "pallets", "update"],
    ),
    Action(
        id="shipment_pallet_labels", domain="shipments",
        description="Download pallet labels (PDF)",
        params_model=ShipmentIdParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_shipment_pallet_labels(
            cid, p["shipment_id"]),
        is_file=True,
        keywords=["shipment", "pallet", "labels", "pdf"],
    ),

    # ── Warehouses ─────────────────────────────────────────────────
    Action(
        id="warehouses", domain="warehouses",
        description="Get business warehouses",
        params_model=None, id_type="business",
        call_fn=lambda api, bid, p: api.get_warehouses(bid),
        keywords=["warehouses", "list"],
    ),
    Action(
        id="all_warehouses", domain="warehouses",
        description="Get all Yandex Market warehouses",
        params_model=None, id_type="none",
        call_fn=lambda api, _, p: api.get_all_warehouses(),
        keywords=["warehouses", "all", "market"],
    ),
    Action(
        id="warehouse_status", domain="warehouses",
        description="Enable/disable warehouse",
        params_model=WarehouseStatusParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.set_warehouse_status(cid, p["enabled"]),
        keywords=["warehouse", "status", "enable", "disable"],
    ),
    Action(
        id="reception_transfer_act", domain="warehouses",
        description="Download reception-transfer act (PDF)",
        params_model=None, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_reception_transfer_act(cid),
        is_file=True,
        keywords=["reception", "transfer", "act", "pdf"],
    ),

    # ── Offers ─────────────────────────────────────────────────────
    Action(
        id="offers", domain="offers",
        description="List products (offer mappings) at business level",
        params_model=OffersListParams, id_type="business",
        call_fn=lambda api, bid, p: api.get_offer_mappings(
            bid, offer_ids=p.get("offer_ids"),
            page_token=p.get("page_token", ""), limit=p.get("limit", 200)),
        keywords=["offers", "products", "list", "mappings"],
    ),
    Action(
        id="offers_update", domain="offers",
        description="Create or update product descriptions (offer mappings)",
        params_model=GenericPayload, id_type="business",
        call_fn=lambda api, bid, p: api.update_offer_mappings(bid, p.get("offerMappings", [])),
        keywords=["offers", "update", "create"],
    ),
    Action(
        id="offers_delete", domain="offers",
        description="Permanently delete products (IRREVERSIBLE)",
        params_model=OfferIdsParams, id_type="business",
        call_fn=lambda api, bid, p: api.delete_offer_mappings(bid, p["offer_ids"]),
        is_destructive=True,
        keywords=["offers", "delete", "remove"],
    ),
    Action(
        id="offers_archive", domain="offers",
        description="Archive or unarchive products",
        params_model=OffersArchiveParams, id_type="business",
        call_fn=lambda api, bid, p: (
            api.archive_offer_mappings(bid, p["offer_ids"])
            if p.get("archive", True)
            else api.unarchive_offer_mappings(bid, p["offer_ids"])),
        is_destructive=True,
        keywords=["offers", "archive", "unarchive", "hide"],
    ),
    Action(
        id="generate_barcodes", domain="offers",
        description="Generate barcodes for offers",
        params_model=OfferIdsParams, id_type="business",
        call_fn=lambda api, bid, p: api.generate_barcodes(bid, p["offer_ids"]),
        keywords=["barcodes", "generate", "offers"],
    ),
    Action(
        id="campaign_offers", domain="offers",
        description="Get campaign offers with prices and stocks",
        params_model=PaginatedParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_campaign_offers(
            cid, page_token=p.get("page_token", ""), limit=p.get("limit", 200)),
        keywords=["campaign", "offers", "prices", "stocks"],
    ),
    Action(
        id="hidden_offers", domain="offers",
        description="Get offers hidden from sale",
        params_model=PaginatedParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_hidden_offers(
            cid, page_token=p.get("page_token", ""), limit=p.get("limit", 200)),
        keywords=["hidden", "offers"],
    ),
    Action(
        id="unhide_offers", domain="offers",
        description="Unhide offers (restore visibility)",
        params_model=OfferIdsParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.unhide_offers(cid, p["offer_ids"]),
        keywords=["unhide", "offers", "show"],
    ),

    # ── Offer Cards ────────────────────────────────────────────────
    Action(
        id="offer_cards", domain="offer_cards",
        description="Get offer cards",
        params_model=OffersListParams, id_type="business",
        call_fn=lambda api, bid, p: api.get_offer_cards(
            bid, offer_ids=p.get("offer_ids"),
            page_token=p.get("page_token", ""), limit=p.get("limit", 200)),
        keywords=["offer", "cards", "content"],
    ),
    Action(
        id="offer_cards_update", domain="offer_cards",
        description="Update offer cards",
        params_model=GenericPayload, id_type="business",
        call_fn=lambda api, bid, p: api.update_offer_cards(bid, p.get("offerCards", [])),
        keywords=["offer", "cards", "update"],
    ),
    Action(
        id="offer_recommendations", domain="offer_cards",
        description="Get offer recommendations",
        params_model=GenericPayload, id_type="business",
        call_fn=lambda api, bid, p: api.get_offer_recommendations(bid, p or None),
        keywords=["offer", "recommendations"],
    ),

    # ── Prices ─────────────────────────────────────────────────────
    Action(
        id="prices", domain="prices",
        description="Get product prices at business level",
        params_model=OffersListParams, id_type="business",
        call_fn=lambda api, bid, p: api.get_business_offer_prices(
            bid, offer_ids=p.get("offer_ids"),
            page_token=p.get("page_token", ""), limit=p.get("limit", 200)),
        keywords=["prices", "list", "cost"],
    ),
    Action(
        id="prices_update", domain="prices",
        description="Update product prices at business level",
        params_model=GenericPayload, id_type="business",
        call_fn=lambda api, bid, p: api.update_business_offer_prices(
            bid, p.get("offers", [])),
        keywords=["prices", "update", "change"],
    ),
    Action(
        id="price_quarantine", domain="prices",
        description="Get offers in price quarantine",
        params_model=GenericPayload, id_type="business",
        call_fn=lambda api, bid, p: api.get_price_quarantine(bid, p or None),
        keywords=["price", "quarantine"],
    ),
    Action(
        id="price_quarantine_confirm", domain="prices",
        description="Confirm quarantine prices",
        params_model=OfferIdsParams, id_type="business",
        call_fn=lambda api, bid, p: api.confirm_price_quarantine(bid, p["offer_ids"]),
        keywords=["price", "quarantine", "confirm"],
    ),
    Action(
        id="campaign_price_quarantine", domain="prices",
        description="Get campaign price quarantine",
        params_model=GenericPayload, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_campaign_price_quarantine(cid, p or None),
        keywords=["campaign", "price", "quarantine"],
    ),
    Action(
        id="campaign_price_quarantine_confirm", domain="prices",
        description="Confirm campaign quarantine prices",
        params_model=OfferIdsParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.confirm_campaign_price_quarantine(
            cid, p["offer_ids"]),
        keywords=["campaign", "price", "quarantine", "confirm"],
    ),

    # ── Stocks ─────────────────────────────────────────────────────
    Action(
        id="stocks", domain="stocks",
        description="Get product stocks for a campaign",
        params_model=PaginatedParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_stocks(
            cid, page_token=p.get("page_token", ""), limit=p.get("limit", 200)),
        keywords=["stocks", "inventory", "list"],
    ),
    Action(
        id="stocks_update", domain="stocks",
        description="Update product stocks",
        params_model=GenericPayload, id_type="campaign",
        call_fn=lambda api, cid, p: api.update_stocks(cid, p.get("skus", [])),
        keywords=["stocks", "update", "inventory"],
    ),

    # ── Delivery ───────────────────────────────────────────────────
    Action(
        id="delivery_services", domain="delivery",
        description="List delivery services",
        params_model=None, id_type="none",
        call_fn=lambda api, _, p: api.get_delivery_services(),
        keywords=["delivery", "services", "list"],
    ),
    Action(
        id="delivery_options", domain="delivery",
        description="Get delivery options",
        params_model=GenericPayload, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_delivery_options(cid, p),
        keywords=["delivery", "options"],
    ),
    Action(
        id="return_delivery_options", domain="delivery",
        description="Get return delivery options",
        params_model=GenericPayload, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_return_delivery_options(cid, p),
        keywords=["return", "delivery", "options"],
    ),

    # ── Logistics ──────────────────────────────────────────────────
    Action(
        id="logistics_points", domain="logistics",
        description="Get logistics/drop-off points",
        params_model=GenericPayload, id_type="business",
        call_fn=lambda api, bid, p: api.get_logistics_points(bid, p or None),
        keywords=["logistics", "points", "drop-off"],
    ),

    # ── Feedbacks ──────────────────────────────────────────────────
    Action(
        id="feedbacks", domain="feedbacks",
        description="Get product reviews/feedbacks",
        params_model=PaginatedParams, id_type="business",
        call_fn=lambda api, bid, p: api.get_feedbacks(
            bid, page_token=p.get("page_token", ""), limit=p.get("limit", 200)),
        keywords=["feedbacks", "reviews", "list"],
    ),
    Action(
        id="feedback_skip", domain="feedbacks",
        description="Skip feedback reaction",
        params_model=GenericPayload, id_type="business",
        call_fn=lambda api, bid, p: api.skip_feedback_reaction(
            bid, p.get("feedbackIds", [])),
        keywords=["feedback", "skip"],
    ),
    Action(
        id="feedback_comments", domain="feedbacks",
        description="Get feedback comments",
        params_model=FeedbackIdParams, id_type="business",
        call_fn=lambda api, bid, p: api.get_feedback_comments(bid, p["feedback_id"]),
        keywords=["feedback", "comments"],
    ),
    Action(
        id="feedback_comment_update", domain="feedbacks",
        description="Update feedback comment",
        params_model=GenericPayload, id_type="business",
        call_fn=lambda api, bid, p: api.update_feedback_comment(bid, p),
        keywords=["feedback", "comment", "update"],
    ),
    Action(
        id="feedback_comment_delete", domain="feedbacks",
        description="Delete feedback comment",
        params_model=CommentIdParams, id_type="business",
        call_fn=lambda api, bid, p: api.delete_feedback_comment(bid, p["comment_id"]),
        is_destructive=True,
        keywords=["feedback", "comment", "delete"],
    ),

    # ── Questions ──────────────────────────────────────────────────
    Action(
        id="questions", domain="questions",
        description="Get product questions from buyers",
        params_model=GenericPayload, id_type="business",
        call_fn=lambda api, bid, p: api.get_questions(bid, p or None),
        keywords=["questions", "list", "buyers"],
    ),
    Action(
        id="question_answer", domain="questions",
        description="Answer a product question",
        params_model=GenericPayload, id_type="business",
        call_fn=lambda api, bid, p: api.answer_question(bid, p),
        keywords=["question", "answer", "reply"],
    ),
    Action(
        id="question_update", domain="questions",
        description="Update an answer to a question",
        params_model=GenericPayload, id_type="business",
        call_fn=lambda api, bid, p: api.update_question_answer(bid, p),
        keywords=["question", "answer", "update"],
    ),

    # ── Quality ────────────────────────────────────────────────────
    Action(
        id="quality_rating", domain="quality",
        description="Get quality rating for campaigns",
        params_model=QualityRatingParams, id_type="business",
        call_fn=lambda api, bid, p: api.get_quality_ratings(
            bid, campaign_ids=[p["campaign_id"]] if p.get("campaign_id") else None),
        keywords=["quality", "rating"],
    ),
    Action(
        id="quality_details", domain="quality",
        description="Get quality rating details",
        params_model=None, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_quality_details(cid),
        keywords=["quality", "details"],
    ),

    # ── Promos ─────────────────────────────────────────────────────
    Action(
        id="promos", domain="promos",
        description="Get active promotions",
        params_model=None, id_type="business",
        call_fn=lambda api, bid, p: api.get_promos(bid),
        keywords=["promos", "promotions", "list"],
    ),
    Action(
        id="promo_offers", domain="promos",
        description="Get offers in a promotion",
        params_model=PromoOffersParams, id_type="business",
        call_fn=lambda api, bid, p: api.get_promo_offers(
            bid, p["promo_id"], p.get("payload") or None),
        keywords=["promo", "offers"],
    ),
    Action(
        id="promo_offers_update", domain="promos",
        description="Update promo offers",
        params_model=GenericPayload, id_type="business",
        call_fn=lambda api, bid, p: api.update_promo_offers(bid, p),
        keywords=["promo", "offers", "update"],
    ),
    Action(
        id="promo_offers_delete", domain="promos",
        description="Delete promo offers",
        params_model=GenericPayload, id_type="business",
        call_fn=lambda api, bid, p: api.delete_promo_offers(bid, p),
        is_destructive=True,
        keywords=["promo", "offers", "delete"],
    ),

    # ── Bids ───────────────────────────────────────────────────────
    Action(
        id="bids", domain="bids",
        description="Get current bids at business level",
        params_model=OffersListParams, id_type="business",
        call_fn=lambda api, bid, p: api.get_bids(
            bid, offer_ids=p.get("offer_ids"),
            page_token=p.get("page_token", ""), limit=p.get("limit", 200)),
        keywords=["bids", "list"],
    ),
    Action(
        id="bids_update", domain="bids",
        description="Update bids (business)",
        params_model=GenericPayload, id_type="business",
        call_fn=lambda api, bid, p: api.update_bids(bid, p.get("bids", [])),
        keywords=["bids", "update"],
    ),
    Action(
        id="campaign_bids", domain="bids",
        description="Get bids (campaign level)",
        params_model=OffersListParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_campaign_bids(
            cid, offer_ids=p.get("offer_ids"),
            page_token=p.get("page_token", ""), limit=p.get("limit", 200)),
        keywords=["campaign", "bids"],
    ),
    Action(
        id="campaign_bids_update", domain="bids",
        description="Update bids (campaign level)",
        params_model=GenericPayload, id_type="campaign",
        call_fn=lambda api, cid, p: api.update_campaign_bids(cid, p.get("bids", [])),
        keywords=["campaign", "bids", "update"],
    ),
    Action(
        id="bid_recommendations", domain="bids",
        description="Get bid recommendations",
        params_model=GenericPayload, id_type="business",
        call_fn=lambda api, bid, p: api.get_bid_recommendations(bid, p or None),
        keywords=["bids", "recommendations"],
    ),

    # ── Outlets ────────────────────────────────────────────────────
    Action(
        id="outlets", domain="outlets",
        description="List outlets (pickup points)",
        params_model=None, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_outlets(cid),
        keywords=["outlets", "pickup", "points", "list"],
    ),
    Action(
        id="outlet", domain="outlets",
        description="Get outlet details",
        params_model=OutletIdParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_outlet(cid, p["outlet_id"]),
        keywords=["outlet", "details"],
    ),
    Action(
        id="outlet_create", domain="outlets",
        description="Create outlet",
        params_model=GenericPayload, id_type="campaign",
        call_fn=lambda api, cid, p: api.create_outlet(cid, p),
        keywords=["outlet", "create", "new"],
    ),
    Action(
        id="outlet_update", domain="outlets",
        description="Update outlet",
        params_model=OutletUpdateParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.update_outlet(cid, p["outlet_id"], p["outlet"]),
        keywords=["outlet", "update"],
    ),
    Action(
        id="outlet_delete", domain="outlets",
        description="Delete outlet",
        params_model=OutletIdParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.delete_outlet(cid, p["outlet_id"]),
        is_destructive=True,
        keywords=["outlet", "delete"],
    ),
    Action(
        id="outlet_licenses", domain="outlets",
        description="Get outlet licenses",
        params_model=None, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_outlet_licenses(cid),
        keywords=["outlet", "licenses"],
    ),

    # ── Geo ────────────────────────────────────────────────────────
    Action(
        id="regions", domain="geo",
        description="Search regions",
        params_model=RegionsParams, id_type="none",
        call_fn=lambda api, _, p: api.get_regions(
            name=p.get("name", ""), page=p.get("page", 1)),
        keywords=["regions", "search"],
    ),
    Action(
        id="region", domain="geo",
        description="Get region by ID",
        params_model=RegionIdParams, id_type="none",
        call_fn=lambda api, _, p: api.get_region(p["region_id"]),
        keywords=["region", "details"],
    ),
    Action(
        id="region_children", domain="geo",
        description="Get child regions",
        params_model=RegionChildrenParams, id_type="none",
        call_fn=lambda api, _, p: api.get_region_children(
            p["region_id"], page=p.get("page", 1)),
        keywords=["region", "children"],
    ),
    Action(
        id="countries", domain="geo",
        description="Get countries list",
        params_model=None, id_type="none",
        call_fn=lambda api, _, p: api.get_countries(),
        keywords=["countries", "list"],
    ),

    # ── Categories ─────────────────────────────────────────────────
    Action(
        id="categories", domain="categories",
        description="Get category tree",
        params_model=None, id_type="none",
        call_fn=lambda api, _, p: api.get_categories_tree(),
        keywords=["categories", "tree", "list"],
    ),
    Action(
        id="category_params", domain="categories",
        description="Get category parameters",
        params_model=CategoryIdParams, id_type="none",
        call_fn=lambda api, _, p: api.get_category_parameters(p["category_id"]),
        keywords=["category", "parameters"],
    ),
    Action(
        id="max_sale_quantum", domain="categories",
        description="Get max sale quantum for categories",
        params_model=GenericPayload, id_type="none",
        call_fn=lambda api, _, p: api.get_max_sale_quantum(p),
        keywords=["max", "sale", "quantum", "categories"],
    ),

    # ── Tariffs ────────────────────────────────────────────────────
    Action(
        id="tariffs", domain="tariffs",
        description="Calculate marketplace tariffs (commissions, delivery, storage)",
        params_model=TariffsParams, id_type="none",
        call_fn=lambda api, _, p: api.calculate_tariffs(
            p["offers"], campaign_id=p.get("campaign_id") or None),
        keywords=["tariffs", "commissions", "calculate"],
    ),

    # ── Chats ──────────────────────────────────────────────────────
    Action(
        id="chats", domain="chats",
        description="List buyer chats",
        params_model=PaginatedParams, id_type="business",
        call_fn=lambda api, bid, p: api.get_chats(
            bid, page_token=p.get("page_token", ""), limit=p.get("limit", 50)),
        keywords=["chats", "list", "messages"],
    ),
    Action(
        id="chat_history", domain="chats",
        description="Get chat history",
        params_model=ChatHistoryParams, id_type="business",
        call_fn=lambda api, bid, p: api.get_chat_history(
            bid, p["chat_id"],
            page_token=p.get("page_token", ""), limit=p.get("limit", 50)),
        keywords=["chat", "history", "messages"],
    ),
    Action(
        id="chat_send", domain="chats",
        description="Send text message in buyer chat",
        params_model=ChatSendParams, id_type="business",
        call_fn=lambda api, bid, p: api.send_chat_message(
            bid, p["chat_id"], p["message"]),
        keywords=["chat", "send", "message"],
    ),
    Action(
        id="chat_new", domain="chats",
        description="Create new chat",
        params_model=GenericPayload, id_type="business",
        call_fn=lambda api, bid, p: api.create_chat(bid, p),
        keywords=["chat", "create", "new"],
    ),
    Action(
        id="chat_file_send", domain="chats",
        description="Send file in chat",
        params_model=ChatFileSendParams, id_type="business",
        call_fn=lambda api, bid, p: api.send_chat_file(
            bid, p["chat_id"], _safe_path(p["file_path"])),
        keywords=["chat", "file", "send"],
    ),

    # ── Reports ────────────────────────────────────────────────────
    Action(
        id="report_status", domain="reports",
        description="Check async report status",
        params_model=ReportStatusParams, id_type="none",
        call_fn=lambda api, _, p: api.get_report_status(p["report_id"]),
        keywords=["report", "status"],
    ),
    Action(
        id="report_generate", domain="reports",
        description="Start async report generation",
        params_model=ReportGenerateParams, id_type="none",
        call_fn=lambda api, _, p: api.generate_report(
            p["report_type"], p.get("payload") or None),
        keywords=["report", "generate", "create"],
    ),
    Action(
        id="report_barcodes", domain="reports",
        description="Generate barcodes report (v1)",
        params_model=GenericPayload, id_type="none",
        call_fn=lambda api, _, p: api.generate_barcodes_report(p),
        keywords=["report", "barcodes"],
    ),

    # ── Stats ──────────────────────────────────────────────────────
    Action(
        id="order_stats", domain="stats",
        description="Get order statistics",
        params_model=OrderStatsParams, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_order_stats(
            cid, date_from=p.get("date_from", ""), date_to=p.get("date_to", "")),
        keywords=["order", "stats", "statistics"],
    ),
    Action(
        id="sku_stats", domain="stats",
        description="Get SKU performance stats",
        params_model=None, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_sku_stats(cid),
        keywords=["sku", "stats", "performance"],
    ),

    # ── Supply Requests ────────────────────────────────────────────
    Action(
        id="supply_requests", domain="supply",
        description="List supply requests",
        params_model=None, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_supply_requests(cid),
        keywords=["supply", "requests", "list"],
    ),
    Action(
        id="supply_request_items", domain="supply",
        description="Get supply request items",
        params_model=None, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_supply_request_items(cid),
        keywords=["supply", "request", "items"],
    ),
    Action(
        id="supply_request_documents", domain="supply",
        description="Download supply request documents (PDF)",
        params_model=None, id_type="campaign",
        call_fn=lambda api, cid, p: api.get_supply_request_documents(cid),
        is_file=True,
        keywords=["supply", "request", "documents", "pdf"],
    ),

    # ── Operations ─────────────────────────────────────────────────
    Action(
        id="operations", domain="operations",
        description="Get async operations",
        params_model=None, id_type="business",
        call_fn=lambda api, bid, p: api.get_operations(bid),
        keywords=["operations", "async"],
    ),
]

ACTIONS: dict[str, Action] = {a.id: a for a in _ACTIONS_LIST}
