"""CLI interface for Yandex Market tools.

Usage: mcp-server-yandex-market-seller <command> [options]
Without arguments starts MCP server (stdio transport).
"""

import argparse
import json
import sys

from . import __version__
from . import server


def _j(s: str) -> dict | list:
    """Parse JSON string for CLI args."""
    try:
        return json.loads(s)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)


def main(argv: list[str] | None = None):
    parser = argparse.ArgumentParser(
        prog="mcp-server-yandex-market-seller",
        description="Yandex Market Seller: MCP-сервер и CLI",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command")

    # campaigns
    sub.add_parser("campaigns", help="Список кампаний")

    # campaign
    p = sub.add_parser("campaign", help="Кампания")
    p.add_argument("--campaign-id", type=int, default=0)

    # campaign-settings
    p = sub.add_parser("campaign-settings", help="Настройки кампании")
    p.add_argument("--campaign-id", type=int, default=0)

    # campaign-settings-update
    p = sub.add_parser("campaign-settings-update", help="Обновить настройки кампании")
    p.add_argument("settings_json")
    p.add_argument("--campaign-id", type=int, default=0)

    # business-settings
    p = sub.add_parser("business-settings", help="Настройки бизнеса")
    p.add_argument("--business-id", type=int, default=0)

    # business-settings-update
    p = sub.add_parser("business-settings-update", help="Обновить настройки бизнеса")
    p.add_argument("settings_json")
    p.add_argument("--business-id", type=int, default=0)

    # orders
    p = sub.add_parser("orders", help="Заказы")
    p.add_argument("--status", default="")
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--page-size", type=int, default=50)
    p.add_argument("--campaign-id", type=int, default=0)

    # order
    p = sub.add_parser("order", help="Заказ")
    p.add_argument("order_id", type=int)
    p.add_argument("--campaign-id", type=int, default=0)

    # order-items
    p = sub.add_parser("order-items", help="Позиции заказа")
    p.add_argument("order_id", type=int)
    p.add_argument("--campaign-id", type=int, default=0)

    # order-buyer
    p = sub.add_parser("order-buyer", help="Покупатель заказа")
    p.add_argument("order_id", type=int)
    p.add_argument("--campaign-id", type=int, default=0)

    # order-tracking
    p = sub.add_parser("order-tracking", help="Трекинг заказа")
    p.add_argument("order_id", type=int)
    p.add_argument("--campaign-id", type=int, default=0)

    # order-status
    p = sub.add_parser("order-status", help="Изменить статус заказа")
    p.add_argument("order_id", type=int)
    p.add_argument("status")
    p.add_argument("--substatus", default="")
    p.add_argument("--campaign-id", type=int, default=0)

    # order-status-batch
    p = sub.add_parser("order-status-batch", help="Пакетное изменение статусов заказов")
    p.add_argument("updates_json")
    p.add_argument("--campaign-id", type=int, default=0)

    # order-labels
    p = sub.add_parser("order-labels", help="Ярлыки заказа")
    p.add_argument("order_id", type=int)
    p.add_argument("output_path")
    p.add_argument("--campaign-id", type=int, default=0)

    # order-labels-data
    p = sub.add_parser("order-labels-data", help="Данные ярлыков заказа")
    p.add_argument("order_id", type=int)
    p.add_argument("--campaign-id", type=int, default=0)

    # order-box-label
    p = sub.add_parser("order-box-label", help="Ярлык грузоместа")
    p.add_argument("order_id", type=int)
    p.add_argument("shipment_id", type=int)
    p.add_argument("box_id", type=int)
    p.add_argument("output_path")
    p.add_argument("--campaign-id", type=int, default=0)

    # order-items-update
    p = sub.add_parser("order-items-update", help="Обновить позиции заказа")
    p.add_argument("order_id", type=int)
    p.add_argument("items_json")
    p.add_argument("--campaign-id", type=int, default=0)

    # order-boxes
    p = sub.add_parser("order-boxes", help="Грузоместа заказа")
    p.add_argument("order_id", type=int)
    p.add_argument("--campaign-id", type=int, default=0)

    # order-boxes-update
    p = sub.add_parser("order-boxes-update", help="Обновить грузоместа заказа")
    p.add_argument("order_id", type=int)
    p.add_argument("boxes_json")
    p.add_argument("--campaign-id", type=int, default=0)

    # order-shipment-boxes
    p = sub.add_parser("order-shipment-boxes", help="Грузоместа отгрузки заказа")
    p.add_argument("order_id", type=int)
    p.add_argument("shipment_id", type=int)
    p.add_argument("boxes_json")
    p.add_argument("--campaign-id", type=int, default=0)

    # order-cancel-accept
    p = sub.add_parser("order-cancel-accept", help="Подтвердить отмену заказа")
    p.add_argument("order_id", type=int)
    p.add_argument("--campaign-id", type=int, default=0)

    # order-delivery-date
    p = sub.add_parser("order-delivery-date", help="Изменить дату доставки")
    p.add_argument("order_id", type=int)
    p.add_argument("dates_json")
    p.add_argument("--campaign-id", type=int, default=0)

    # order-tracking-update
    p = sub.add_parser("order-tracking-update", help="Обновить трекинг заказа")
    p.add_argument("order_id", type=int)
    p.add_argument("tracks_json")
    p.add_argument("--campaign-id", type=int, default=0)

    # order-business-buyer
    p = sub.add_parser("order-business-buyer", help="Покупатель-юрлицо заказа")
    p.add_argument("order_id", type=int)
    p.add_argument("--campaign-id", type=int, default=0)

    # order-verify-eac
    p = sub.add_parser("order-verify-eac", help="Проверить код подтверждения")
    p.add_argument("order_id", type=int)
    p.add_argument("code")
    p.add_argument("--campaign-id", type=int, default=0)

    # order-storage-limit
    p = sub.add_parser("order-storage-limit", help="Срок хранения заказа")
    p.add_argument("order_id", type=int)
    p.add_argument("--campaign-id", type=int, default=0)

    # order-storage-limit-update
    p = sub.add_parser("order-storage-limit-update", help="Обновить срок хранения")
    p.add_argument("order_id", type=int)
    p.add_argument("date")
    p.add_argument("--campaign-id", type=int, default=0)

    # order-deliver-digital
    p = sub.add_parser("order-deliver-digital", help="Передать цифровой товар")
    p.add_argument("order_id", type=int)
    p.add_argument("items_json")
    p.add_argument("--campaign-id", type=int, default=0)

    # order-documents
    p = sub.add_parser("order-documents", help="Документы заказа")
    p.add_argument("order_id", type=int)
    p.add_argument("--campaign-id", type=int, default=0)

    # order-document-create
    p = sub.add_parser("order-document-create", help="Создать документ заказа")
    p.add_argument("order_id", type=int)
    p.add_argument("document_json")
    p.add_argument("--campaign-id", type=int, default=0)

    # business-orders
    p = sub.add_parser("business-orders", help="Заказы бизнеса")
    p.add_argument("payload_json")
    p.add_argument("--business-id", type=int, default=0)

    # order-create
    p = sub.add_parser("order-create", help="Создать заказ")
    p.add_argument("order_json")
    p.add_argument("--campaign-id", type=int, default=0)

    # order-update-v1
    p = sub.add_parser("order-update-v1", help="Обновить заказ (v1)")
    p.add_argument("order_json")
    p.add_argument("--campaign-id", type=int, default=0)

    # order-update-options
    p = sub.add_parser("order-update-options", help="Обновить параметры заказа")
    p.add_argument("options_json")
    p.add_argument("--campaign-id", type=int, default=0)

    # offers
    p = sub.add_parser("offers", help="Товары")
    p.add_argument("--offer-ids", default="")
    p.add_argument("--limit", type=int, default=200)
    p.add_argument("--business-id", type=int, default=0)

    # offer-cards
    p = sub.add_parser("offer-cards", help="Карточки товаров")
    p.add_argument("--offer-ids", default="")
    p.add_argument("--business-id", type=int, default=0)

    # offers-update
    p = sub.add_parser("offers-update", help="Обновить товары")
    p.add_argument("offers_json")
    p.add_argument("--business-id", type=int, default=0)

    # offers-delete
    p = sub.add_parser("offers-delete", help="Удалить товары")
    p.add_argument("offer_ids")
    p.add_argument("--business-id", type=int, default=0)

    # offers-archive
    p = sub.add_parser("offers-archive", help="Архивировать/разархивировать товары")
    p.add_argument("offer_ids")
    p.add_argument("--unarchive", action="store_true")
    p.add_argument("--business-id", type=int, default=0)

    # generate-barcodes
    p = sub.add_parser("generate-barcodes", help="Сгенерировать штрихкоды")
    p.add_argument("offer_ids")
    p.add_argument("--business-id", type=int, default=0)

    # prices
    p = sub.add_parser("prices", help="Цены")
    p.add_argument("--offer-ids", default="")
    p.add_argument("--limit", type=int, default=200)
    p.add_argument("--business-id", type=int, default=0)

    # prices-update
    p = sub.add_parser("prices-update", help="Обновить цены")
    p.add_argument("prices_json")
    p.add_argument("--business-id", type=int, default=0)

    # price-quarantine
    p = sub.add_parser("price-quarantine", help="Карантин цен")
    p.add_argument("--business-id", type=int, default=0)

    # price-quarantine-confirm
    p = sub.add_parser("price-quarantine-confirm", help="Подтвердить карантин цен")
    p.add_argument("offer_ids")
    p.add_argument("--business-id", type=int, default=0)

    # campaign-price-quarantine
    p = sub.add_parser("campaign-price-quarantine", help="Карантин цен кампании")
    p.add_argument("--payload-json", default="{}")
    p.add_argument("--campaign-id", type=int, default=0)

    # campaign-price-quarantine-confirm
    p = sub.add_parser("campaign-price-quarantine-confirm", help="Подтвердить карантин цен кампании")
    p.add_argument("offer_ids")
    p.add_argument("--campaign-id", type=int, default=0)

    # stocks
    p = sub.add_parser("stocks", help="Остатки")
    p.add_argument("--limit", type=int, default=200)
    p.add_argument("--campaign-id", type=int, default=0)

    # stocks-update
    p = sub.add_parser("stocks-update", help="Обновить остатки")
    p.add_argument("stocks_json")
    p.add_argument("--campaign-id", type=int, default=0)

    # hidden-offers
    p = sub.add_parser("hidden-offers", help="Скрытые товары")
    p.add_argument("--campaign-id", type=int, default=0)

    # campaign-offers
    p = sub.add_parser("campaign-offers", help="Товары кампании")
    p.add_argument("--limit", type=int, default=200)
    p.add_argument("--campaign-id", type=int, default=0)

    # unhide-offers
    p = sub.add_parser("unhide-offers", help="Показать скрытые товары")
    p.add_argument("offer_ids")
    p.add_argument("--campaign-id", type=int, default=0)

    # offer-cards-update
    p = sub.add_parser("offer-cards-update", help="Обновить карточки товаров")
    p.add_argument("cards_json")
    p.add_argument("--business-id", type=int, default=0)

    # offer-recommendations
    p = sub.add_parser("offer-recommendations", help="Рекомендации по товарам")
    p.add_argument("--payload-json", default="{}")
    p.add_argument("--business-id", type=int, default=0)

    # returns
    p = sub.add_parser("returns", help="Возвраты")
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--campaign-id", type=int, default=0)

    # return
    p = sub.add_parser("return", help="Возврат")
    p.add_argument("order_id", type=int)
    p.add_argument("return_id", type=int)
    p.add_argument("--campaign-id", type=int, default=0)

    # return-decision
    p = sub.add_parser("return-decision", help="Решение по возврату")
    p.add_argument("order_id", type=int)
    p.add_argument("return_id", type=int)
    p.add_argument("--campaign-id", type=int, default=0)

    # return-decision-set
    p = sub.add_parser("return-decision-set", help="Установить решение по возврату")
    p.add_argument("order_id", type=int)
    p.add_argument("return_id", type=int)
    p.add_argument("decision_json")
    p.add_argument("--campaign-id", type=int, default=0)

    # return-decision-submit
    p = sub.add_parser("return-decision-submit", help="Подтвердить решение по возврату")
    p.add_argument("order_id", type=int)
    p.add_argument("return_id", type=int)
    p.add_argument("--campaign-id", type=int, default=0)

    # return-application
    p = sub.add_parser("return-application", help="Заявление на возврат")
    p.add_argument("order_id", type=int)
    p.add_argument("return_id", type=int)
    p.add_argument("output_path")
    p.add_argument("--campaign-id", type=int, default=0)

    # business-return-decisions
    p = sub.add_parser("business-return-decisions", help="Решения по возвратам бизнеса")
    p.add_argument("payload_json")
    p.add_argument("--business-id", type=int, default=0)

    # return-create
    p = sub.add_parser("return-create", help="Создать возврат")
    p.add_argument("return_json")
    p.add_argument("--campaign-id", type=int, default=0)

    # return-cancel
    p = sub.add_parser("return-cancel", help="Отменить возврат")
    p.add_argument("return_json")
    p.add_argument("--campaign-id", type=int, default=0)

    # shipments
    p = sub.add_parser("shipments", help="Отгрузки")
    p.add_argument("--campaign-id", type=int, default=0)

    # shipment
    p = sub.add_parser("shipment", help="Отгрузка")
    p.add_argument("shipment_id", type=int)
    p.add_argument("--campaign-id", type=int, default=0)

    # shipments-search
    p = sub.add_parser("shipments-search", help="Поиск отгрузок")
    p.add_argument("payload_json")
    p.add_argument("--campaign-id", type=int, default=0)

    # shipment-update
    p = sub.add_parser("shipment-update", help="Обновить отгрузку")
    p.add_argument("shipment_id", type=int)
    p.add_argument("payload_json")
    p.add_argument("--campaign-id", type=int, default=0)

    # shipment-confirm
    p = sub.add_parser("shipment-confirm", help="Подтвердить отгрузку")
    p.add_argument("shipment_id", type=int)
    p.add_argument("--campaign-id", type=int, default=0)

    # shipment-orders
    p = sub.add_parser("shipment-orders", help="Заказы отгрузки")
    p.add_argument("shipment_id", type=int)
    p.add_argument("--campaign-id", type=int, default=0)

    # shipment-transfer
    p = sub.add_parser("shipment-transfer", help="Передача отгрузки")
    p.add_argument("shipment_id", type=int)
    p.add_argument("payload_json")
    p.add_argument("--campaign-id", type=int, default=0)

    # shipment-act
    p = sub.add_parser("shipment-act", help="Акт отгрузки")
    p.add_argument("shipment_id", type=int)
    p.add_argument("output_path")
    p.add_argument("--campaign-id", type=int, default=0)

    # shipment-inbound-act
    p = sub.add_parser("shipment-inbound-act", help="Акт приёмки отгрузки")
    p.add_argument("shipment_id", type=int)
    p.add_argument("output_path")
    p.add_argument("--campaign-id", type=int, default=0)

    # shipment-waybill
    p = sub.add_parser("shipment-waybill", help="Транспортная накладная")
    p.add_argument("shipment_id", type=int)
    p.add_argument("output_path")
    p.add_argument("--campaign-id", type=int, default=0)

    # shipment-discrepancy-act
    p = sub.add_parser("shipment-discrepancy-act", help="Акт расхождений")
    p.add_argument("shipment_id", type=int)
    p.add_argument("output_path")
    p.add_argument("--campaign-id", type=int, default=0)

    # shipment-pallets
    p = sub.add_parser("shipment-pallets", help="Палеты отгрузки")
    p.add_argument("shipment_id", type=int)
    p.add_argument("--campaign-id", type=int, default=0)

    # shipment-pallets-update
    p = sub.add_parser("shipment-pallets-update", help="Обновить палеты отгрузки")
    p.add_argument("shipment_id", type=int)
    p.add_argument("pallets_json")
    p.add_argument("--campaign-id", type=int, default=0)

    # shipment-pallet-labels
    p = sub.add_parser("shipment-pallet-labels", help="Ярлыки палет")
    p.add_argument("shipment_id", type=int)
    p.add_argument("output_path")
    p.add_argument("--campaign-id", type=int, default=0)

    # feedbacks
    p = sub.add_parser("feedbacks", help="Отзывы")
    p.add_argument("--limit", type=int, default=200)
    p.add_argument("--business-id", type=int, default=0)

    # feedback-skip
    p = sub.add_parser("feedback-skip", help="Пропустить отзывы")
    p.add_argument("feedback_ids_json")
    p.add_argument("--business-id", type=int, default=0)

    # feedback-comments
    p = sub.add_parser("feedback-comments", help="Комментарии отзыва")
    p.add_argument("feedback_id", type=int)
    p.add_argument("--business-id", type=int, default=0)

    # feedback-comment-update
    p = sub.add_parser("feedback-comment-update", help="Обновить комментарий отзыва")
    p.add_argument("comment_json")
    p.add_argument("--business-id", type=int, default=0)

    # feedback-comment-delete
    p = sub.add_parser("feedback-comment-delete", help="Удалить комментарий отзыва")
    p.add_argument("comment_id", type=int)
    p.add_argument("--business-id", type=int, default=0)

    # questions
    p = sub.add_parser("questions", help="Вопросы")
    p.add_argument("--business-id", type=int, default=0)

    # question-answer
    p = sub.add_parser("question-answer", help="Ответить на вопрос")
    p.add_argument("answer_json")
    p.add_argument("--business-id", type=int, default=0)

    # question-update
    p = sub.add_parser("question-update", help="Обновить вопрос")
    p.add_argument("update_json")
    p.add_argument("--business-id", type=int, default=0)

    # quality
    p = sub.add_parser("quality", help="Рейтинг качества")
    p.add_argument("--business-id", type=int, default=0)

    # quality-details
    p = sub.add_parser("quality-details", help="Детали рейтинга")
    p.add_argument("--campaign-id", type=int, default=0)

    # warehouses
    p = sub.add_parser("warehouses", help="Склады бизнеса")
    p.add_argument("--business-id", type=int, default=0)

    # warehouse-status
    p = sub.add_parser("warehouse-status", help="Статус склада")
    p.add_argument("enabled", type=lambda v: v.lower() in ("true", "1", "yes"))
    p.add_argument("--campaign-id", type=int, default=0)

    # all-warehouses
    sub.add_parser("all-warehouses", help="Все склады Маркета")

    # logistics-points
    p = sub.add_parser("logistics-points", help="Точки сдачи")
    p.add_argument("--business-id", type=int, default=0)

    # reception-transfer-act
    p = sub.add_parser("reception-transfer-act", help="Акт приёма-передачи")
    p.add_argument("output_path")
    p.add_argument("--campaign-id", type=int, default=0)

    # outlets
    p = sub.add_parser("outlets", help="Точки продаж")
    p.add_argument("--campaign-id", type=int, default=0)

    # outlet
    p = sub.add_parser("outlet", help="Точка продаж")
    p.add_argument("outlet_id", type=int)
    p.add_argument("--campaign-id", type=int, default=0)

    # outlet-create
    p = sub.add_parser("outlet-create", help="Создать точку продаж")
    p.add_argument("outlet_json")
    p.add_argument("--campaign-id", type=int, default=0)

    # outlet-update
    p = sub.add_parser("outlet-update", help="Обновить точку продаж")
    p.add_argument("outlet_id", type=int)
    p.add_argument("outlet_json")
    p.add_argument("--campaign-id", type=int, default=0)

    # outlet-delete
    p = sub.add_parser("outlet-delete", help="Удалить точку продаж")
    p.add_argument("outlet_id", type=int)
    p.add_argument("--campaign-id", type=int, default=0)

    # outlet-licenses
    p = sub.add_parser("outlet-licenses", help="Лицензии точек продаж")
    p.add_argument("--campaign-id", type=int, default=0)

    # delivery-services
    sub.add_parser("delivery-services", help="Службы доставки")

    # delivery-options
    p = sub.add_parser("delivery-options", help="Варианты доставки")
    p.add_argument("payload_json")
    p.add_argument("--campaign-id", type=int, default=0)

    # return-delivery-options
    p = sub.add_parser("return-delivery-options", help="Варианты обратной доставки")
    p.add_argument("payload_json")
    p.add_argument("--campaign-id", type=int, default=0)

    # regions
    p = sub.add_parser("regions", help="Регионы")
    p.add_argument("name", nargs="?", default="")

    # region
    p = sub.add_parser("region", help="Регион")
    p.add_argument("region_id", type=int)

    # region-children
    p = sub.add_parser("region-children", help="Дочерние регионы")
    p.add_argument("region_id", type=int)
    p.add_argument("--page", type=int, default=1)

    # countries
    sub.add_parser("countries", help="Страны")

    # categories
    sub.add_parser("categories", help="Категории")

    # category-params
    p = sub.add_parser("category-params", help="Параметры категории")
    p.add_argument("category_id", type=int)

    # max-sale-quantum
    p = sub.add_parser("max-sale-quantum", help="Макс. квант продажи")
    p.add_argument("payload_json")

    # tariffs
    p = sub.add_parser("tariffs", help="Тарифы")
    p.add_argument("offers_json")
    p.add_argument("--campaign-id", type=int, default=0)

    # promos
    p = sub.add_parser("promos", help="Акции")
    p.add_argument("--business-id", type=int, default=0)

    # promo-offers
    p = sub.add_parser("promo-offers", help="Товары в акции")
    p.add_argument("promo_id")
    p.add_argument("--payload-json", default="{}")
    p.add_argument("--business-id", type=int, default=0)

    # promo-offers-update
    p = sub.add_parser("promo-offers-update", help="Обновить товары в акции")
    p.add_argument("payload_json")
    p.add_argument("--business-id", type=int, default=0)

    # promo-offers-delete
    p = sub.add_parser("promo-offers-delete", help="Удалить товары из акции")
    p.add_argument("payload_json")
    p.add_argument("--business-id", type=int, default=0)

    # bids
    p = sub.add_parser("bids", help="Ставки")
    p.add_argument("--offer-ids", default="")
    p.add_argument("--business-id", type=int, default=0)

    # bids-update
    p = sub.add_parser("bids-update", help="Обновить ставки")
    p.add_argument("bids_json")
    p.add_argument("--business-id", type=int, default=0)

    # campaign-bids
    p = sub.add_parser("campaign-bids", help="Ставки кампании")
    p.add_argument("--offer-ids", default="")
    p.add_argument("--limit", type=int, default=200)
    p.add_argument("--campaign-id", type=int, default=0)

    # campaign-bids-update
    p = sub.add_parser("campaign-bids-update", help="Обновить ставки кампании")
    p.add_argument("bids_json")
    p.add_argument("--campaign-id", type=int, default=0)

    # bid-recommendations
    p = sub.add_parser("bid-recommendations", help="Рекомендации ставок")
    p.add_argument("--business-id", type=int, default=0)

    # chats
    p = sub.add_parser("chats", help="Чаты")
    p.add_argument("--business-id", type=int, default=0)

    # chat-history
    p = sub.add_parser("chat-history", help="История чата")
    p.add_argument("chat_id", type=int)
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--business-id", type=int, default=0)

    # chat-send
    p = sub.add_parser("chat-send", help="Отправить сообщение в чат")
    p.add_argument("chat_id", type=int)
    p.add_argument("message")
    p.add_argument("--business-id", type=int, default=0)

    # chat-new
    p = sub.add_parser("chat-new", help="Создать чат")
    p.add_argument("payload_json")
    p.add_argument("--business-id", type=int, default=0)

    # chat-file-send
    p = sub.add_parser("chat-file-send", help="Отправить файл в чат")
    p.add_argument("chat_id", type=int)
    p.add_argument("file_path")
    p.add_argument("--business-id", type=int, default=0)

    # report-status
    p = sub.add_parser("report-status", help="Статус отчёта")
    p.add_argument("report_id")

    # report-generate
    p = sub.add_parser("report-generate", help="Сгенерировать отчёт")
    p.add_argument("report_type")
    p.add_argument("--payload-json", default="{}")

    # report-barcodes
    p = sub.add_parser("report-barcodes", help="Отчёт по штрихкодам")
    p.add_argument("payload_json")

    # order-stats
    p = sub.add_parser("order-stats", help="Статистика заказов")
    p.add_argument("--date-from", default="")
    p.add_argument("--date-to", default="")
    p.add_argument("--campaign-id", type=int, default=0)

    # supply-requests
    p = sub.add_parser("supply-requests", help="Заявки на поставку")
    p.add_argument("--campaign-id", type=int, default=0)

    # supply-request-items
    p = sub.add_parser("supply-request-items", help="Товары заявки на поставку")
    p.add_argument("--campaign-id", type=int, default=0)

    # supply-request-documents
    p = sub.add_parser("supply-request-documents", help="Документы заявки на поставку")
    p.add_argument("output_path")
    p.add_argument("--campaign-id", type=int, default=0)

    # sku-stats
    p = sub.add_parser("sku-stats", help="Статистика по SKU")
    p.add_argument("--campaign-id", type=int, default=0)

    # operations
    p = sub.add_parser("operations", help="Асинхронные операции")
    p.add_argument("--business-id", type=int, default=0)

    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        sys.exit(1)

    # fmt: off
    handlers = {
        # ── Campaigns ──────────────────────────────────────────────
        "campaigns": lambda: server.execute_action("campaigns", {}),
        "campaign": lambda: server.execute_action("campaign", {"campaign_id": args.campaign_id}),
        "campaign-settings": lambda: server.execute_action("campaign_settings", {"campaign_id": args.campaign_id}),
        "campaign-settings-update": lambda: server.execute_action("campaign_settings_update", {**_j(args.settings_json), "campaign_id": args.campaign_id}),
        "business-settings": lambda: server.execute_action("business_settings", {"business_id": args.business_id}),
        "business-settings-update": lambda: server.execute_action("business_settings_update", {**_j(args.settings_json), "business_id": args.business_id}),

        # ── Orders v2 ─────────────────────────────────────────────
        "orders": lambda: server.ym_orders(status=args.status, page=args.page, page_size=args.page_size, campaign_id=args.campaign_id),
        "order": lambda: server.ym_order(args.order_id, campaign_id=args.campaign_id),
        "order-items": lambda: server.execute_action("order_items", {"order_id": args.order_id, "campaign_id": args.campaign_id}),
        "order-buyer": lambda: server.execute_action("order_buyer", {"order_id": args.order_id, "campaign_id": args.campaign_id}),
        "order-tracking": lambda: server.execute_action("order_tracking", {"order_id": args.order_id, "campaign_id": args.campaign_id}),
        "order-status": lambda: server.ym_order_status(args.order_id, args.status, substatus=args.substatus, campaign_id=args.campaign_id),
        "order-status-batch": lambda: server.execute_action("order_status_batch", {"orders": _j(args.updates_json), "campaign_id": args.campaign_id}),
        "order-labels": lambda: server.execute_file_action("order_labels", {"order_id": args.order_id, "campaign_id": args.campaign_id}, args.output_path),
        "order-labels-data": lambda: server.execute_action("order_labels_data", {"order_id": args.order_id, "campaign_id": args.campaign_id}),
        "order-box-label": lambda: server.execute_file_action("order_box_label", {"order_id": args.order_id, "shipment_id": args.shipment_id, "box_id": args.box_id, "campaign_id": args.campaign_id}, args.output_path),
        "order-items-update": lambda: server.execute_action("order_items_update", {"order_id": args.order_id, "items": _j(args.items_json), "campaign_id": args.campaign_id}),
        "order-boxes": lambda: server.execute_action("order_boxes", {"order_id": args.order_id, "campaign_id": args.campaign_id}),
        "order-boxes-update": lambda: server.execute_action("order_boxes_update", {"order_id": args.order_id, "boxes": _j(args.boxes_json), "campaign_id": args.campaign_id}),
        "order-shipment-boxes": lambda: server.execute_action("order_shipment_boxes", {"order_id": args.order_id, "shipment_id": args.shipment_id, "boxes": _j(args.boxes_json), "campaign_id": args.campaign_id}),
        "order-cancel-accept": lambda: server.execute_action("order_cancel_accept", {"order_id": args.order_id, "campaign_id": args.campaign_id}),
        "order-delivery-date": lambda: server.execute_action("order_delivery_date", {"order_id": args.order_id, "dates": _j(args.dates_json), "campaign_id": args.campaign_id}),
        "order-tracking-update": lambda: server.execute_action("order_tracking_update", {"order_id": args.order_id, "tracks": _j(args.tracks_json), "campaign_id": args.campaign_id}),
        "order-business-buyer": lambda: server.execute_action("order_business_buyer", {"order_id": args.order_id, "campaign_id": args.campaign_id}),
        "order-verify-eac": lambda: server.execute_action("order_verify_eac", {"order_id": args.order_id, "code": args.code, "campaign_id": args.campaign_id}),
        "order-storage-limit": lambda: server.execute_action("order_storage_limit", {"order_id": args.order_id, "campaign_id": args.campaign_id}),
        "order-storage-limit-update": lambda: server.execute_action("order_storage_limit_update", {"order_id": args.order_id, "date": args.date, "campaign_id": args.campaign_id}),
        "order-deliver-digital": lambda: server.execute_action("order_deliver_digital", {"order_id": args.order_id, "items": _j(args.items_json), "campaign_id": args.campaign_id}),
        "order-documents": lambda: server.execute_action("order_documents", {"order_id": args.order_id, "campaign_id": args.campaign_id}),
        "order-document-create": lambda: server.execute_action("order_document_create", {"order_id": args.order_id, "document": _j(args.document_json), "campaign_id": args.campaign_id}),
        "business-orders": lambda: server.execute_action("business_orders", {**_j(args.payload_json), "business_id": args.business_id}),
        "order-create": lambda: server.execute_action("order_create", {**_j(args.order_json), "campaign_id": args.campaign_id}),
        "order-update-v1": lambda: server.execute_action("order_update_v1", {**_j(args.order_json), "campaign_id": args.campaign_id}),
        "order-update-options": lambda: server.execute_action("order_update_options", {**_j(args.options_json), "campaign_id": args.campaign_id}),

        # ── Offers ─────────────────────────────────────────────────
        "offers": lambda: server.ym_offers(offer_ids=args.offer_ids, limit=args.limit, business_id=args.business_id),
        "offer-cards": lambda: server.execute_action("offer_cards", {"offer_ids": [s.strip() for s in args.offer_ids.split(",") if s.strip()] if args.offer_ids else None, "business_id": args.business_id}),
        "offers-update": lambda: server.execute_action("offers_update", {"offerMappings": _j(args.offers_json), "business_id": args.business_id}),
        "offers-delete": lambda: server.execute_action("offers_delete", {"offer_ids": [s.strip() for s in args.offer_ids.split(",")], "business_id": args.business_id}),
        "offers-archive": lambda: server.execute_action("offers_archive", {"offer_ids": [s.strip() for s in args.offer_ids.split(",")], "archive": not args.unarchive, "business_id": args.business_id}),
        "generate-barcodes": lambda: server.execute_action("generate_barcodes", {"offer_ids": [s.strip() for s in args.offer_ids.split(",")], "business_id": args.business_id}),

        # ── Prices ─────────────────────────────────────────────────
        "prices": lambda: server.ym_prices(offer_ids=args.offer_ids, limit=args.limit, business_id=args.business_id),
        "prices-update": lambda: server.ym_prices_update(args.prices_json, business_id=args.business_id),
        "price-quarantine": lambda: server.execute_action("price_quarantine", {"business_id": args.business_id}),
        "price-quarantine-confirm": lambda: server.execute_action("price_quarantine_confirm", {"offer_ids": [s.strip() for s in args.offer_ids.split(",")], "business_id": args.business_id}),
        "campaign-price-quarantine": lambda: server.execute_action("campaign_price_quarantine", {**_j(args.payload_json), "campaign_id": args.campaign_id}),
        "campaign-price-quarantine-confirm": lambda: server.execute_action("campaign_price_quarantine_confirm", {"offer_ids": [s.strip() for s in args.offer_ids.split(",")], "campaign_id": args.campaign_id}),

        # ── Stocks ─────────────────────────────────────────────────
        "stocks": lambda: server.ym_stocks(limit=args.limit, campaign_id=args.campaign_id),
        "stocks-update": lambda: server.ym_stocks_update(args.stocks_json, campaign_id=args.campaign_id),

        # ── Campaign Offers / Hidden ───────────────────────────────
        "hidden-offers": lambda: server.execute_action("hidden_offers", {"campaign_id": args.campaign_id}),
        "campaign-offers": lambda: server.execute_action("campaign_offers", {"limit": args.limit, "campaign_id": args.campaign_id}),
        "unhide-offers": lambda: server.execute_action("unhide_offers", {"offer_ids": [s.strip() for s in args.offer_ids.split(",")], "campaign_id": args.campaign_id}),

        # ── Offer Cards ────────────────────────────────────────────
        "offer-cards-update": lambda: server.execute_action("offer_cards_update", {"offerCards": _j(args.cards_json), "business_id": args.business_id}),
        "offer-recommendations": lambda: server.execute_action("offer_recommendations", {**_j(args.payload_json), "business_id": args.business_id}),

        # ── Returns ────────────────────────────────────────────────
        "returns": lambda: server.ym_returns(page=args.page, campaign_id=args.campaign_id),
        "return": lambda: server.execute_action("return", {"order_id": args.order_id, "return_id": args.return_id, "campaign_id": args.campaign_id}),
        "return-decision": lambda: server.execute_action("return_decision", {"order_id": args.order_id, "return_id": args.return_id, "campaign_id": args.campaign_id}),
        "return-decision-set": lambda: server.execute_action("return_decision_set", {"order_id": args.order_id, "return_id": args.return_id, "decision": _j(args.decision_json), "campaign_id": args.campaign_id}),
        "return-decision-submit": lambda: server.execute_action("return_decision_submit", {"order_id": args.order_id, "return_id": args.return_id, "campaign_id": args.campaign_id}),
        "return-application": lambda: server.execute_file_action("return_application", {"order_id": args.order_id, "return_id": args.return_id, "campaign_id": args.campaign_id}, args.output_path),
        "business-return-decisions": lambda: server.execute_action("business_return_decisions", {**_j(args.payload_json), "business_id": args.business_id}),
        "return-create": lambda: server.execute_action("return_create", {**_j(args.return_json), "campaign_id": args.campaign_id}),
        "return-cancel": lambda: server.execute_action("return_cancel", {**_j(args.return_json), "campaign_id": args.campaign_id}),

        # ── Shipments ──────────────────────────────────────────────
        "shipments": lambda: server.ym_shipments(campaign_id=args.campaign_id),
        "shipment": lambda: server.execute_action("shipment", {"shipment_id": args.shipment_id, "campaign_id": args.campaign_id}),
        "shipments-search": lambda: server.execute_action("shipments_search", {**_j(args.payload_json), "campaign_id": args.campaign_id}),
        "shipment-update": lambda: server.execute_action("shipment_update", {"shipment_id": args.shipment_id, "payload": _j(args.payload_json), "campaign_id": args.campaign_id}),
        "shipment-confirm": lambda: server.execute_action("shipment_confirm", {"shipment_id": args.shipment_id, "campaign_id": args.campaign_id}),
        "shipment-orders": lambda: server.execute_action("shipment_orders", {"shipment_id": args.shipment_id, "campaign_id": args.campaign_id}),
        "shipment-transfer": lambda: server.execute_action("shipment_transfer", {"shipment_id": args.shipment_id, "payload": _j(args.payload_json), "campaign_id": args.campaign_id}),
        "shipment-act": lambda: server.execute_file_action("shipment_act", {"shipment_id": args.shipment_id, "campaign_id": args.campaign_id}, args.output_path),
        "shipment-inbound-act": lambda: server.execute_file_action("shipment_inbound_act", {"shipment_id": args.shipment_id, "campaign_id": args.campaign_id}, args.output_path),
        "shipment-waybill": lambda: server.execute_file_action("shipment_waybill", {"shipment_id": args.shipment_id, "campaign_id": args.campaign_id}, args.output_path),
        "shipment-discrepancy-act": lambda: server.execute_file_action("shipment_discrepancy_act", {"shipment_id": args.shipment_id, "campaign_id": args.campaign_id}, args.output_path),
        "shipment-pallets": lambda: server.execute_action("shipment_pallets", {"shipment_id": args.shipment_id, "campaign_id": args.campaign_id}),
        "shipment-pallets-update": lambda: server.execute_action("shipment_pallets_update", {"shipment_id": args.shipment_id, "pallets": _j(args.pallets_json), "campaign_id": args.campaign_id}),
        "shipment-pallet-labels": lambda: server.execute_file_action("shipment_pallet_labels", {"shipment_id": args.shipment_id, "campaign_id": args.campaign_id}, args.output_path),

        # ── Feedbacks ──────────────────────────────────────────────
        "feedbacks": lambda: server.ym_feedbacks(limit=args.limit, business_id=args.business_id),
        "feedback-skip": lambda: server.execute_action("feedback_skip", {"feedbackIds": _j(args.feedback_ids_json), "business_id": args.business_id}),
        "feedback-comments": lambda: server.execute_action("feedback_comments", {"feedback_id": args.feedback_id, "business_id": args.business_id}),
        "feedback-comment-update": lambda: server.execute_action("feedback_comment_update", {**_j(args.comment_json), "business_id": args.business_id}),
        "feedback-comment-delete": lambda: server.execute_action("feedback_comment_delete", {"comment_id": args.comment_id, "business_id": args.business_id}),

        # ── Questions ──────────────────────────────────────────────
        "questions": lambda: server.execute_action("questions", {"business_id": args.business_id}),
        "question-answer": lambda: server.execute_action("question_answer", {**_j(args.answer_json), "business_id": args.business_id}),
        "question-update": lambda: server.execute_action("question_update", {**_j(args.update_json), "business_id": args.business_id}),

        # ── Quality ────────────────────────────────────────────────
        "quality": lambda: server.execute_action("quality_rating", {"business_id": args.business_id}),
        "quality-details": lambda: server.execute_action("quality_details", {"campaign_id": args.campaign_id}),

        # ── Warehouses ─────────────────────────────────────────────
        "warehouses": lambda: server.execute_action("warehouses", {"business_id": args.business_id}),
        "warehouse-status": lambda: server.execute_action("warehouse_status", {"enabled": args.enabled, "campaign_id": args.campaign_id}),
        "all-warehouses": lambda: server.execute_action("all_warehouses", {}),
        "logistics-points": lambda: server.execute_action("logistics_points", {"business_id": args.business_id}),
        "reception-transfer-act": lambda: server.execute_file_action("reception_transfer_act", {"campaign_id": args.campaign_id}, args.output_path),

        # ── Outlets ────────────────────────────────────────────────
        "outlets": lambda: server.execute_action("outlets", {"campaign_id": args.campaign_id}),
        "outlet": lambda: server.execute_action("outlet", {"outlet_id": args.outlet_id, "campaign_id": args.campaign_id}),
        "outlet-create": lambda: server.execute_action("outlet_create", {**_j(args.outlet_json), "campaign_id": args.campaign_id}),
        "outlet-update": lambda: server.execute_action("outlet_update", {"outlet_id": args.outlet_id, "outlet": _j(args.outlet_json), "campaign_id": args.campaign_id}),
        "outlet-delete": lambda: server.execute_action("outlet_delete", {"outlet_id": args.outlet_id, "campaign_id": args.campaign_id}),
        "outlet-licenses": lambda: server.execute_action("outlet_licenses", {"campaign_id": args.campaign_id}),

        # ── Delivery ───────────────────────────────────────────────
        "delivery-services": lambda: server.execute_action("delivery_services", {}),
        "delivery-options": lambda: server.execute_action("delivery_options", {**_j(args.payload_json), "campaign_id": args.campaign_id}),
        "return-delivery-options": lambda: server.execute_action("return_delivery_options", {**_j(args.payload_json), "campaign_id": args.campaign_id}),

        # ── Geo ────────────────────────────────────────────────────
        "regions": lambda: server.execute_action("regions", {"name": args.name}),
        "region": lambda: server.execute_action("region", {"region_id": args.region_id}),
        "region-children": lambda: server.execute_action("region_children", {"region_id": args.region_id, "page": args.page}),
        "countries": lambda: server.execute_action("countries", {}),

        # ── Categories ─────────────────────────────────────────────
        "categories": lambda: server.execute_action("categories", {}),
        "category-params": lambda: server.execute_action("category_params", {"category_id": args.category_id}),
        "max-sale-quantum": lambda: server.execute_action("max_sale_quantum", _j(args.payload_json)),

        # ── Tariffs ────────────────────────────────────────────────
        "tariffs": lambda: server.execute_action("tariffs", {"offers": _j(args.offers_json), "campaign_id": args.campaign_id}),

        # ── Promos ─────────────────────────────────────────────────
        "promos": lambda: server.execute_action("promos", {"business_id": args.business_id}),
        "promo-offers": lambda: server.execute_action("promo_offers", {"promo_id": args.promo_id, "payload": _j(args.payload_json), "business_id": args.business_id}),
        "promo-offers-update": lambda: server.execute_action("promo_offers_update", {**_j(args.payload_json), "business_id": args.business_id}),
        "promo-offers-delete": lambda: server.execute_action("promo_offers_delete", {**_j(args.payload_json), "business_id": args.business_id}),

        # ── Bids ───────────────────────────────────────────────────
        "bids": lambda: server.ym_bids(offer_ids=args.offer_ids, business_id=args.business_id),
        "bids-update": lambda: server.execute_action("bids_update", {"bids": _j(args.bids_json), "business_id": args.business_id}),
        "campaign-bids": lambda: server.execute_action("campaign_bids", {"offer_ids": [s.strip() for s in args.offer_ids.split(",") if s.strip()] if args.offer_ids else None, "limit": args.limit, "campaign_id": args.campaign_id}),
        "campaign-bids-update": lambda: server.execute_action("campaign_bids_update", {"bids": _j(args.bids_json), "campaign_id": args.campaign_id}),
        "bid-recommendations": lambda: server.execute_action("bid_recommendations", {"business_id": args.business_id}),

        # ── Chats ──────────────────────────────────────────────────
        "chats": lambda: server.ym_chats(business_id=args.business_id),
        "chat-history": lambda: server.execute_action("chat_history", {"chat_id": args.chat_id, "limit": args.limit, "business_id": args.business_id}),
        "chat-send": lambda: server.execute_action("chat_send", {"chat_id": args.chat_id, "message": args.message, "business_id": args.business_id}),
        "chat-new": lambda: server.execute_action("chat_new", {**_j(args.payload_json), "business_id": args.business_id}),
        "chat-file-send": lambda: server.execute_action("chat_file_send", {"chat_id": args.chat_id, "file_path": args.file_path, "business_id": args.business_id}),

        # ── Reports ────────────────────────────────────────────────
        "report-status": lambda: server.execute_action("report_status", {"report_id": args.report_id}),
        "report-generate": lambda: server.ym_report_generate(args.report_type, payload_json=args.payload_json),
        "report-barcodes": lambda: server.execute_action("report_barcodes", _j(args.payload_json)),

        # ── Stats ──────────────────────────────────────────────────
        "order-stats": lambda: server.execute_action("order_stats", {"date_from": args.date_from, "date_to": args.date_to, "campaign_id": args.campaign_id}),
        "sku-stats": lambda: server.execute_action("sku_stats", {"campaign_id": args.campaign_id}),

        # ── Supply ─────────────────────────────────────────────────
        "supply-requests": lambda: server.execute_action("supply_requests", {"campaign_id": args.campaign_id}),
        "supply-request-items": lambda: server.execute_action("supply_request_items", {"campaign_id": args.campaign_id}),
        "supply-request-documents": lambda: server.execute_file_action("supply_request_documents", {"campaign_id": args.campaign_id}, args.output_path),

        # ── Operations ─────────────────────────────────────────────
        "operations": lambda: server.execute_action("operations", {"business_id": args.business_id}),
    }
    # fmt: on

    print(handlers[args.command]())
