"""CLI interface for Yandex Market tools.

Usage: mcp-server-yandex-market-seller <command> [options]
Without arguments starts MCP server (stdio transport).
"""

import argparse
import sys

from . import __version__
from . import server


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

    handlers = {
        "campaigns": lambda: server.ym_campaigns(),
        "campaign": lambda: server.ym_campaign(campaign_id=args.campaign_id),
        "campaign-settings": lambda: server.ym_campaign_settings(campaign_id=args.campaign_id),
        "campaign-settings-update": lambda: server.ym_campaign_settings_update(args.settings_json, campaign_id=args.campaign_id),
        "business-settings": lambda: server.ym_business_settings(business_id=args.business_id),
        "business-settings-update": lambda: server.ym_business_settings_update(args.settings_json, business_id=args.business_id),
        "orders": lambda: server.ym_orders(status=args.status, page=args.page, page_size=args.page_size, campaign_id=args.campaign_id),
        "order": lambda: server.ym_order(args.order_id, campaign_id=args.campaign_id),
        "order-items": lambda: server.ym_order_items(args.order_id, campaign_id=args.campaign_id),
        "order-buyer": lambda: server.ym_order_buyer(args.order_id, campaign_id=args.campaign_id),
        "order-tracking": lambda: server.ym_order_tracking(args.order_id, campaign_id=args.campaign_id),
        "order-status": lambda: server.ym_order_status(args.order_id, args.status, substatus=args.substatus, campaign_id=args.campaign_id),
        "order-status-batch": lambda: server.ym_order_status_batch(args.updates_json, campaign_id=args.campaign_id),
        "order-labels": lambda: server.ym_order_labels(args.order_id, args.output_path, campaign_id=args.campaign_id),
        "order-labels-data": lambda: server.ym_order_labels_data(args.order_id, campaign_id=args.campaign_id),
        "order-box-label": lambda: server.ym_order_box_label(args.order_id, args.shipment_id, args.box_id, args.output_path, campaign_id=args.campaign_id),
        "order-items-update": lambda: server.ym_order_items_update(args.order_id, args.items_json, campaign_id=args.campaign_id),
        "order-boxes": lambda: server.ym_order_boxes(args.order_id, campaign_id=args.campaign_id),
        "order-boxes-update": lambda: server.ym_order_boxes_update(args.order_id, args.boxes_json, campaign_id=args.campaign_id),
        "order-shipment-boxes": lambda: server.ym_order_shipment_boxes(args.order_id, args.shipment_id, args.boxes_json, campaign_id=args.campaign_id),
        "order-cancel-accept": lambda: server.ym_order_cancel_accept(args.order_id, campaign_id=args.campaign_id),
        "order-delivery-date": lambda: server.ym_order_delivery_date(args.order_id, args.dates_json, campaign_id=args.campaign_id),
        "order-tracking-update": lambda: server.ym_order_tracking_update(args.order_id, args.tracks_json, campaign_id=args.campaign_id),
        "order-business-buyer": lambda: server.ym_order_business_buyer(args.order_id, campaign_id=args.campaign_id),
        "order-verify-eac": lambda: server.ym_order_verify_eac(args.order_id, args.code, campaign_id=args.campaign_id),
        "order-storage-limit": lambda: server.ym_order_storage_limit(args.order_id, campaign_id=args.campaign_id),
        "order-storage-limit-update": lambda: server.ym_order_storage_limit_update(args.order_id, args.date, campaign_id=args.campaign_id),
        "order-deliver-digital": lambda: server.ym_order_deliver_digital(args.order_id, args.items_json, campaign_id=args.campaign_id),
        "order-documents": lambda: server.ym_order_documents(args.order_id, campaign_id=args.campaign_id),
        "order-document-create": lambda: server.ym_order_document_create(args.order_id, args.document_json, campaign_id=args.campaign_id),
        "business-orders": lambda: server.ym_business_orders(args.payload_json, business_id=args.business_id),
        "order-create": lambda: server.ym_order_create(args.order_json, campaign_id=args.campaign_id),
        "order-update-v1": lambda: server.ym_order_update_v1(args.order_json, campaign_id=args.campaign_id),
        "order-update-options": lambda: server.ym_order_update_options(args.options_json, campaign_id=args.campaign_id),
        "offers": lambda: server.ym_offers(offer_ids=args.offer_ids, limit=args.limit, business_id=args.business_id),
        "offer-cards": lambda: server.ym_offer_cards(offer_ids=args.offer_ids, business_id=args.business_id),
        "offers-update": lambda: server.ym_offers_update(args.offers_json, business_id=args.business_id),
        "offers-delete": lambda: server.ym_offers_delete(args.offer_ids, business_id=args.business_id),
        "offers-archive": lambda: server.ym_offers_archive(args.offer_ids, archive=not args.unarchive, business_id=args.business_id),
        "generate-barcodes": lambda: server.ym_generate_barcodes(args.offer_ids, business_id=args.business_id),
        "prices": lambda: server.ym_prices(offer_ids=args.offer_ids, limit=args.limit, business_id=args.business_id),
        "prices-update": lambda: server.ym_prices_update(args.prices_json, business_id=args.business_id),
        "price-quarantine": lambda: server.ym_price_quarantine(business_id=args.business_id),
        "price-quarantine-confirm": lambda: server.ym_price_quarantine_confirm(args.offer_ids, business_id=args.business_id),
        "campaign-price-quarantine": lambda: server.ym_campaign_price_quarantine(args.payload_json, campaign_id=args.campaign_id),
        "campaign-price-quarantine-confirm": lambda: server.ym_campaign_price_quarantine_confirm(args.offer_ids, campaign_id=args.campaign_id),
        "stocks": lambda: server.ym_stocks(limit=args.limit, campaign_id=args.campaign_id),
        "stocks-update": lambda: server.ym_stocks_update(args.stocks_json, campaign_id=args.campaign_id),
        "hidden-offers": lambda: server.ym_hidden_offers(campaign_id=args.campaign_id),
        "campaign-offers": lambda: server.ym_campaign_offers(limit=args.limit, campaign_id=args.campaign_id),
        "unhide-offers": lambda: server.ym_unhide_offers(args.offer_ids, campaign_id=args.campaign_id),
        "offer-cards-update": lambda: server.ym_offer_cards_update(args.cards_json, business_id=args.business_id),
        "offer-recommendations": lambda: server.ym_offer_recommendations(args.payload_json, business_id=args.business_id),
        "returns": lambda: server.ym_returns(page=args.page, campaign_id=args.campaign_id),
        "return": lambda: server.ym_return(args.order_id, args.return_id, campaign_id=args.campaign_id),
        "return-decision": lambda: server.ym_return_decision(args.order_id, args.return_id, campaign_id=args.campaign_id),
        "return-decision-set": lambda: server.ym_return_decision_set(args.order_id, args.return_id, args.decision_json, campaign_id=args.campaign_id),
        "return-decision-submit": lambda: server.ym_return_decision_submit(args.order_id, args.return_id, campaign_id=args.campaign_id),
        "return-application": lambda: server.ym_return_application(args.order_id, args.return_id, args.output_path, campaign_id=args.campaign_id),
        "business-return-decisions": lambda: server.ym_business_return_decisions(args.payload_json, business_id=args.business_id),
        "return-create": lambda: server.ym_return_create(args.return_json, campaign_id=args.campaign_id),
        "return-cancel": lambda: server.ym_return_cancel(args.return_json, campaign_id=args.campaign_id),
        "shipments": lambda: server.ym_shipments(campaign_id=args.campaign_id),
        "shipment": lambda: server.ym_shipment(args.shipment_id, campaign_id=args.campaign_id),
        "shipments-search": lambda: server.ym_shipments_search(args.payload_json, campaign_id=args.campaign_id),
        "shipment-update": lambda: server.ym_shipment_update(args.shipment_id, args.payload_json, campaign_id=args.campaign_id),
        "shipment-confirm": lambda: server.ym_shipment_confirm(args.shipment_id, campaign_id=args.campaign_id),
        "shipment-orders": lambda: server.ym_shipment_orders(args.shipment_id, campaign_id=args.campaign_id),
        "shipment-transfer": lambda: server.ym_shipment_transfer(args.shipment_id, args.payload_json, campaign_id=args.campaign_id),
        "shipment-act": lambda: server.ym_shipment_act(args.shipment_id, args.output_path, campaign_id=args.campaign_id),
        "shipment-inbound-act": lambda: server.ym_shipment_inbound_act(args.shipment_id, args.output_path, campaign_id=args.campaign_id),
        "shipment-waybill": lambda: server.ym_shipment_waybill(args.shipment_id, args.output_path, campaign_id=args.campaign_id),
        "shipment-discrepancy-act": lambda: server.ym_shipment_discrepancy_act(args.shipment_id, args.output_path, campaign_id=args.campaign_id),
        "shipment-pallets": lambda: server.ym_shipment_pallets(args.shipment_id, campaign_id=args.campaign_id),
        "shipment-pallets-update": lambda: server.ym_shipment_pallets_update(args.shipment_id, args.pallets_json, campaign_id=args.campaign_id),
        "shipment-pallet-labels": lambda: server.ym_shipment_pallet_labels(args.shipment_id, args.output_path, campaign_id=args.campaign_id),
        "feedbacks": lambda: server.ym_feedbacks(limit=args.limit, business_id=args.business_id),
        "feedback-skip": lambda: server.ym_feedback_skip(args.feedback_ids_json, business_id=args.business_id),
        "feedback-comments": lambda: server.ym_feedback_comments(args.feedback_id, business_id=args.business_id),
        "feedback-comment-update": lambda: server.ym_feedback_comment_update(args.comment_json, business_id=args.business_id),
        "feedback-comment-delete": lambda: server.ym_feedback_comment_delete(args.comment_id, business_id=args.business_id),
        "questions": lambda: server.ym_questions(business_id=args.business_id),
        "question-answer": lambda: server.ym_question_answer(args.answer_json, business_id=args.business_id),
        "question-update": lambda: server.ym_question_update(args.update_json, business_id=args.business_id),
        "quality": lambda: server.ym_quality_rating(business_id=args.business_id),
        "quality-details": lambda: server.ym_quality_details(campaign_id=args.campaign_id),
        "warehouses": lambda: server.ym_warehouses(business_id=args.business_id),
        "warehouse-status": lambda: server.ym_warehouse_status(args.enabled, campaign_id=args.campaign_id),
        "all-warehouses": lambda: server.ym_all_warehouses(),
        "logistics-points": lambda: server.ym_logistics_points(business_id=args.business_id),
        "reception-transfer-act": lambda: server.ym_reception_transfer_act(args.output_path, campaign_id=args.campaign_id),
        "outlets": lambda: server.ym_outlets(campaign_id=args.campaign_id),
        "outlet": lambda: server.ym_outlet(args.outlet_id, campaign_id=args.campaign_id),
        "outlet-create": lambda: server.ym_outlet_create(args.outlet_json, campaign_id=args.campaign_id),
        "outlet-update": lambda: server.ym_outlet_update(args.outlet_id, args.outlet_json, campaign_id=args.campaign_id),
        "outlet-delete": lambda: server.ym_outlet_delete(args.outlet_id, campaign_id=args.campaign_id),
        "outlet-licenses": lambda: server.ym_outlet_licenses(campaign_id=args.campaign_id),
        "delivery-services": lambda: server.ym_delivery_services(),
        "delivery-options": lambda: server.ym_delivery_options(args.payload_json, campaign_id=args.campaign_id),
        "return-delivery-options": lambda: server.ym_return_delivery_options(args.payload_json, campaign_id=args.campaign_id),
        "regions": lambda: server.ym_regions(name=args.name),
        "region": lambda: server.ym_region(args.region_id),
        "region-children": lambda: server.ym_region_children(args.region_id, page=args.page),
        "countries": lambda: server.ym_countries(),
        "categories": lambda: server.ym_categories(),
        "category-params": lambda: server.ym_category_params(args.category_id),
        "max-sale-quantum": lambda: server.ym_max_sale_quantum(args.payload_json),
        "tariffs": lambda: server.ym_tariffs(args.offers_json, campaign_id=args.campaign_id),
        "promos": lambda: server.ym_promos(business_id=args.business_id),
        "promo-offers": lambda: server.ym_promo_offers(args.promo_id, payload_json=args.payload_json, business_id=args.business_id),
        "promo-offers-update": lambda: server.ym_promo_offers_update(args.payload_json, business_id=args.business_id),
        "promo-offers-delete": lambda: server.ym_promo_offers_delete(args.payload_json, business_id=args.business_id),
        "bids": lambda: server.ym_bids(offer_ids=args.offer_ids, business_id=args.business_id),
        "bids-update": lambda: server.ym_bids_update(args.bids_json, business_id=args.business_id),
        "campaign-bids": lambda: server.ym_campaign_bids(offer_ids=args.offer_ids, limit=args.limit, campaign_id=args.campaign_id),
        "campaign-bids-update": lambda: server.ym_campaign_bids_update(args.bids_json, campaign_id=args.campaign_id),
        "bid-recommendations": lambda: server.ym_bid_recommendations(business_id=args.business_id),
        "chats": lambda: server.ym_chats(business_id=args.business_id),
        "chat-history": lambda: server.ym_chat_history(args.chat_id, limit=args.limit, business_id=args.business_id),
        "chat-send": lambda: server.ym_chat_send(args.chat_id, args.message, business_id=args.business_id),
        "chat-new": lambda: server.ym_chat_new(args.payload_json, business_id=args.business_id),
        "chat-file-send": lambda: server.ym_chat_file_send(args.chat_id, args.file_path, business_id=args.business_id),
        "report-status": lambda: server.ym_report_status(args.report_id),
        "report-generate": lambda: server.ym_report_generate(args.report_type, payload_json=args.payload_json),
        "report-barcodes": lambda: server.ym_report_barcodes(args.payload_json),
        "order-stats": lambda: server.ym_order_stats(date_from=args.date_from, date_to=args.date_to, campaign_id=args.campaign_id),
        "supply-requests": lambda: server.ym_supply_requests(campaign_id=args.campaign_id),
        "supply-request-items": lambda: server.ym_supply_request_items(campaign_id=args.campaign_id),
        "supply-request-documents": lambda: server.ym_supply_request_documents(args.output_path, campaign_id=args.campaign_id),
        "sku-stats": lambda: server.ym_sku_stats(campaign_id=args.campaign_id),
        "operations": lambda: server.ym_operations(business_id=args.business_id),
    }

    print(handlers[args.command]())
