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
    sub.add_parser("campaigns", help="Список кампаний (магазинов)")

    # orders
    p_orders = sub.add_parser("orders", help="Список заказов")
    p_orders.add_argument("--status", default="", help="Фильтр по статусу")
    p_orders.add_argument("--page", type=int, default=1)
    p_orders.add_argument("--page-size", type=int, default=50)
    p_orders.add_argument("--campaign-id", type=int, default=0)

    # order
    p_order = sub.add_parser("order", help="Информация о заказе")
    p_order.add_argument("order_id", type=int)
    p_order.add_argument("--campaign-id", type=int, default=0)

    # offers
    p_offers = sub.add_parser("offers", help="Список товаров")
    p_offers.add_argument("--offer-ids", default="", help="IDs через запятую")
    p_offers.add_argument("--limit", type=int, default=200)
    p_offers.add_argument("--business-id", type=int, default=0)

    # prices
    p_prices = sub.add_parser("prices", help="Цены товаров")
    p_prices.add_argument("--offer-ids", default="")
    p_prices.add_argument("--limit", type=int, default=200)
    p_prices.add_argument("--business-id", type=int, default=0)

    # stocks
    p_stocks = sub.add_parser("stocks", help="Остатки товаров")
    p_stocks.add_argument("--limit", type=int, default=200)
    p_stocks.add_argument("--campaign-id", type=int, default=0)

    # returns
    p_returns = sub.add_parser("returns", help="Список возвратов")
    p_returns.add_argument("--page", type=int, default=1)
    p_returns.add_argument("--campaign-id", type=int, default=0)

    # feedbacks
    p_fb = sub.add_parser("feedbacks", help="Отзывы о товарах")
    p_fb.add_argument("--limit", type=int, default=200)
    p_fb.add_argument("--business-id", type=int, default=0)

    # quality
    p_quality = sub.add_parser("quality", help="Рейтинг качества")
    p_quality.add_argument("--business-id", type=int, default=0)

    # warehouses
    p_wh = sub.add_parser("warehouses", help="Склады")
    p_wh.add_argument("--business-id", type=int, default=0)

    # regions
    p_regions = sub.add_parser("regions", help="Поиск регионов")
    p_regions.add_argument("name", nargs="?", default="", help="Название региона")

    # categories
    sub.add_parser("categories", help="Дерево категорий")

    # promos
    p_promos = sub.add_parser("promos", help="Промоакции")
    p_promos.add_argument("--business-id", type=int, default=0)

    # chats
    p_chats = sub.add_parser("chats", help="Чаты с покупателями")
    p_chats.add_argument("--business-id", type=int, default=0)

    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        sys.exit(1)

    handlers = {
        "campaigns": lambda: server.ym_campaigns(),
        "orders": lambda: server.ym_orders(
            status=args.status, page=args.page, page_size=args.page_size,
            campaign_id=args.campaign_id,
        ),
        "order": lambda: server.ym_order(args.order_id, campaign_id=args.campaign_id),
        "offers": lambda: server.ym_offers(
            offer_ids=args.offer_ids, limit=args.limit, business_id=args.business_id,
        ),
        "prices": lambda: server.ym_prices(
            offer_ids=args.offer_ids, limit=args.limit, business_id=args.business_id,
        ),
        "stocks": lambda: server.ym_stocks(limit=args.limit, campaign_id=args.campaign_id),
        "returns": lambda: server.ym_returns(page=args.page, campaign_id=args.campaign_id),
        "feedbacks": lambda: server.ym_feedbacks(limit=args.limit, business_id=args.business_id),
        "quality": lambda: server.ym_quality_rating(business_id=args.business_id),
        "warehouses": lambda: server.ym_warehouses(business_id=args.business_id),
        "regions": lambda: server.ym_regions(name=args.name),
        "categories": lambda: server.ym_categories(),
        "promos": lambda: server.ym_promos(business_id=args.business_id),
        "chats": lambda: server.ym_chats(business_id=args.business_id),
    }

    print(handlers[args.command]())
