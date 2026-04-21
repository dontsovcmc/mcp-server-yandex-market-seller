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

    # --- Кампании ---

    def get_campaigns(self) -> list:
        """Получить список кампаний (магазинов)."""
        data = self._get("/v2/campaigns")
        return data.get("campaigns", [])

    def get_campaign(self, campaign_id: int) -> dict:
        """Получить информацию о кампании."""
        data = self._get(f"/v2/campaigns/{campaign_id}")
        return data.get("campaign", {})

    # --- Заказы ---

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

    def get_order_labels(self, campaign_id: int, order_id: int) -> bytes:
        """Скачать этикетки заказа (PDF)."""
        resp = self.session.get(
            f"{BASE_URL}/v2/campaigns/{campaign_id}/orders/{order_id}/delivery/labels",
            timeout=30,
        )
        if not resp.ok:
            raise RuntimeError(f"Download labels -> {resp.status_code}: {resp.text}")
        return resp.content

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
        """Обновить товары (описания, параметры)."""
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

    # --- Цены ---

    def get_offer_prices(self, campaign_id: int, page_token: str = "",
                         limit: int = 200) -> dict:
        """Получить цены товаров кампании."""
        params: dict = {"limit": limit}
        if page_token:
            params["page_token"] = page_token
        return self._post(f"/v2/campaigns/{campaign_id}/offer-prices", {}, params=params)

    def update_offer_prices(self, campaign_id: int, prices: list[dict]) -> dict:
        """Обновить цены товаров.

        prices: [{"offerId": "SKU1", "price": {"value": 1000, "currencyId": "RUR"}}]
        """
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
        """Обновить цены товаров бизнеса.

        prices: [{"offerId": "SKU1", "price": {"value": 1000, "currencyId": "RUR"}}]
        """
        return self._post(f"/v2/businesses/{business_id}/offer-prices/updates",
                          {"offers": prices})

    # --- Остатки ---

    def get_stocks(self, campaign_id: int, page_token: str = "",
                   limit: int = 200) -> dict:
        """Получить остатки товаров на складе."""
        params: dict = {"limit": limit}
        if page_token:
            params["page_token"] = page_token
        return self._get(f"/v2/campaigns/{campaign_id}/offers/stocks", params=params)

    def update_stocks(self, campaign_id: int, stocks: list[dict]) -> dict:
        """Обновить остатки товаров.

        stocks: [{"offerId": "SKU1", "stocks": [{"type": "FIT", "count": 10, "warehouseId": 123}]}]
        """
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
        """Обновить условия продажи товаров в кампании."""
        return self._post(f"/v2/campaigns/{campaign_id}/offers/update",
                          {"offers": offers})

    # --- Скрытые товары ---

    def get_hidden_offers(self, campaign_id: int, page_token: str = "",
                          limit: int = 200) -> dict:
        """Получить список скрытых товаров."""
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

    # --- Склады ---

    def get_warehouses(self, business_id: int) -> dict:
        """Получить склады бизнеса."""
        return self._get(f"/v2/businesses/{business_id}/warehouses")

    # --- Возвраты ---

    def get_returns(self, campaign_id: int, page: int = 1, page_size: int = 50) -> dict:
        """Получить список возвратов."""
        params = {"page": page, "pageSize": page_size}
        return self._get(f"/v2/campaigns/{campaign_id}/returns", params=params)

    def get_return(self, campaign_id: int, order_id: int, return_id: int) -> dict:
        """Получить информацию о возврате."""
        return self._get(
            f"/v2/campaigns/{campaign_id}/orders/{order_id}/returns/{return_id}"
        )

    # --- Отзывы ---

    def get_feedbacks(self, business_id: int, page_token: str = "",
                      limit: int = 200) -> dict:
        """Получить отзывы о товарах."""
        params: dict = {"limit": limit}
        if page_token:
            params["page_token"] = page_token
        return self._post(f"/v2/businesses/{business_id}/goods-feedback", {}, params=params)

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

    # --- Рейтинг ---

    def get_quality_ratings(self, business_id: int, campaign_ids: list[int] | None = None) -> dict:
        """Получить рейтинг качества."""
        payload: dict = {}
        if campaign_ids:
            payload["campaignIds"] = campaign_ids
        return self._post(f"/v2/businesses/{business_id}/ratings/quality", payload)

    # --- Промоакции ---

    def get_promos(self, business_id: int) -> dict:
        """Получить список акций."""
        return self._post(f"/v2/businesses/{business_id}/promos", {})

    # --- Ставки ---

    def get_bids(self, business_id: int, offer_ids: list[str] | None = None,
                 page_token: str = "", limit: int = 200) -> dict:
        """Получить ставки для товаров."""
        payload: dict = {}
        if offer_ids:
            payload["offerIds"] = offer_ids
        params: dict = {"limit": limit}
        if page_token:
            params["page_token"] = page_token
        return self._post(f"/v2/businesses/{business_id}/bids/info", payload, params=params)

    def update_bids(self, business_id: int, bids: list[dict]) -> dict:
        """Обновить ставки для товаров.

        bids: [{"offerId": "SKU1", "bid": 50}]
        """
        return self._put(f"/v2/businesses/{business_id}/bids", {"bids": bids})

    # --- Регионы ---

    def get_regions(self, name: str = "", page: int = 1) -> dict:
        """Поиск регионов."""
        params: dict = {"page": page}
        if name:
            params["name"] = name
        return self._get("/v2/regions", params=params)

    # --- Расчёт тарифов ---

    def calculate_tariffs(self, offers: list[dict], campaign_id: int | None = None) -> dict:
        """Рассчитать стоимость услуг.

        offers: [{"offerId": "SKU1", "price": 1000, "categoryId": 123, ...}]
        """
        payload: dict = {"offers": offers}
        if campaign_id:
            payload["campaignId"] = campaign_id
        return self._post("/v2/tariffs/calculate", payload)

    # --- Категории ---

    def get_categories_tree(self) -> dict:
        """Получить дерево категорий."""
        return self._post("/v2/categories/tree", {})

    def get_category_parameters(self, category_id: int) -> dict:
        """Получить параметры категории."""
        return self._get(f"/v2/category/{category_id}/parameters")

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
        """Отправить сообщение в чат."""
        return self._post(f"/v2/businesses/{business_id}/chats/message",
                          {"chatId": chat_id, "message": message})
