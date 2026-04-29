<!-- mcp-name: io.github.dontsovcmc/yandex-market-seller -->

# mcp-server-yandex-market-seller

[![Version](https://img.shields.io/badge/version-0.4.0-blue)](https://github.com/dontsovcmc/mcp-server-yandex-market-seller)

MCP-сервер для работы с [Yandex Market Partner API](https://yandex.ru/dev/market/partner-api/doc/) через Claude Code, Claude Desktop и другие MCP-совместимые клиенты.

API клиент написан по [OpenAPI спецификации](https://github.com/yandex-market/yandex-market-partner-api/blob/master/openapi/openapi.yaml) из официального репозитория Яндекс Маркета.

Все данные остаются на вашем компьютере — токен никуда не передаётся.

**131 инструмент** — полное покрытие Yandex Market Partner API.

## Возможности

### Кампании и настройки
| Инструмент | Описание |
|------------|----------|
| `ym_campaigns` | Список кампаний (магазинов) |
| `ym_campaign` | Информация о кампании |
| `ym_campaign_settings` | Настройки кампании |
| `ym_campaign_settings_update` | Обновить настройки кампании |
| `ym_business_settings` | Настройки бизнеса |
| `ym_business_settings_update` | Обновить настройки бизнеса |

### Заказы
| Инструмент | Описание |
|------------|----------|
| `ym_orders` | Список заказов (фильтр по статусу) |
| `ym_order` | Подробная информация о заказе |
| `ym_order_status` | Обновить статус заказа |
| `ym_order_status_batch` | Пакетное обновление статусов |
| `ym_order_labels` | Скачать этикетки заказа (PDF) |
| `ym_order_labels_data` | Данные этикеток (JSON) |
| `ym_order_box_label` | Скачать этикетку коробки (PDF) |
| `ym_order_items` | Позиции заказа |
| `ym_order_items_update` | Обновить позиции заказа |
| `ym_order_boxes` | Коробки заказа |
| `ym_order_boxes_update` | Обновить коробки заказа |
| `ym_order_shipment_boxes` | Установить коробки отгрузки |
| `ym_order_cancel_accept` | Принять отмену заказа |
| `ym_order_delivery_date` | Установить дату доставки |
| `ym_order_tracking` | Трекинг заказа |
| `ym_order_tracking_update` | Установить трек-номера |
| `ym_order_buyer` | Информация о покупателе |
| `ym_order_business_buyer` | Юрлицо покупателя |
| `ym_order_verify_eac` | Проверить код подтверждения (EAC) |
| `ym_order_storage_limit` | Срок хранения заказа |
| `ym_order_storage_limit_update` | Установить срок хранения |
| `ym_order_deliver_digital` | Передать цифровые товары |
| `ym_order_documents` | Документы заказа |
| `ym_order_document_create` | Создать документ заказа |
| `ym_business_orders` | Заказы бизнеса (v1) |
| `ym_order_create` | Создать заказ (v1) |
| `ym_order_update_v1` | Обновить заказ (v1) |
| `ym_order_update_options` | Обновить опции заказа (v1) |
| `ym_order_stats` | Статистика заказов за период |

### Возвраты
| Инструмент | Описание |
|------------|----------|
| `ym_returns` | Список возвратов |
| `ym_return` | Подробности возврата |
| `ym_return_decision` | Решение по возврату |
| `ym_return_decision_set` | Установить решение по возврату |
| `ym_return_decision_submit` | Подтвердить решение по возврату |
| `ym_return_application` | Скачать заявление на возврат (PDF) |
| `ym_business_return_decisions` | Решения по возвратам бизнеса (v1) |
| `ym_return_create` | Создать возврат (v1) |
| `ym_return_cancel` | Отменить возврат (v1) |

### Отгрузки
| Инструмент | Описание |
|------------|----------|
| `ym_shipments` | Список отгрузок |
| `ym_shipments_search` | Поиск отгрузок |
| `ym_shipment` | Подробности отгрузки |
| `ym_shipment_update` | Обновить отгрузку |
| `ym_shipment_confirm` | Подтвердить отгрузку |
| `ym_shipment_orders` | Заказы в отгрузке |
| `ym_shipment_transfer` | Перенести заказы в отгрузку |
| `ym_shipment_act` | Скачать акт отгрузки (PDF) |
| `ym_shipment_inbound_act` | Скачать входящий акт (PDF) |
| `ym_shipment_waybill` | Скачать транспортную накладную (PDF) |
| `ym_shipment_discrepancy_act` | Скачать акт расхождений (PDF) |
| `ym_shipment_pallets` | Паллеты отгрузки |
| `ym_shipment_pallets_update` | Установить паллеты |
| `ym_shipment_pallet_labels` | Скачать ярлыки паллетов (PDF) |

### Товары
| Инструмент | Описание |
|------------|----------|
| `ym_offers` | Список товаров (offer-mappings) |
| `ym_offers_update` | Обновить описания товаров |
| `ym_offers_delete` | Удалить товары из каталога |
| `ym_offers_archive` | Архивировать / разархивировать товары |
| `ym_generate_barcodes` | Сгенерировать штрихкоды |
| `ym_campaign_offers` | Товары кампании с ценами и остатками |
| `ym_hidden_offers` | Скрытые товары |
| `ym_unhide_offers` | Показать скрытые товары |
| `ym_offer_cards` | Карточки товаров |
| `ym_offer_cards_update` | Обновить карточки товаров |
| `ym_offer_recommendations` | Рекомендации по товарам |

### Цены
| Инструмент | Описание |
|------------|----------|
| `ym_prices` | Получить цены товаров |
| `ym_prices_update` | Обновить цены |
| `ym_price_quarantine` | Товары в карантине цен |
| `ym_price_quarantine_confirm` | Подтвердить цены из карантина |
| `ym_campaign_price_quarantine` | Карантин цен кампании |
| `ym_campaign_price_quarantine_confirm` | Подтвердить цены карантина кампании |

### Остатки
| Инструмент | Описание |
|------------|----------|
| `ym_stocks` | Получить остатки |
| `ym_stocks_update` | Обновить остатки |

### Промоакции и ставки
| Инструмент | Описание |
|------------|----------|
| `ym_promos` | Список акций |
| `ym_promo_offers` | Товары в акции |
| `ym_promo_offers_update` | Добавить товары в акцию |
| `ym_promo_offers_delete` | Убрать товары из акции |
| `ym_bids` | Получить ставки (бизнес) |
| `ym_bids_update` | Обновить ставки (бизнес) |
| `ym_campaign_bids` | Получить ставки (кампания) |
| `ym_campaign_bids_update` | Обновить ставки (кампания) |
| `ym_bid_recommendations` | Рекомендации по ставкам |

### Склады и доставка
| Инструмент | Описание |
|------------|----------|
| `ym_warehouses` | Склады бизнеса |
| `ym_all_warehouses` | Все склады Маркета |
| `ym_warehouse_status` | Включить/выключить склад |
| `ym_reception_transfer_act` | Скачать акт приёма-передачи (PDF) |
| `ym_delivery_services` | Службы доставки |
| `ym_delivery_options` | Варианты доставки |
| `ym_return_delivery_options` | Варианты доставки возврата |
| `ym_logistics_points` | Точки сдачи |

### Покупатели
| Инструмент | Описание |
|------------|----------|
| `ym_feedbacks` | Отзывы о товарах |
| `ym_feedback_skip` | Пропустить реакцию на отзыв |
| `ym_feedback_comments` | Комментарии к отзыву |
| `ym_feedback_comment_update` | Обновить комментарий к отзыву |
| `ym_feedback_comment_delete` | Удалить комментарий к отзыву |
| `ym_questions` | Вопросы о товарах |
| `ym_question_answer` | Ответить на вопрос |
| `ym_question_update` | Обновить ответ |
| `ym_chats` | Чаты с покупателями |
| `ym_chat_history` | История сообщений чата |
| `ym_chat_send` | Отправить сообщение в чат |
| `ym_chat_new` | Создать чат |
| `ym_chat_file_send` | Отправить файл в чат |

### Точки продаж
| Инструмент | Описание |
|------------|----------|
| `ym_outlets` | Список точек продаж |
| `ym_outlet` | Подробности точки продаж |
| `ym_outlet_create` | Создать точку продаж |
| `ym_outlet_update` | Обновить точку продаж |
| `ym_outlet_delete` | Удалить точку продаж |
| `ym_outlet_licenses` | Лицензии точек продаж |

### Аналитика и отчёты
| Инструмент | Описание |
|------------|----------|
| `ym_quality_rating` | Рейтинг качества |
| `ym_quality_details` | Детали рейтинга качества |
| `ym_report_status` | Статус генерации отчёта |
| `ym_report_generate` | Сгенерировать отчёт |
| `ym_report_barcodes` | Отчёт по штрихкодам (v1) |
| `ym_order_stats` | Статистика заказов |
| `ym_sku_stats` | Статистика по SKU |
| `ym_tariffs` | Рассчитать тарифы |

### Справочники
| Инструмент | Описание |
|------------|----------|
| `ym_regions` | Поиск регионов |
| `ym_region` | Регион по ID |
| `ym_region_children` | Дочерние регионы |
| `ym_countries` | Список стран |
| `ym_categories` | Дерево категорий Маркета |
| `ym_category_params` | Параметры категории |
| `ym_max_sale_quantum` | Макс. квант продажи |

### Прочее
| Инструмент | Описание |
|------------|----------|
| `ym_supply_requests` | Заявки на поставку |
| `ym_supply_request_items` | Товары в заявке на поставку |
| `ym_supply_request_documents` | Скачать документы заявки (PDF) |
| `ym_operations` | Асинхронные операции |

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

Каждый tool также принимает `campaign_id`/`business_id` как параметр — это позволяет работать с несколькими магазинами в одной сессии.

### Шаг 4. Проверить

Попросите Claude: *«покажи мои заказы на Маркете»* — он вызовет `ym_orders`.

## Примеры (MCP)

### Заказы
- «покажи заказы» → `ym_orders`
- «покажи необработанные заказы» → `ym_orders` (status=PROCESSING)
- «что с заказом 12345?» → `ym_order`
- «отправь заказ 12345» → `ym_order_status` (status=DELIVERY)
- «скачай этикетки для заказа 12345» → `ym_order_labels`
- «покажи статистику заказов за апрель» → `ym_order_stats`

### Товары и цены
- «покажи мои товары» → `ym_offers`
- «какие цены на товар SKU1?» → `ym_prices`
- «обнови цену SKU1 до 2000 руб.» → `ym_prices_update`
- «сколько остатков SKU1?» → `ym_stocks`
- «обнови остатки SKU1 до 50 шт.» → `ym_stocks_update`

### Акции и ставки
- «какие акции сейчас?» → `ym_promos`
- «покажи товары в акции» → `ym_promo_offers`
- «добавь товар в акцию» → `ym_promo_offers_update`
- «покажи текущие ставки» → `ym_bids`

### Покупатели
- «покажи возвраты» → `ym_returns`
- «покажи отзывы» → `ym_feedbacks`
- «покажи чаты с покупателями» → `ym_chats`
- «ответь на вопрос о товаре» → `ym_question_answer`

### Аналитика
- «покажи рейтинг качества» → `ym_quality_rating`
- «рассчитай тарифы» → `ym_tariffs`
- «сгенерируй отчёт united-netting» → `ym_report_generate`

## CLI-режим

Без аргументов запускается MCP-сервер, с командой — CLI. Все команды выводят JSON.

```bash
# Версия
mcp-server-yandex-market-seller --version

# Кампании
mcp-server-yandex-market-seller campaigns
mcp-server-yandex-market-seller campaign
mcp-server-yandex-market-seller campaign-settings
mcp-server-yandex-market-seller business-settings

# Заказы
mcp-server-yandex-market-seller orders
mcp-server-yandex-market-seller orders --status PROCESSING
mcp-server-yandex-market-seller order 12345
mcp-server-yandex-market-seller order-status 12345 DELIVERY
mcp-server-yandex-market-seller order-labels 12345 labels.pdf
mcp-server-yandex-market-seller order-items 12345
mcp-server-yandex-market-seller order-buyer 12345
mcp-server-yandex-market-seller order-tracking 12345
mcp-server-yandex-market-seller order-documents 12345
mcp-server-yandex-market-seller order-stats --date-from 2026-04-01

# Возвраты
mcp-server-yandex-market-seller returns
mcp-server-yandex-market-seller return 12345 67890

# Отгрузки
mcp-server-yandex-market-seller shipments
mcp-server-yandex-market-seller shipment 12345
mcp-server-yandex-market-seller shipment-orders 12345
mcp-server-yandex-market-seller shipment-act 12345 act.pdf

# Товары
mcp-server-yandex-market-seller offers
mcp-server-yandex-market-seller offers --offer-ids SKU1,SKU2
mcp-server-yandex-market-seller offer-cards
mcp-server-yandex-market-seller campaign-offers
mcp-server-yandex-market-seller hidden-offers

# Цены и остатки
mcp-server-yandex-market-seller prices
mcp-server-yandex-market-seller prices --offer-ids SKU1
mcp-server-yandex-market-seller price-quarantine
mcp-server-yandex-market-seller stocks

# Акции и ставки
mcp-server-yandex-market-seller promos
mcp-server-yandex-market-seller promo-offers cf_137460
mcp-server-yandex-market-seller promo-offers-update '{"promoId":"cf_137460","offers":[{"offerId":"SKU1","params":{"discountParams":{"price":6500,"promoPrice":4900}}}]}'
mcp-server-yandex-market-seller promo-offers-delete '{"promoId":"cf_137460","offers":[{"offerId":"SKU1"}]}'
mcp-server-yandex-market-seller bids
mcp-server-yandex-market-seller bid-recommendations

# Склады и доставка
mcp-server-yandex-market-seller warehouses
mcp-server-yandex-market-seller all-warehouses
mcp-server-yandex-market-seller logistics-points
mcp-server-yandex-market-seller delivery-services

# Покупатели
mcp-server-yandex-market-seller feedbacks
mcp-server-yandex-market-seller feedback-comments 12345
mcp-server-yandex-market-seller questions
mcp-server-yandex-market-seller chats
mcp-server-yandex-market-seller chat-history 12345
mcp-server-yandex-market-seller chat-send 12345 "Ваш заказ отправлен"

# Точки продаж
mcp-server-yandex-market-seller outlets
mcp-server-yandex-market-seller outlet 12345

# Аналитика
mcp-server-yandex-market-seller quality
mcp-server-yandex-market-seller quality-details
mcp-server-yandex-market-seller sku-stats
mcp-server-yandex-market-seller report-status abc123

# Справочники
mcp-server-yandex-market-seller regions Москва
mcp-server-yandex-market-seller region 213
mcp-server-yandex-market-seller countries
mcp-server-yandex-market-seller categories
mcp-server-yandex-market-seller category-params 12345

# Поставки
mcp-server-yandex-market-seller supply-requests
mcp-server-yandex-market-seller operations
```

## Лицензия

MIT
