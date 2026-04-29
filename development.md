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

- Всегда проверять `".." in pathlib.Path(path).parts` перед `open()`.
- Использовать хелпер `_safe_path(path)` в `server.py` — он бросает `ValueError` при попытке traversal.
- Правило распространяется на: `output_path` в инструментах сохранения PDF, `file_path` в `send_chat_file`, и любой другой путь из внешнего источника.

```python
# Правильно
def _safe_path(path: str) -> pathlib.Path:
    p = pathlib.Path(path)
    if ".." in p.parts:
        raise ValueError(f"Path traversal not allowed: '{path}'")
    return p

# Неправильно
with open(path, "wb") as f:  # путь не проверен
    ...
```

### Парсинг JSON от пользователя

**CRITICAL:** Никогда не вызывать `json.loads()` напрямую на строке, пришедшей как параметр инструмента.

- Использовать хелпер `_parse_json(s)` в `server.py` — он бросает `ValueError` с понятным сообщением.
- `json.JSONDecodeError` — технический тип, пользователю нужно видеть `"Invalid JSON input: ..."`.

```python
# Правильно
return _j(_get_api().update_order_items(..., _parse_json(items_json)))

# Неправильно
return _j(_get_api().update_order_items(..., json.loads(items_json)))
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

### Линтинг

- CI прогоняет `ruff check` перед тестами. Код должен проходить без ошибок.
- Запуск локально: `ruff check src/ tests/`
- `ruff` добавлен в `[project.optional-dependencies] test`.
