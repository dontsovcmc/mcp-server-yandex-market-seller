# Разработка и диагностика

## Как Claude запускает MCP-сервер

Claude Code запускает MCP-сервер как **дочерний процесс** (subprocess) и общается с ним по **stdin/stdout** через JSON-RPC 2.0:

```
Claude Code                          MCP-сервер
    │                                    │
    │── spawn subprocess ──────────────►│  (command + args из конфига)
    │                                    │
    │── stdin: {"method":"initialize"} ─►│  handshake (таймаут 10 сек)
    │◄─ stdout: {"capabilities":...} ───│
    │                                    │
    │── stdin: {"method":"tools/list"} ─►│  получить список инструментов
    │◄─ stdout: [tools...] ─────────────│
    │                                    │
    │        ✓ Connected                 │
```

**Важно:**
- Сервер **не запускается в login shell** — `~/.bashrc`, `~/.zshrc` не выполняются
- **PATH может быть урезан** — команда может не находиться, хотя в обычном терминале работает
- **stdout зарезервирован** для протокола — любой `print()` в stdout ломает соединение (используйте stderr)

## `✗ Failed to connect` — что делать

**1. Запустить сервер вручную:**

```bash
uvx mcp-server-yandex-market-seller
# или
mcp-server-yandex-market-seller
```

**2. Проверить что команда доступна:**

```bash
which mcp-server-yandex-market-seller
```

**3. Использовать абсолютный путь** (если PATH урезан):

```bash
which mcp-server-yandex-market-seller
# Использовать полный путь в конфиге
```

**4. Посмотреть логи Claude Code:**

```bash
# macOS:
tail -f ~/Library/Logs/Claude/mcp*.log
# Linux:
ls ~/.config/Claude/logs/
```

**5. Включить debug-режим:**

```bash
claude --mcp-debug
```

## Частые проблемы

| Симптом | Причина | Решение |
|---------|---------|---------|
| `command not found` | Пакет не установлен | `pip install mcp-server-yandex-market-seller` |
| `Failed to connect` | PATH урезан | Используйте абсолютный путь |
| `401 Unauthorized` | Неверный API-ключ | Проверьте `YM_TOKEN` |
| `403 Forbidden` | Недостаточно прав | Проверьте права API-ключа в ЛК Маркета |
| `No module named` | Другой Python | Используйте entry point вместо `python -m` |

---

## Правила безопасности и качества кода

### Файловые пути (path traversal)

**CRITICAL:** Никогда не открывать файл по пути, переданному от пользователя/LLM без проверки.

- Всегда валидировать через `_safe_path(path)` в `server.py`.
- Хелпер проверяет:
  1. `os.path.realpath()` — резолвит симлинки и `..` (защита от symlink-атак)
  2. Запись разрешена **только в `~/...` или `/tmp/...`** (с `+ os.sep` для защиты от prefix-атак типа `/tmp_evil`)
  3. Запрет записи в **hidden-файлы/директории** под home (`~/.ssh/`, `~/.config/` и т.д.)
- Правило распространяется на: `output_path` в инструментах сохранения PDF, `file_path` в `send_chat_file`, и любой другой путь из внешнего источника.

```python
# Правильно
def _safe_path(path: str) -> str:
    resolved = os.path.realpath(path)
    home = os.path.realpath(os.path.expanduser("~"))
    tmp_dirs = {os.path.realpath(tempfile.gettempdir())}
    if os.path.isdir("/tmp"):
        tmp_dirs.add(os.path.realpath("/tmp"))
    is_under_home = resolved.startswith(home + os.sep)
    is_under_tmp = any(resolved.startswith(d + os.sep) for d in tmp_dirs)
    if not (is_under_home or is_under_tmp):
        raise ValueError(f"Output path must be under home or temp directory: {path}")
    if is_under_home and os.sep + "." in resolved[len(home):]:
        raise ValueError(f"Writing to hidden files/directories is not allowed: {path}")
    return resolved

# Неправильно
with open(path, "wb") as f:  # путь не проверен
    ...
```

### Парсинг JSON от пользователя

**CRITICAL:** Никогда не вызывать `json.loads()` напрямую на строке, пришедшей как параметр инструмента.

