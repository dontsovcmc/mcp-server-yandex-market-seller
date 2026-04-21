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

    # campaign-settings
    p = sub.add_parser("campaign-settings", help="Настройки кампании")
    p.add_argument("--campaign-id", type=int, default=0)

    # business-settings
    p = sub.add_parser("business-settings", help="Настройки бизнеса")
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

    # offers
    p = sub.add_parser("offers", help="Товары")
    p.add_argument("--offer-ids", default="")
    p.add_argument("--limit", type=int, default=200)
    p.add_argument("--business-id", type=int, default=0)

    # offer-cards
    p = sub.add_parser("offer-cards", help="Карточки товаров")
    p.add_argument("--offer-ids", default="")
    p.add_argument("--business-id", type=int, default=0)

    # prices
    p = sub.add_parser("prices", help="Цены")
    p.add_argument("--offer-ids", default="")
    p.add_argument("--limit", type=int, default=200)
    p.add_argument("--business-id", type=int, default=0)

    # price-quarantine
    p = sub.add_parser("price-quarantine", help="Карантин цен")
    p.add_argument("--business-id", type=int, default=0)

    # stocks
    p = sub.add_parser("stocks", help="Остатки")
    p.add_argument("--limit", type=int, default=200)
    p.add_argument("--campaign-id", type=int, default=0)

    # hidden-offers
    p = sub.add_parser("hidden-offers", help="Скрытые товары")
    p.add_argument("--campaign-id", type=int, default=0)

    # returns
    p = sub.add_parser("returns", help="Возвраты")
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--campaign-id", type=int, default=0)

    # shipments
    p = sub.add_parser("shipments", help="Отгрузки")
    p.add_argument("--campaign-id", type=int, default=0)

    # shipment
    p = sub.add_parser("shipment", help="Отгрузка")
    p.add_argument("shipment_id", type=int)
    p.add_argument("--campaign-id", type=int, default=0)

    # feedbacks
    p = sub.add_parser("feedbacks", help="Отзывы")
    p.add_argument("--limit", type=int, default=200)
    p.add_argument("--business-id", type=int, default=0)

    # questions
    p = sub.add_parser("questions", help="Вопросы")
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

    # all-warehouses
    sub.add_parser("all-warehouses", help="Все склады Маркета")

    # logistics-points
    p = sub.add_parser("logistics-points", help="Точки сдачи")
    p.add_argument("--business-id", type=int, default=0)

    # outlets
    p = sub.add_parser("outlets", help="Точки продаж")
    p.add_argument("--campaign-id", type=int, default=0)

    # delivery-services
    sub.add_parser("delivery-services", help="Службы доставки")

    # regions
    p = sub.add_parser("regions", help="Регионы")
    p.add_argument("name", nargs="?", default="")

    # countries
    sub.add_parser("countries", help="Страны")

    # categories
    sub.add_parser("categories", help="Категории")

    # promos
    p = sub.add_parser("promos", help="Акции")
    p.add_argument("--business-id", type=int, default=0)

    # bids
    p = sub.add_parser("bids", help="Ставки")
    p.add_argument("--offer-ids", default="")
    p.add_argument("--business-id", type=int, default=0)

    # bid-recommendations
    p = sub.add_parser("bid-recommendations", help="Рекомендации ставок")
    p.add_argument("--business-id", type=int, default=0)

    # chats
    p = sub.add_parser("chats", help="Чаты")
    p.add_argument("--business-id", type=int, default=0)

    # report-status
    p = sub.add_parser("report-status", help="Статус отчёта")
    p.add_argument("report_id")

    # supply-requests
    p = sub.add_parser("supply-requests", help="Заявки на поставку")
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
        "campaign-settings": lambda: server.ym_campaign_settings(campaign_id=args.campaign_id),
        "business-settings": lambda: server.ym_business_settings(business_id=args.business_id),
        "orders": lambda: server.ym_orders(status=args.status, page=args.page, page_size=args.page_size, campaign_id=args.campaign_id),
        "order": lambda: server.ym_order(args.order_id, campaign_id=args.campaign_id),
        "order-items": lambda: server.ym_order_items(args.order_id, campaign_id=args.campaign_id),
        "order-buyer": lambda: server.ym_order_buyer(args.order_id, campaign_id=args.campaign_id),
        "order-tracking": lambda: server.ym_order_tracking(args.order_id, campaign_id=args.campaign_id),
        "offers": lambda: server.ym_offers(offer_ids=args.offer_ids, limit=args.limit, business_id=args.business_id),
        "offer-cards": lambda: server.ym_offer_cards(offer_ids=args.offer_ids, business_id=args.business_id),
        "prices": lambda: server.ym_prices(offer_ids=args.offer_ids, limit=args.limit, business_id=args.business_id),
        "price-quarantine": lambda: server.ym_price_quarantine(business_id=args.business_id),
        "stocks": lambda: server.ym_stocks(limit=args.limit, campaign_id=args.campaign_id),
        "hidden-offers": lambda: server.ym_hidden_offers(campaign_id=args.campaign_id),
        "returns": lambda: server.ym_returns(page=args.page, campaign_id=args.campaign_id),
        "shipments": lambda: server.ym_shipments(campaign_id=args.campaign_id),
        "shipment": lambda: server.ym_shipment(args.shipment_id, campaign_id=args.campaign_id),
        "feedbacks": lambda: server.ym_feedbacks(limit=args.limit, business_id=args.business_id),
        "questions": lambda: server.ym_questions(business_id=args.business_id),
        "quality": lambda: server.ym_quality_rating(business_id=args.business_id),
        "quality-details": lambda: server.ym_quality_details(campaign_id=args.campaign_id),
        "warehouses": lambda: server.ym_warehouses(business_id=args.business_id),
        "all-warehouses": lambda: server.ym_all_warehouses(),
        "logistics-points": lambda: server.ym_logistics_points(business_id=args.business_id),
        "outlets": lambda: server.ym_outlets(campaign_id=args.campaign_id),
        "delivery-services": lambda: server.ym_delivery_services(),
        "regions": lambda: server.ym_regions(name=args.name),
        "countries": lambda: server.ym_countries(),
        "categories": lambda: server.ym_categories(),
        "promos": lambda: server.ym_promos(business_id=args.business_id),
        "bids": lambda: server.ym_bids(offer_ids=args.offer_ids, business_id=args.business_id),
        "bid-recommendations": lambda: server.ym_bid_recommendations(business_id=args.business_id),
        "chats": lambda: server.ym_chats(business_id=args.business_id),
        "report-status": lambda: server.ym_report_status(args.report_id),
        "supply-requests": lambda: server.ym_supply_requests(campaign_id=args.campaign_id),
        "sku-stats": lambda: server.ym_sku_stats(campaign_id=args.campaign_id),
        "operations": lambda: server.ym_operations(business_id=args.business_id),
    }

    print(handlers[args.command]())
