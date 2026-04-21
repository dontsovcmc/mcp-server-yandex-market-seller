"""Клиент для Yandex Market Partner API.

Docs: https://yandex.ru/dev/market/partner-api/doc/
OpenAPI spec: https://github.com/yandex-market/yandex-market-partner-api/blob/master/openapi/openapi.yaml
Base URL: https://api.partner.market.yandex.ru
Auth: Api-Key header or OAuth 2.0 Bearer token
"""

import logging
import sys

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", stream=sys.stderr)
log = logging.getLogger(__name__)

BASE_URL = "https://api.partner.market.yandex.ru"


class YandexMarketAPI:
    """Синхронный клиент Yandex Market Partner API."""

    def __init__(self, token: str, auth_type: str = "api-key"):
        self.session = requests.Session()
        if auth_type == "oauth":
            self.session.headers.update({"Authorization": f"Bearer {token}"})
        else:
            self.session.headers.update({"Api-Key": token})
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def _get(self, path: str, **kwargs) -> dict:
        resp = self.session.get(f"{BASE_URL}{path}", timeout=30, **kwargs)
        if not resp.ok:
            raise RuntimeError(f"GET {path} -> {resp.status_code}: {resp.text}")
        return resp.json()

    def _get_bytes(self, path: str, **kwargs) -> bytes:
        resp = self.session.get(f"{BASE_URL}{path}", timeout=30, **kwargs)
        if not resp.ok:
            raise RuntimeError(f"GET {path} -> {resp.status_code}: {resp.text}")
        return resp.content

    def _post(self, path: str, payload: dict | None = None, **kwargs) -> dict:
        resp = self.session.post(f"{BASE_URL}{path}", json=payload, timeout=30, **kwargs)
        if not resp.ok:
            raise RuntimeError(f"POST {path} -> {resp.status_code}: {resp.text}")
        return resp.json()

    def _put(self, path: str, payload: dict, **kwargs) -> dict:
        resp = self.session.put(f"{BASE_URL}{path}", json=payload, timeout=30, **kwargs)
        if not resp.ok:
            raise RuntimeError(f"PUT {path} -> {resp.status_code}: {resp.text}")
        return resp.json()

    def _delete(self, path: str, payload: dict | None = None, **kwargs) -> dict:
        resp = self.session.request("DELETE", f"{BASE_URL}{path}", json=payload, timeout=30, **kwargs)
        if not resp.ok:
            raise RuntimeError(f"DELETE {path} -> {resp.status_code}: {resp.text}")
        return resp.json()

    # --- Кампании и настройки ---

    def get_campaigns(self) -> list:
        """Получить список кампаний (магазинов)."""
        data = self._get("/v2/campaigns")
        return data.get("campaigns", [])

    def get_campaign(self, campaign_id: int) -> dict:
        """Получить информацию о кампании."""
        data = self._get(f"/v2/campaigns/{campaign_id}")
        return data.get("campaign", {})

    def get_campaign_settings(self, campaign_id: int) -> dict:
        """Получить настройки кампании."""
        return self._get(f"/v2/campaigns/{campaign_id}/settings")

    def update_campaign_settings(self, campaign_id: int, settings: dict) -> dict:
        """Обновить настройки кампании."""
        return self._put(f"/v2/campaigns/{campaign_id}/settings", settings)

    def get_business_settings(self, business_id: int) -> dict:
        """Получить настройки бизнеса."""
        return self._get(f"/v2/businesses/{business_id}/settings")

    def update_business_settings(self, business_id: int, settings: dict) -> dict:
        """Обновить настройки бизнеса."""
        return self._put(f"/v2/businesses/{business_id}/settings", settings)

    # --- Заказы v2 ---

    def get_orders(self, campaign_id: int, status: str = "", page: int = 1,
                   page_size: int = 50) -> dict:
        """Получить список заказов."""
        params = {"page": page, "pageSize": page_size}
        if status:
            params["status"] = status
        return self._get(f"/v2/campaigns/{campaign_id}/orders", params=params)

    def get_order(self, campaign_id: int, order_id: int) -> dict:
        """Получить информацию о заказе."""
        data = self._get(f"/v2/campaigns/{campaign_id}/orders/{order_id}")
        return data.get("order", {})

    def update_order_status(self, campaign_id: int, order_id: int,
                            status: str, substatus: str = "") -> dict:
        """Обновить статус заказа."""
        payload: dict = {"order": {"status": status}}
        if substatus:
            payload["order"]["substatus"] = substatus
        return self._put(f"/v2/campaigns/{campaign_id}/orders/{order_id}/status", payload)

    def batch_update_order_statuses(self, campaign_id: int, updates: list[dict]) -> dict:
        """Пакетное обновление статусов заказов."""
        return self._post(f"/v2/campaigns/{campaign_id}/orders/status-update",
                          {"orders": updates})

    def get_order_labels(self, campaign_id: int, order_id: int) -> bytes:
        """Скачать этикетки заказа (PDF)."""
        return self._get_bytes(
            f"/v2/campaigns/{campaign_id}/orders/{order_id}/delivery/labels")

    def get_order_labels_data(self, campaign_id: int, order_id: int) -> dict:
        """Получить данные этикеток заказа (JSON)."""
        return self._get(
            f"/v2/campaigns/{campaign_id}/orders/{order_id}/delivery/labels/data")

    def get_order_box_label(self, campaign_id: int, order_id: int,
                            shipment_id: int, box_id: int) -> bytes:
        """Скачать этикетку коробки."""
        return self._get_bytes(
            f"/v2/campaigns/{campaign_id}/orders/{order_id}/delivery/shipments/{shipment_id}/boxes/{box_id}/label")

    def get_order_items(self, campaign_id: int, order_id: int) -> dict:
        """Получить позиции заказа."""
        return self._get(f"/v2/campaigns/{campaign_id}/orders/{order_id}/items")

    def update_order_items(self, campaign_id: int, order_id: int, items: list[dict]) -> dict:
        """Обновить позиции заказа."""
        return self._put(f"/v2/campaigns/{campaign_id}/orders/{order_id}/items",
                         {"items": items})

    def get_order_boxes(self, campaign_id: int, order_id: int) -> dict:
        """Получить коробки заказа."""
        return self._get(f"/v2/campaigns/{campaign_id}/orders/{order_id}/boxes")

    def update_order_boxes(self, campaign_id: int, order_id: int, boxes: list[dict]) -> dict:
        """Обновить коробки заказа."""
        return self._put(f"/v2/campaigns/{campaign_id}/orders/{order_id}/boxes",
                         {"boxes": boxes})

    def set_shipment_boxes(self, campaign_id: int, order_id: int,
                           shipment_id: int, boxes: list[dict]) -> dict:
        """Задать коробки отгрузки."""
        return self._put(
            f"/v2/campaigns/{campaign_id}/orders/{order_id}/delivery/shipments/{shipment_id}/boxes",
            {"boxes": boxes})

    def accept_order_cancellation(self, campaign_id: int, order_id: int) -> dict:
        """Принять отмену заказа."""
        return self._post(
            f"/v2/campaigns/{campaign_id}/orders/{order_id}/cancellation/accept")

    def set_order_delivery_date(self, campaign_id: int, order_id: int, dates: dict) -> dict:
        """Установить дату доставки."""
        return self._put(f"/v2/campaigns/{campaign_id}/orders/{order_id}/delivery/date",
                         {"delivery": dates})

    def get_order_tracking(self, campaign_id: int, order_id: int) -> dict:
        """Получить трек-номер заказа."""
        return self._get(
            f"/v2/campaigns/{campaign_id}/orders/{order_id}/delivery/track")

    def set_order_tracking(self, campaign_id: int, order_id: int, tracks: list[dict]) -> dict:
        """Установить трек-номер заказа."""
        return self._post(
            f"/v2/campaigns/{campaign_id}/orders/{order_id}/delivery/track",
            {"tracks": tracks})

    def get_order_buyer(self, campaign_id: int, order_id: int) -> dict:
        """Получить данные покупателя."""
        return self._get(f"/v2/campaigns/{campaign_id}/orders/{order_id}/buyer")

    def get_order_business_buyer(self, campaign_id: int, order_id: int) -> dict:
        """Получить данные юр.лица покупателя."""
        return self._get(
            f"/v2/campaigns/{campaign_id}/orders/{order_id}/business-buyer")

    def verify_order_eac(self, campaign_id: int, order_id: int, code: str) -> dict:
        """Проверить код подтверждения (EAC)."""
        return self._post(
            f"/v2/campaigns/{campaign_id}/orders/{order_id}/verifyEac",
            {"code": code})

    def get_order_storage_limit(self, campaign_id: int, order_id: int) -> dict:
        """Получить срок хранения заказа."""
        return self._get(
            f"/v2/campaigns/{campaign_id}/orders/{order_id}/delivery/storage-limit")

    def set_order_storage_limit(self, campaign_id: int, order_id: int, date: str) -> dict:
        """Установить срок хранения заказа."""
        return self._put(
            f"/v2/campaigns/{campaign_id}/orders/{order_id}/delivery/storage-limit",
            {"storageLimit": {"date": date}})

    def deliver_digital_goods(self, campaign_id: int, order_id: int, items: list[dict]) -> dict:
        """Передать цифровые товары."""
        return self._post(
            f"/v2/campaigns/{campaign_id}/orders/{order_id}/deliverDigitalGoods",
            {"items": items})

    def get_order_documents(self, campaign_id: int, order_id: int) -> dict:
        """Получить документы заказа."""
        return self._get(f"/v2/campaigns/{campaign_id}/orders/{order_id}/documents")

    def create_order_document(self, campaign_id: int, order_id: int, document: dict) -> dict:
        """Создать документ заказа."""
        return self._post(f"/v2/campaigns/{campaign_id}/orders/{order_id}/documents",
                          document)

    # --- Заказы v1 ---

    def get_business_orders(self, business_id: int, payload: dict) -> dict:
        """Получить заказы бизнеса."""
        return self._post(f"/v1/businesses/{business_id}/orders", payload)

    def create_order_v1(self, campaign_id: int, order: dict) -> dict:
        """Создать заказ (v1)."""
        return self._post(f"/v1/campaigns/{campaign_id}/orders/create", order)

    def update_order_v1(self, campaign_id: int, order: dict) -> dict:
        """Обновить заказ (v1)."""
        return self._post(f"/v1/campaigns/{campaign_id}/orders/update", order)

    def update_order_options(self, campaign_id: int, options: dict) -> dict:
        """Обновить параметры заказа (v1)."""
        return self._post(f"/v1/campaigns/{campaign_id}/orders/update-options", options)

    # --- Возвраты v2 ---

    def get_returns(self, campaign_id: int, page: int = 1, page_size: int = 50) -> dict:
        """Получить список возвратов."""
        params = {"page": page, "pageSize": page_size}
        return self._get(f"/v2/campaigns/{campaign_id}/returns", params=params)

    def get_return(self, campaign_id: int, order_id: int, return_id: int) -> dict:
        """Получить информацию о возврате."""
        return self._get(
            f"/v2/campaigns/{campaign_id}/orders/{order_id}/returns/{return_id}")

    def get_return_decision(self, campaign_id: int, order_id: int, return_id: int) -> dict:
        """Получить решение по возврату."""
        return self._get(
            f"/v2/campaigns/{campaign_id}/orders/{order_id}/returns/{return_id}/decision")

    def set_return_decision(self, campaign_id: int, order_id: int,
                            return_id: int, decision: dict) -> dict:
        """Установить решение по возврату."""
        return self._post(
            f"/v2/campaigns/{campaign_id}/orders/{order_id}/returns/{return_id}/decision",
            decision)

    def submit_return_decision(self, campaign_id: int, order_id: int, return_id: int) -> dict:
        """Подтвердить решение по возврату."""
        return self._post(
            f"/v2/campaigns/{campaign_id}/orders/{order_id}/returns/{return_id}/decision/submit")

    def get_return_application(self, campaign_id: int, order_id: int, return_id: int) -> bytes:
        """Скачать заявление на возврат (PDF)."""
        return self._get_bytes(
            f"/v2/campaigns/{campaign_id}/orders/{order_id}/returns/{return_id}/application")

    # --- Возвраты v1 ---

    def get_business_return_decisions(self, business_id: int, payload: dict) -> dict:
        """Получить решения по возвратам бизнеса."""
        return self._post(f"/v1/businesses/{business_id}/returns/decisions", payload)

    def create_return_v1(self, campaign_id: int, payload: dict) -> dict:
        """Создать возврат (v1)."""
        return self._post(f"/v1/campaigns/{campaign_id}/returns/create", payload)

    def cancel_return_v1(self, campaign_id: int, payload: dict) -> dict:
        """Отменить возврат (v1)."""
        return self._post(f"/v1/campaigns/{campaign_id}/returns/cancel", payload)

    # --- First-mile отгрузки ---

    def get_shipments(self, campaign_id: int, **params) -> dict:
        """Получить список отгрузок."""
        return self._get(f"/v2/campaigns/{campaign_id}/first-mile/shipments", params=params)

    def search_shipments(self, campaign_id: int, payload: dict) -> dict:
        """Поиск отгрузок."""
        return self._post(f"/v2/campaigns/{campaign_id}/first-mile/shipments", payload)

    def get_shipment(self, campaign_id: int, shipment_id: int) -> dict:
        """Получить отгрузку."""
        return self._get(
            f"/v2/campaigns/{campaign_id}/first-mile/shipments/{shipment_id}")

    def update_shipment(self, campaign_id: int, shipment_id: int, payload: dict) -> dict:
        """Обновить отгрузку."""
        return self._put(
            f"/v2/campaigns/{campaign_id}/first-mile/shipments/{shipment_id}", payload)

    def confirm_shipment(self, campaign_id: int, shipment_id: int) -> dict:
        """Подтвердить отгрузку."""
        return self._post(
            f"/v2/campaigns/{campaign_id}/first-mile/shipments/{shipment_id}/confirm")

    def get_shipment_orders(self, campaign_id: int, shipment_id: int) -> dict:
        """Получить заказы отгрузки."""
        return self._get(
            f"/v2/campaigns/{campaign_id}/first-mile/shipments/{shipment_id}/orders/info")

    def transfer_shipment_orders(self, campaign_id: int, shipment_id: int,
                                 payload: dict) -> dict:
        """Перенести заказы в отгрузку."""
        return self._post(
            f"/v2/campaigns/{campaign_id}/first-mile/shipments/{shipment_id}/orders/transfer",
            payload)

    def get_shipment_act(self, campaign_id: int, shipment_id: int) -> bytes:
        """Скачать акт приёма-передачи (PDF)."""
        return self._get_bytes(
            f"/v2/campaigns/{campaign_id}/first-mile/shipments/{shipment_id}/act")

    def get_shipment_inbound_act(self, campaign_id: int, shipment_id: int) -> bytes:
        """Скачать акт приёмки (PDF)."""
        return self._get_bytes(
            f"/v2/campaigns/{campaign_id}/first-mile/shipments/{shipment_id}/inbound-act")

    def get_shipment_waybill(self, campaign_id: int, shipment_id: int) -> bytes:
        """Скачать транспортную накладную (PDF)."""
        return self._get_bytes(
            f"/v2/campaigns/{campaign_id}/first-mile/shipments/{shipment_id}/transportation-waybill")

    def get_shipment_discrepancy_act(self, campaign_id: int, shipment_id: int) -> bytes:
        """Скачать акт расхождений (PDF)."""
        return self._get_bytes(
            f"/v2/campaigns/{campaign_id}/first-mile/shipments/{shipment_id}/discrepancy-act")

    def get_shipment_pallets(self, campaign_id: int, shipment_id: int) -> dict:
        """Получить паллеты отгрузки."""
        return self._get(
            f"/v2/campaigns/{campaign_id}/first-mile/shipments/{shipment_id}/pallets")

    def set_shipment_pallets(self, campaign_id: int, shipment_id: int,
                             pallets: list[dict]) -> dict:
        """Задать паллеты отгрузки."""
        return self._put(
            f"/v2/campaigns/{campaign_id}/first-mile/shipments/{shipment_id}/pallets",
            {"pallets": pallets})

    def get_shipment_pallet_labels(self, campaign_id: int, shipment_id: int) -> bytes:
        """Скачать этикетки паллет (PDF)."""
        return self._get_bytes(
            f"/v2/campaigns/{campaign_id}/first-mile/shipments/{shipment_id}/pallet/labels")

    # --- Склады ---

    def get_warehouses(self, business_id: int) -> dict:
        """Получить склады бизнеса."""
        return self._get(f"/v2/businesses/{business_id}/warehouses")

    def get_all_warehouses(self) -> dict:
        """Получить все склады Маркета."""
        return self._get("/v2/warehouses")

    def set_warehouse_status(self, campaign_id: int, enabled: bool) -> dict:
        """Включить/выключить склад кампании."""
        return self._post(f"/v2/campaigns/{campaign_id}/warehouse/status",
                          {"enabled": enabled})

    def get_reception_transfer_act(self, campaign_id: int) -> bytes:
        """Скачать акт приёма-передачи склада (PDF)."""
        return self._get_bytes(
            f"/v2/campaigns/{campaign_id}/shipments/reception-transfer-act")

    # --- Товары (offer-mappings) ---

    def get_offer_mappings(self, business_id: int, offer_ids: list[str] | None = None,
                           page_token: str = "", limit: int = 200) -> dict:
        """Получить список товаров бизнеса."""
        payload: dict = {}
        if offer_ids:
            payload["offerIds"] = offer_ids
        params: dict = {"limit": limit}
        if page_token:
            params["page_token"] = page_token
        return self._post(f"/v2/businesses/{business_id}/offer-mappings", payload, params=params)

    def update_offer_mappings(self, business_id: int, offers: list[dict]) -> dict:
        """Обновить товары."""
        return self._post(f"/v2/businesses/{business_id}/offer-mappings/update",
                          {"offerMappings": offers})

    def delete_offer_mappings(self, business_id: int, offer_ids: list[str]) -> dict:
        """Удалить товары."""
        return self._post(f"/v2/businesses/{business_id}/offer-mappings/delete",
                          {"offerIds": offer_ids})

    def archive_offer_mappings(self, business_id: int, offer_ids: list[str]) -> dict:
        """Архивировать товары."""
        return self._post(f"/v2/businesses/{business_id}/offer-mappings/archive",
                          {"offerIds": offer_ids})

    def unarchive_offer_mappings(self, business_id: int, offer_ids: list[str]) -> dict:
        """Разархивировать товары."""
        return self._post(f"/v2/businesses/{business_id}/offer-mappings/unarchive",
                          {"offerIds": offer_ids})

    def generate_barcodes(self, business_id: int, offer_ids: list[str]) -> dict:
        """Сгенерировать штрихкоды для товаров."""
        return self._post(f"/v1/businesses/{business_id}/offer-mappings/barcodes/generate",
                          {"offerIds": offer_ids})

    # --- Цены ---

    def get_offer_prices(self, campaign_id: int, page_token: str = "",
                         limit: int = 200) -> dict:
        """Получить цены товаров кампании."""
        params: dict = {"limit": limit}
        if page_token:
            params["page_token"] = page_token
        return self._post(f"/v2/campaigns/{campaign_id}/offer-prices", {}, params=params)

    def update_offer_prices(self, campaign_id: int, prices: list[dict]) -> dict:
        """Обновить цены товаров кампании."""
        return self._post(f"/v2/campaigns/{campaign_id}/offer-prices/updates",
                          {"offers": prices})

    def get_business_offer_prices(self, business_id: int, offer_ids: list[str] | None = None,
                                  page_token: str = "", limit: int = 200) -> dict:
        """Получить цены товаров бизнеса."""
        payload: dict = {}
        if offer_ids:
            payload["offerIds"] = offer_ids
        params: dict = {"limit": limit}
        if page_token:
            params["page_token"] = page_token
        return self._post(f"/v2/businesses/{business_id}/offer-prices", payload, params=params)

    def update_business_offer_prices(self, business_id: int, prices: list[dict]) -> dict:
        """Обновить цены товаров бизнеса."""
        return self._post(f"/v2/businesses/{business_id}/offer-prices/updates",
                          {"offers": prices})

    def get_price_quarantine(self, business_id: int, payload: dict | None = None) -> dict:
        """Получить товары на карантине цен (бизнес)."""
        return self._post(f"/v2/businesses/{business_id}/price-quarantine", payload or {})

    def confirm_price_quarantine(self, business_id: int, offer_ids: list[str]) -> dict:
        """Подтвердить цены на карантине (бизнес)."""
        return self._post(f"/v2/businesses/{business_id}/price-quarantine/confirm",
                          {"offerIds": offer_ids})

    def get_campaign_price_quarantine(self, campaign_id: int, payload: dict | None = None) -> dict:
        """Получить товары на карантине цен (кампания)."""
        return self._post(f"/v2/campaigns/{campaign_id}/price-quarantine", payload or {})

    def confirm_campaign_price_quarantine(self, campaign_id: int, offer_ids: list[str]) -> dict:
        """Подтвердить цены на карантине (кампания)."""
        return self._post(f"/v2/campaigns/{campaign_id}/price-quarantine/confirm",
                          {"offerIds": offer_ids})

    # --- Остатки ---

    def get_stocks(self, campaign_id: int, page_token: str = "",
                   limit: int = 200) -> dict:
        """Получить остатки товаров."""
        params: dict = {"limit": limit}
        if page_token:
            params["page_token"] = page_token
        return self._get(f"/v2/campaigns/{campaign_id}/offers/stocks", params=params)

    def update_stocks(self, campaign_id: int, stocks: list[dict]) -> dict:
        """Обновить остатки товаров."""
        return self._put(f"/v2/campaigns/{campaign_id}/offers/stocks",
                         {"skus": stocks})

    # --- Offers (кампании) ---

    def get_campaign_offers(self, campaign_id: int, page_token: str = "",
                            limit: int = 200) -> dict:
        """Получить товары кампании с ценами и остатками."""
        params: dict = {"limit": limit}
        if page_token:
            params["page_token"] = page_token
        return self._post(f"/v2/campaigns/{campaign_id}/offers", {}, params=params)

    def update_campaign_offers(self, campaign_id: int, offers: list[dict]) -> dict:
        """Обновить условия продажи товаров."""
        return self._post(f"/v2/campaigns/{campaign_id}/offers/update",
                          {"offers": offers})

    # --- Скрытые товары ---

    def get_hidden_offers(self, campaign_id: int, page_token: str = "",
                          limit: int = 200) -> dict:
        """Получить скрытые товары."""
        params: dict = {"limit": limit}
        if page_token:
            params["page_token"] = page_token
        return self._get(f"/v2/campaigns/{campaign_id}/hidden-offers", params=params)

    def unhide_offers(self, campaign_id: int, offer_ids: list[str]) -> dict:
        """Показать скрытые товары."""
        return self._post(f"/v2/campaigns/{campaign_id}/hidden-offers/delete",
                          {"hiddenOffers": [{"offerId": oid} for oid in offer_ids]})

    # --- Карточки товаров ---

    def get_offer_cards(self, business_id: int, offer_ids: list[str] | None = None,
                        page_token: str = "", limit: int = 200) -> dict:
        """Получить карточки товаров."""
        payload: dict = {}
        if offer_ids:
            payload["offerIds"] = offer_ids
        params: dict = {"limit": limit}
        if page_token:
            params["page_token"] = page_token
        return self._post(f"/v2/businesses/{business_id}/offer-cards", payload, params=params)

    def update_offer_cards(self, business_id: int, cards: list[dict]) -> dict:
        """Обновить карточки товаров."""
        return self._post(f"/v2/businesses/{business_id}/offer-cards/update",
                          {"offerCards": cards})

    def get_offer_recommendations(self, business_id: int, payload: dict | None = None) -> dict:
        """Получить рекомендации по товарам."""
        return self._post(f"/v2/businesses/{business_id}/offers/recommendations",
                          payload or {})

    # --- Доставка ---

    def get_delivery_services(self) -> dict:
        """Получить список служб доставки."""
        return self._get("/v2/delivery/services")

    def get_delivery_options(self, campaign_id: int, payload: dict) -> dict:
        """Получить варианты доставки."""
        return self._post(f"/v1/campaigns/{campaign_id}/delivery-options", payload)

    def get_return_delivery_options(self, campaign_id: int, payload: dict) -> dict:
        """Получить варианты возвратной доставки."""
        return self._post(f"/v1/campaigns/{campaign_id}/return-delivery-options", payload)

    # --- Логистические точки ---

    def get_logistics_points(self, business_id: int, payload: dict | None = None) -> dict:
        """Получить точки сдачи (логистические точки)."""
        return self._post(f"/v1/businesses/{business_id}/logistics-points", payload or {})

    # --- Возвраты ---
    # get_returns и get_return определены выше

    # --- Отзывы ---

    def get_feedbacks(self, business_id: int, page_token: str = "",
                      limit: int = 200) -> dict:
        """Получить отзывы о товарах."""
        params: dict = {"limit": limit}
        if page_token:
            params["page_token"] = page_token
        return self._post(f"/v2/businesses/{business_id}/goods-feedback", {}, params=params)

    def skip_feedback_reaction(self, business_id: int, feedback_ids: list[int]) -> dict:
        """Пропустить отзыв (не отвечать)."""
        return self._post(f"/v2/businesses/{business_id}/goods-feedback/skip-reaction",
                          {"feedbackIds": feedback_ids})

    def get_feedback_comments(self, business_id: int, feedback_id: int,
                              page_token: str = "", limit: int = 50) -> dict:
        """Получить комментарии к отзыву."""
        params: dict = {"limit": limit}
        if page_token:
            params["page_token"] = page_token
        return self._post(f"/v2/businesses/{business_id}/goods-feedback/comments",
                          {"feedbackId": feedback_id}, params=params)

    def update_feedback_comment(self, business_id: int, comment: dict) -> dict:
        """Обновить комментарий к отзыву."""
        return self._post(f"/v2/businesses/{business_id}/goods-feedback/comments/update",
                          comment)

    def delete_feedback_comment(self, business_id: int, comment_id: int) -> dict:
        """Удалить комментарий к отзыву."""
        return self._post(f"/v2/businesses/{business_id}/goods-feedback/comments/delete",
                          {"commentId": comment_id})

    # --- Вопросы ---

    def get_questions(self, business_id: int, payload: dict | None = None) -> dict:
        """Получить вопросы о товарах."""
        return self._post(f"/v1/businesses/{business_id}/goods-questions", payload or {})

    def answer_question(self, business_id: int, answer: dict) -> dict:
        """Ответить на вопрос."""
        return self._post(f"/v1/businesses/{business_id}/goods-questions/answers", answer)

    def update_question_answer(self, business_id: int, update: dict) -> dict:
        """Обновить ответ на вопрос."""
        return self._post(f"/v1/businesses/{business_id}/goods-questions/update", update)

    # --- Статистика ---

    def get_order_stats(self, campaign_id: int, date_from: str = "",
                        date_to: str = "") -> dict:
        """Получить статистику заказов."""
        params: dict = {}
        if date_from:
            params["dateFrom"] = date_from
        if date_to:
            params["dateTo"] = date_to
        return self._get(f"/v2/campaigns/{campaign_id}/stats/orders", params=params)

    def get_sku_stats(self, campaign_id: int, **params) -> dict:
        """Получить статистику по SKU."""
        return self._get(f"/v2/campaigns/{campaign_id}/stats/skus", params=params)

    # --- Рейтинг ---

    def get_quality_ratings(self, business_id: int, campaign_ids: list[int] | None = None) -> dict:
        """Получить рейтинг качества."""
        payload: dict = {}
        if campaign_ids:
            payload["campaignIds"] = campaign_ids
        return self._post(f"/v2/businesses/{business_id}/ratings/quality", payload)

    def get_quality_details(self, campaign_id: int) -> dict:
        """Получить детали рейтинга качества."""
        return self._get(f"/v2/campaigns/{campaign_id}/ratings/quality/details")

    # --- Промоакции ---

    def get_promos(self, business_id: int) -> dict:
        """Получить список акций."""
        return self._post(f"/v2/businesses/{business_id}/promos", {})

    def get_promo_offers(self, business_id: int, promo_id: str, payload: dict | None = None) -> dict:
        """Получить товары в акции."""
        p = payload or {}
        p["promoId"] = promo_id
        return self._post(f"/v2/businesses/{business_id}/promos/offers", p)

    def update_promo_offers(self, business_id: int, payload: dict) -> dict:
        """Обновить товары в акции."""
        return self._post(f"/v2/businesses/{business_id}/promos/offers/update", payload)

    def delete_promo_offers(self, business_id: int, payload: dict) -> dict:
        """Удалить товары из акции."""
        return self._post(f"/v2/businesses/{business_id}/promos/offers/delete", payload)

    # --- Ставки ---

    def get_bids(self, business_id: int, offer_ids: list[str] | None = None,
                 page_token: str = "", limit: int = 200) -> dict:
        """Получить ставки (бизнес)."""
        payload: dict = {}
        if offer_ids:
            payload["offerIds"] = offer_ids
        params: dict = {"limit": limit}
        if page_token:
            params["page_token"] = page_token
        return self._post(f"/v2/businesses/{business_id}/bids/info", payload, params=params)

    def update_bids(self, business_id: int, bids: list[dict]) -> dict:
        """Обновить ставки (бизнес)."""
        return self._put(f"/v2/businesses/{business_id}/bids", {"bids": bids})

    def get_campaign_bids(self, campaign_id: int, offer_ids: list[str] | None = None,
                          page_token: str = "", limit: int = 200) -> dict:
        """Получить ставки (кампания)."""
        payload: dict = {}
        if offer_ids:
            payload["offerIds"] = offer_ids
        params: dict = {"limit": limit}
        if page_token:
            params["page_token"] = page_token
        return self._post(f"/v2/campaigns/{campaign_id}/bids", payload, params=params)

    def update_campaign_bids(self, campaign_id: int, bids: list[dict]) -> dict:
        """Обновить ставки (кампания)."""
        return self._put(f"/v2/campaigns/{campaign_id}/bids", {"bids": bids})

    def get_bid_recommendations(self, business_id: int, payload: dict | None = None) -> dict:
        """Получить рекомендации по ставкам."""
        return self._post(f"/v2/businesses/{business_id}/bids/recommendations", payload or {})

    # --- Точки продаж (outlets) ---

    def get_outlets(self, campaign_id: int, page: int = 1, page_size: int = 50) -> dict:
        """Получить точки продаж."""
        return self._get(f"/v2/campaigns/{campaign_id}/outlets",
                         params={"page": page, "pageSize": page_size})

    def get_outlet(self, campaign_id: int, outlet_id: int) -> dict:
        """Получить точку продаж."""
        return self._get(f"/v2/campaigns/{campaign_id}/outlets/{outlet_id}")

    def create_outlet(self, campaign_id: int, outlet: dict) -> dict:
        """Создать точку продаж."""
        return self._post(f"/v2/campaigns/{campaign_id}/outlets", outlet)

    def update_outlet(self, campaign_id: int, outlet_id: int, outlet: dict) -> dict:
        """Обновить точку продаж."""
        return self._put(f"/v2/campaigns/{campaign_id}/outlets/{outlet_id}", outlet)

    def delete_outlet(self, campaign_id: int, outlet_id: int) -> dict:
        """Удалить точку продаж."""
        return self._delete(f"/v2/campaigns/{campaign_id}/outlets/{outlet_id}")

    def get_outlet_licenses(self, campaign_id: int) -> dict:
        """Получить лицензии точек продаж."""
        return self._get(f"/v2/campaigns/{campaign_id}/outlets/licenses")

    # --- Регионы ---

    def get_regions(self, name: str = "", page: int = 1) -> dict:
        """Поиск регионов."""
        params: dict = {"page": page}
        if name:
            params["name"] = name
        return self._get("/v2/regions", params=params)

    def get_region(self, region_id: int) -> dict:
        """Получить регион."""
        return self._get(f"/v2/regions/{region_id}")

    def get_region_children(self, region_id: int, page: int = 1) -> dict:
        """Получить дочерние регионы."""
        return self._get(f"/v2/regions/{region_id}/children", params={"page": page})

    def get_countries(self) -> dict:
        """Получить список стран."""
        return self._get("/v2/regions/countries")

    # --- Категории ---

    def get_categories_tree(self) -> dict:
        """Получить дерево категорий."""
        return self._post("/v2/categories/tree", {})

    def get_category_parameters(self, category_id: int) -> dict:
        """Получить параметры категории."""
        return self._get(f"/v2/category/{category_id}/parameters")

    def get_max_sale_quantum(self, payload: dict) -> dict:
        """Получить лимиты продажи."""
        return self._post("/v2/categories/max-sale-quantum", payload)

    # --- Расчёт тарифов ---

    def calculate_tariffs(self, offers: list[dict], campaign_id: int | None = None) -> dict:
        """Рассчитать стоимость услуг."""
        payload: dict = {"offers": offers}
        if campaign_id:
            payload["campaignId"] = campaign_id
        return self._post("/v2/tariffs/calculate", payload)

    # --- Чаты ---

    def get_chats(self, business_id: int, page_token: str = "",
                  limit: int = 50) -> dict:
        """Получить список чатов."""
        params: dict = {"limit": limit}
        if page_token:
            params["page_token"] = page_token
        return self._post(f"/v2/businesses/{business_id}/chats", {}, params=params)

    def get_chat_history(self, business_id: int, chat_id: int,
                         page_token: str = "", limit: int = 50) -> dict:
        """Получить историю чата."""
        params: dict = {"chatId": chat_id, "limit": limit}
        if page_token:
            params["page_token"] = page_token
        return self._post(f"/v2/businesses/{business_id}/chats/history", {}, params=params)

    def send_chat_message(self, business_id: int, chat_id: int, message: str) -> dict:
        """Отправить сообщение."""
        return self._post(f"/v2/businesses/{business_id}/chats/message",
                          {"chatId": chat_id, "message": message})

    def create_chat(self, business_id: int, payload: dict) -> dict:
        """Создать чат."""
        return self._post(f"/v2/businesses/{business_id}/chats/new", payload)

    def send_chat_file(self, business_id: int, chat_id: int, file_path: str) -> dict:
        """Отправить файл в чат."""
        with open(file_path, "rb") as f:
            resp = self.session.post(
                f"{BASE_URL}/v2/businesses/{business_id}/chats/file/send",
                params={"chatId": chat_id},
                files={"file": f},
                headers={"Content-Type": None},
                timeout=60,
            )
        if not resp.ok:
            raise RuntimeError(f"Send file -> {resp.status_code}: {resp.text}")
        return resp.json()

    # --- Отчёты ---

    def generate_report(self, report_type: str, payload: dict | None = None) -> dict:
        """Сгенерировать отчёт. Возвращает reportId для polling."""
        return self._post(f"/v2/reports/{report_type}/generate", payload or {})

    def get_report_status(self, report_id: str) -> dict:
        """Проверить статус отчёта."""
        return self._get(f"/v2/reports/info/{report_id}")

    def generate_barcodes_report(self, payload: dict) -> dict:
        """Сгенерировать отчёт со штрихкодами."""
        return self._post("/v1/reports/documents/barcodes/generate", payload)

    # --- Заявки на поставку ---

    def get_supply_requests(self, campaign_id: int, **params) -> dict:
        """Получить заявки на поставку."""
        return self._get(f"/v2/campaigns/{campaign_id}/supply-requests", params=params)

    def get_supply_request_items(self, campaign_id: int, **params) -> dict:
        """Получить позиции заявки."""
        return self._get(f"/v2/campaigns/{campaign_id}/supply-requests/items", params=params)

    def get_supply_request_documents(self, campaign_id: int) -> bytes:
        """Скачать документы заявки (PDF)."""
        return self._get_bytes(f"/v2/campaigns/{campaign_id}/supply-requests/documents")

    # --- Операции ---

    def get_operations(self, business_id: int, **params) -> dict:
        """Получить асинхронные операции."""
        return self._get(f"/v1/businesses/{business_id}/operations", params=params)

    # --- Авторизация ---

    def get_auth_token(self, payload: dict) -> dict:
        """Получить/обновить токен."""
        return self._post("/v2/auth/token", payload)