- Использовать хелпер `_parse_json(s, label)` в `server.py` — он бросает `ValueError` с понятным сообщением и именем параметра.
- `json.JSONDecodeError` — технический тип, пользователю нужно видеть `"Invalid JSON in offers_json: ..."`.

```python
# Правильно
return _to_json(_get_api().update_order_items(..., _parse_json(items_json, "items_json")))

# Неправильно
return _to_json(_get_api().update_order_items(..., json.loads(items_json)))
```

### Ошибки HTTP-клиента

- **НЕ** включать `resp.text` в текст исключения — ответ API может содержать персональные данные.
- Полное тело ответа логировать только через `log.debug(...)`.
- В `RuntimeError` передавать только метод, путь и статус-код.

```python
# Правильно
log.debug("GET %s error body: %s", path, resp.text)
raise RuntimeError(f"GET {path} -> {resp.status_code}")

# Неправильно
raise RuntimeError(f"GET {path} -> {resp.status_code}: {resp.text}")
```

### Обработка ошибок

- **Никогда не глотать исключения молча.** `except Exception:` без логирования запрещён. Всегда логировать через `log.warning()` или `log.error()` с контекстом (что делали, для какого объекта).
- **Ошибки валидации** — бросать `ValueError` / `RuntimeError` с понятным сообщением. Пример: `raise ValueError(f"Invalid JSON in {label}: {e}")`.
- **HTTP-ошибки** — `ym_api.py` бросает `RuntimeError`. Не перехватывать в tool-функциях — FastMCP сам вернёт ошибку клиенту.

### Стиль кода

- **Читаемые имена хелперов:** `_to_json`, `_parse_json`, `_safe_path`, а не `_j`, `_p`, `_s`.
- **Импорты** — стандартная библиотека → сторонние пакеты → локальные модули, разделённые пустой строкой. Не импортировать неиспользуемые имена.
- **Типы** — аннотировать параметры и возвращаемые значения. `dict`, `list`, `str` — не `Dict`, `List` (Python 3.10+).

### API-клиент (ym_api.py)

- **Сессия** — `YandexMarketAPI` кэшируется в `server._api_instance` (один экземпляр на процесс). Не создавать новый `YandexMarketAPI` на каждый вызов.
- **HTTP-хелперы** — `_get()`, `_post()`, `_put()`, `_delete()`, `_get_bytes()`. Для скачивания файлов использовать `_get_bytes()`, не писать ручные запросы через `session.get()`.

### Логирование

- `logging.basicConfig()` вызывается **только один раз** — в `server.py`.
- В `ym_api.py` и других модулях только `log = logging.getLogger(__name__)` без `basicConfig`.
- Никогда не логировать токены, заголовки авторизации, персональные данные покупателей.

### Хелперы для env-переменных

- `_get_campaign_id()` — обязательный campaign_id, бросает `RuntimeError` если не задан.
- `_get_business_id()` — обязательный business_id, бросает `RuntimeError` если не задан.
- `_get_optional_campaign_id()` — необязательный campaign_id, возвращает `None` если не задан (использовать только там, где API действительно не требует ID).
- **Не обращаться к `os.getenv("YM_CAMPAIGN_ID")` напрямую в теле инструментов** — только через хелперы.

### Тесты

Каждый новый инструмент или изменение в `server.py`/`ym_api.py` **обязательно** покрывается тестами для:

1. **Happy path** — штатный вызов с корректными данными.
2. **Невалидный JSON** — если инструмент принимает `*_json` параметр.
3. **Ошибка API** — мок бросает `RuntimeError`, инструмент возвращает `isError=True`.
4. **Path traversal** — если инструмент принимает `output_path` или `file_path`.

- **Мокаем `YandexMarketAPI`** на уровне класса: `@patch("mcp_server_yandex_market_seller.server.YandexMarketAPI")`. Кэш API сбрасывается автоматически через фикстуру `_reset_api_singleton` в `conftest.py`.
- **Пути в тестах** — использовать `os.path.realpath()` для сравнения путей (на macOS `/tmp` → `/private/tmp`). Temp-файлы создавать в `/tmp` явно.
- **Тестовые данные** — вымышленные ID, имена, адреса. Никаких реальных персональных данных.

### Линтинг

- CI прогоняет `ruff check` перед тестами. Код должен проходить без ошибок.
- Запуск локально: `ruff check src/ tests/`
- `ruff` добавлен в `[project.optional-dependencies] test`.
