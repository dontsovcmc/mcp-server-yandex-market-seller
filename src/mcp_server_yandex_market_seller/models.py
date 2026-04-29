"""Pydantic models for action parameter validation."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


# ── Generic ────────────────────────────────────────────────────────


class GenericPayload(BaseModel):
    """Pass-through JSON payload for actions without a strict schema."""

    model_config = ConfigDict(extra="allow")


class PaginatedParams(BaseModel):
    page_token: str = Field(default="", description="Pagination token")
    limit: int = Field(default=200, description="Page size")


class OfferIdsParams(BaseModel):
    offer_ids: list[str] = Field(description="List of offer IDs")


# ── Offers ─────────────────────────────────────────────────────────


class OffersListParams(BaseModel):
    offer_ids: list[str] | None = Field(default=None, description="Filter by offer IDs")
    page_token: str = Field(default="")
    limit: int = Field(default=200)


class OffersArchiveParams(BaseModel):
    offer_ids: list[str] = Field(description="List of offer IDs")
    archive: bool = Field(default=True, description="True to archive, false to unarchive")


# ── Orders ─────────────────────────────────────────────────────────


class OrdersListParams(BaseModel):
    status: str = Field(default="", description="UNPAID, PROCESSING, DELIVERY, PICKUP, DELIVERED, CANCELLED")
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=50, ge=1, le=200)


class OrderIdParams(BaseModel):
    order_id: int = Field(description="Order ID")


class OrderStatusParams(BaseModel):
    order_id: int = Field(description="Order ID")
    status: str = Field(description="PROCESSING, DELIVERY, DELIVERED, CANCELLED")
    substatus: str = Field(default="", description="Substatus (optional)")


class OrderBoxLabelParams(BaseModel):
    order_id: int
    shipment_id: int
    box_id: int


class OrderItemsUpdateParams(BaseModel):
    order_id: int
    items: list[dict] = Field(description="Array of item objects")


class OrderBoxesUpdateParams(BaseModel):
    order_id: int
    boxes: list[dict] = Field(description="Array of box objects")


class OrderShipmentBoxesParams(BaseModel):
    order_id: int
    shipment_id: int
    boxes: list[dict]


class OrderDeliveryDateParams(BaseModel):
    order_id: int
    dates: dict = Field(description="{fromDate, toDate}")


class OrderTrackingUpdateParams(BaseModel):
    order_id: int
    tracks: list[dict] = Field(description="Array of {trackCode, deliveryServiceId}")


class OrderVerifyEacParams(BaseModel):
    order_id: int
    code: str


class OrderStorageLimitParams(BaseModel):
    order_id: int
    date: str = Field(description="YYYY-MM-DD")


class OrderDeliverDigitalParams(BaseModel):
    order_id: int
    items: list[dict]


class OrderDocumentCreateParams(BaseModel):
    order_id: int
    document: dict


class OrderStatsParams(BaseModel):
    date_from: str = Field(default="")
    date_to: str = Field(default="")


# ── Returns ────────────────────────────────────────────────────────


class ReturnsListParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=50, ge=1, le=200)


class ReturnParams(BaseModel):
    order_id: int
    return_id: int


class ReturnDecisionSetParams(BaseModel):
    order_id: int
    return_id: int
    decision: dict = Field(description="Decision object")


# ── Shipments ──────────────────────────────────────────────────────


class ShipmentIdParams(BaseModel):
    shipment_id: int


class ShipmentPayloadParams(BaseModel):
    shipment_id: int
    payload: dict = Field(description="Shipment data object")


class ShipmentPalletsUpdateParams(BaseModel):
    shipment_id: int
    pallets: list[dict]


# ── Warehouses ─────────────────────────────────────────────────────


class WarehouseStatusParams(BaseModel):
    enabled: bool


# ── Feedbacks ──────────────────────────────────────────────────────


class FeedbackIdParams(BaseModel):
    feedback_id: int


class CommentIdParams(BaseModel):
    comment_id: int


# ── Quality ────────────────────────────────────────────────────────


class QualityRatingParams(BaseModel):
    campaign_id: int = Field(default=0, description="Optional campaign ID to filter")


# ── Promos ─────────────────────────────────────────────────────────


class PromoOffersParams(BaseModel):
    promo_id: str
    payload: dict = Field(default_factory=dict)


# ── Outlets ────────────────────────────────────────────────────────


class OutletIdParams(BaseModel):
    outlet_id: int


class OutletUpdateParams(BaseModel):
    outlet_id: int
    outlet: dict


# ── Geo ────────────────────────────────────────────────────────────


class RegionsParams(BaseModel):
    name: str = Field(default="")
    page: int = Field(default=1)


class RegionIdParams(BaseModel):
    region_id: int


class RegionChildrenParams(BaseModel):
    region_id: int
    page: int = Field(default=1)


# ── Categories ─────────────────────────────────────────────────────


class CategoryIdParams(BaseModel):
    category_id: int


# ── Tariffs ────────────────────────────────────────────────────────


class TariffsParams(BaseModel):
    offers: list[dict] = Field(description="Array of offer objects for tariff calculation")
    campaign_id: int = Field(default=0, description="Optional campaign ID")


# ── Chats ──────────────────────────────────────────────────────────


class ChatHistoryParams(BaseModel):
    chat_id: int
    page_token: str = Field(default="")
    limit: int = Field(default=50)


class ChatSendParams(BaseModel):
    chat_id: int
    message: str


class ChatFileSendParams(BaseModel):
    chat_id: int
    file_path: str


# ── Reports ────────────────────────────────────────────────────────


class ReportStatusParams(BaseModel):
    report_id: str


class ReportGenerateParams(BaseModel):
    report_type: str = Field(description="united-netting, united-marketplace-services, etc.")
    payload: dict = Field(default_factory=dict)
