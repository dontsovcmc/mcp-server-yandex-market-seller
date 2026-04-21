<!-- mcp-name: io.github.dontsovcmc/yandex-market-seller -->

# mcp-server-yandex-market-seller

MCP-сервер для работы с [Yandex Market Partner API](https://yandex.ru/dev/market/partner-api/doc/) через Claude Code, Claude Desktop и другие MCP-совместимые клиенты.

API клиент написан по [OpenAPI спецификации](https://github.com/yandex-market/yandex-market-partner-api/blob/master/openapi/openapi.yaml) из официального репозитория Яндекс Маркета.

Все данные остаются на вашем компьютере — токен никуда не передаётся.

## Возможности

### Заказы
| Инструмент | Описание |
|------------|----------|
| `ym_orders` | Список заказов (с фильтром по статусу) |
| `ym_order` | Подробная информация о заказе |
| `ym_order_status` | Обновить статус заказа |
| `ym_order_labels` | Скачать этикетки заказа (PDF) |
| `ym_order_stats` | Статистика заказов за период |

### Товары
| Инструмент | Описание |
|------------|----------|
| `ym_offers` | Список товаров из каталога (offer-mappings) |
| `ym_offers_update` | Обновить описания и параметры товаров |
| `ym_offers_delete` | Удалить товары из каталога |
| `ym_offers_archive` | Архивировать / разархивировать товары |
| `ym_campaign_offers` | Товары кампании с ценами и остатками |
| `ym_hidden_offers` | Скрытые товары |
| `ym_unhide_offers` | Показать скрытые товары |

### Цены и остатки
| Инструмент | Описание |
|------------|----------|
| `ym_prices` | Получить цены товаров |
| `ym_prices_update` | Обновить цены |
| `ym_stocks` | Получить остатки |
| `ym_stocks_update` | Обновить остатки |

### Магазин и аналитика
| Инструмент | Описание |
|------------|----------|
| `ym_campaigns` | Список кампаний (магазинов) |
| `ym_campaign` | Информация о кампании |
| `ym_warehouses` | Склады бизнеса |
| `ym_quality_rating` | Рейтинг качества |
| `ym_promos` | Промоакции |
| `ym_bids` | Получить ставки |
| `ym_bids_update` | Обновить ставки |
| `ym_tariffs` | Рассчитать тарифы на услуги |

### Покупатели
| Инструмент | Описание |
|------------|----------|
| `ym_returns` | Список возвратов |
| `ym_return` | Подробности возврата |
| `ym_feedbacks` | Отзывы о товарах |
| `ym_chats` | Чаты с покупателями |
| `ym_chat_history` | История сообщений чата |
| `ym_chat_send` | Отправить сообщение в чат |

### Справочники
| Инструмент | Описание |
|------------|----------|
| `ym_regions` | Поиск регионов |
| `ym_categories` | Дерево категорий Маркета |
| `ym_category_params` | Параметры категории |

## Настройка

### Шаг 1. Получить API-ключ

1. Откройте [личный кабинет Яндекс Маркета](https://partner.market.yandex.ru)
2. Перейдите в **Настройки** → **API-ключи**
3. Создайте новый ключ с нужными правами
4. Скопируйте API-ключ

Альтернативно можно использовать [OAuth-токен](https://oauth.yandex.ru/).

### Шаг 2. Узнать ID кампании и бизнеса

```bash
# После установки и настройки токена:
mcp-server-yandex-market-seller campaigns
```

Запишите `campaignId` и `businessId` из вывода.

### Шаг 3. Подключить MCP-сервер

#### Claude Code (CLI в терминале)

**Способ 1: через uvx** (не требует установки пакета)

```bash
claude mcp add yandex-market-seller \
  -e YM_TOKEN=ваш_api_ключ \
  -e YM_CAMPAIGN_ID=12345 \
  -e YM_BUSINESS_ID=67890 \
  -- uvx mcp-server-yandex-market-seller
```

**Способ 2: через pip**

```bash
pip install mcp-server-yandex-market-seller

claude mcp add yandex-market-seller \
  -e YM_TOKEN=ваш_api_ключ \
  -e YM_CAMPAIGN_ID=12345 \
  -e YM_BUSINESS_ID=67890 \
  -- python -m mcp_server_yandex_market_seller
```

Для удаления:
```bash
claude mcp remove yandex-market-seller
```

#### Claude Desktop (десктопное приложение)

Добавьте в конфигурационный файл:

| Клиент | ОС | Путь к файлу |
|--------|----|-------------|
| Claude Code | все | `~/.claude/settings.json` (секция `mcpServers`) |
| Claude Desktop | macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Claude Desktop | Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| Claude Desktop | Linux | `~/.config/Claude/claude_desktop_config.json` |

```json
{
  "mcpServers": {
    "yandex-market-seller": {
      "command": "uvx",
      "args": ["mcp-server-yandex-market-seller"],
      "env": {
        "YM_TOKEN": "ваш_api_ключ",
        "YM_CAMPAIGN_ID": "12345",
        "YM_BUSINESS_ID": "67890"
      }
    }
  }
}
```

### Переменные окружения

| Переменная | Обязательная | Описание |
|-----------|:-----------:|----------|
| `YM_TOKEN` | да | API-ключ или OAuth-токен |
| `YM_AUTH_TYPE` | нет | `api-key` (по умолчанию) или `oauth` |
| `YM_CAMPAIGN_ID` | да | ID кампании (магазина) |
| `YM_BUSINESS_ID` | да | ID бизнеса |

Все переменные можно задать как через env, так и через настройки Claude (секция `env` в конфиге MCP-сервера). Каждый tool также принимает `campaign_id`/`business_id` как параметр — это позволяет работать с несколькими магазинами в одной сессии.

### Шаг 4. Проверить

Попросите Claude: *«покажи мои заказы на Маркете»* — он вызовет `ym_orders`.

## API спецификация

Клиент написан по [OpenAPI спецификации Yandex Market Partner API](https://github.com/yandex-market/yandex-market-partner-api/blob/master/openapi/openapi.yaml):

```
https://github.com/yandex-market/yandex-market-partner-api/blob/master/openapi/openapi.yaml
```

Для генерации клиента на других языках используйте OpenAPI Generator:
```bash
# Python
openapi-python-client generate \
  --url https://raw.githubusercontent.com/yandex-market/yandex-market-partner-api/master/openapi/openapi.yaml

# Другие языки
openapi-generator generate -i openapi.yaml -g <язык> -o ./generated
```

## Примеры (MCP)

- «покажи заказы» → `ym_orders`
- «покажи необработанные заказы» → `ym_orders` (status=PROCESSING)
- «что с заказом 12345?» → `ym_order`
- «отправь заказ 12345» → `ym_order_status` (status=DELIVERY)
- «скачай этикетки для заказа 12345» → `ym_order_labels`
- «покажи мои товары» → `ym_offers`
- «какие цены на товар SKU1?» → `ym_prices`
- «обнови цену SKU1 до 2000 руб.» → `ym_prices_update`
- «сколько остатков SKU1?» → `ym_stocks`
- «обнови остатки SKU1 до 50 шт.» → `ym_stocks_update`
- «покажи возвраты» → `ym_returns`
- «покажи отзывы» → `ym_feedbacks`
- «покажи рейтинг качества» → `ym_quality_rating`
- «какие акции сейчас?» → `ym_promos`
- «покажи чаты с покупателями» → `ym_chats`

## CLI-режим

Без аргументов запускается MCP-сервер, с командой — CLI.

### Команды

```bash
# Кампании
mcp-server-yandex-market-seller campaigns

# Заказы
mcp-server-yandex-market-seller orders
mcp-server-yandex-market-seller orders --status PROCESSING
mcp-server-yandex-market-seller order 12345

# Товары
mcp-server-yandex-market-seller offers
mcp-server-yandex-market-seller offers --offer-ids SKU1,SKU2

# Цены и остатки
mcp-server-yandex-market-seller prices
mcp-server-yandex-market-seller stocks

# Возвраты и отзывы
mcp-server-yandex-market-seller returns
mcp-server-yandex-market-seller feedbacks

# Рейтинг и склады
mcp-server-yandex-market-seller quality
mcp-server-yandex-market-seller warehouses

# Справочники
mcp-server-yandex-market-seller regions Москва
mcp-server-yandex-market-seller categories

# Промоакции и чаты
mcp-server-yandex-market-seller promos
mcp-server-yandex-market-seller chats
```

Все команды выводят результат в JSON.

## Лицензия

MIT
