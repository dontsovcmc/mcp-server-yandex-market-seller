# CLAUDE.md

## Разработка

**CRITICAL: Все правила разработки описаны в [development.md](development.md). Всегда следовать им при любых изменениях кода, тестов и документации.**

### Запуск из исходников

```bash
pip install -e ".[test]"
```

### Запуск тестов

```bash
pytest tests/ -v
```

Тесты мокают API Яндекс Маркета — `YM_TOKEN` не нужен. Все тесты проходят локально без доступа к реальному API.

### CI

GitHub Actions: `.github/workflows/test.yml`, `runs-on: self-hosted`. Токен не требуется.

### Структура

```
src/mcp_server_yandex_market_seller/
├── __init__.py          # main(), версия
├── __main__.py          # python -m entry point
├── server.py            # FastMCP, все tools
├── ym_api.py            # HTTP-клиент Yandex Market Partner API
└── cli.py               # CLI-интерфейс
```

### API Яндекс Маркета

- Документация: https://yandex.ru/dev/market/partner-api/doc/
- OpenAPI spec: https://github.com/yandex-market/yandex-market-partner-api/blob/master/openapi/openapi.yaml
- Base URL: `https://api.partner.market.yandex.ru`
- Авторизация: `Api-Key` header (по умолчанию) или OAuth 2.0 Bearer token

### Работа с заказами

Типичный workflow:
1. `ym_orders` (status=PROCESSING) — получить новые заказы
2. `ym_order` — просмотреть детали заказа
3. `ym_order_labels` — скачать этикетки
4. `ym_order_status` (status=DELIVERY) — подтвердить отправку

Статусы заказов: UNPAID, PROCESSING, DELIVERY, PICKUP, DELIVERED, CANCELLED.

### Работа с товарами

- **Business-level** (`business_id`): offer-mappings, карточки, цены бизнеса, ставки
- **Campaign-level** (`campaign_id`): offers кампании, остатки, цены кампании, скрытые товары

### ID-шники

- `campaign_id` — ID кампании (магазина) в Маркете
- `business_id` — ID бизнеса (объединяет несколько кампаний)
- Оба можно задать через env (`YM_CAMPAIGN_ID`, `YM_BUSINESS_ID`) или передать в каждый tool

### Обновление MCP-сервера

Когда пользователь просит "обнови mcp yandex-market-seller":

1. Определить способ установки:
   ```bash
   which mcp-server-yandex-market-seller && pip show mcp-server-yandex-market-seller
   ```
2. Обновить пакет:
   - **pip:** `pip install --upgrade mcp-server-yandex-market-seller`
   - **uvx:** `uvx --upgrade mcp-server-yandex-market-seller`
3. Проверить версию:
   ```bash
   mcp-server-yandex-market-seller --version
   ```
4. Сообщить пользователю новую версию и попросить перезапустить Claude Code.

### Правила

- **CRITICAL: НИКОГДА не коммить в master/main!** Все коммиты — только в рабочую ветку.
- **Все изменения — через Pull Request в main.** Создать ветку, закоммитить, сделать rebase на свежий main, запушить, создать PR.
- **ПЕРЕД КОММИТОМ проверить, не слита ли текущая ветка в main.** Если ветка уже слита (merged) — создать новую ветку от свежего main и делать новый PR. Никогда не пушить в уже слитую ветку.
- **MANDATORY BEFORE EVERY `git push`: rebase onto fresh main:**
  ```bash
  git checkout main && git remote update && git pull && git checkout - && git rebase main
  ```
- **NEVER use `git stash`.**
- **NEVER use merge commits. ALWAYS rebase.**
- **CRITICAL: НИКОГДА не читать содержимое `.env` файлов** — запрещено использовать `cat`, `Read`, `grep`, `head`, `tail` и любые другие способы чтения `.env`. Для загрузки переменных использовать **только** `source <path>/.env`.
- Не хардкодить токены и секреты в коде.
- stdout в MCP сервере занят JSON-RPC — для логов использовать только stderr.
- **ПЕРЕД КАЖДЫМ КОММИТОМ** проверять все файлы на наличие реальных персональных данных. Заменять на вымышленные.
- **В КАЖДОМ PR** обновлять версию в `pyproject.toml` и `src/mcp_server_yandex_market_seller/__init__.py` (patch для фиксов, minor для новых фич).
- **ПЕРЕД публикацией в MCP-реестр** обязательно запускать `mcp-publisher validate` — проверяет `server.json` на соответствие схеме реестра (лимиты длины полей и т.д.).
