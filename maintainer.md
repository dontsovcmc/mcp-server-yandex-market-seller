# Публикация пакета

## PyPI

### Сборка и публикация

```bash
pip install build twine
python -m build
twine upload dist/*
```

### Проверка

```bash
pip install mcp-server-yandex-market-seller==X.Y.Z
```

## MCP-реестр

### CRITICAL: mcp-name в README

**Обязательно** в `README.md` должна быть строка:

```
mcp-name: io.github.dontsovcmc/yandex-market-seller
```

Значение должно совпадать с полем `name` в `server.json`. Без этой строки `mcp-publisher publish` вернёт ошибку:
`PyPI package ownership validation failed. The server name must appear as 'mcp-name: ...' in the package README`.

Строка нужна для подтверждения владения PyPI-пакетом — реестр проверяет README на PyPI.

### Публикация

```bash
mcp-publisher validate   # обязательно перед публикацией
mcp-publisher login github
mcp-publisher publish
```

### Обновление версии

При каждом релизе обновить в трёх местах:
1. `pyproject.toml` — `version`
2. `src/mcp_server_yandex_market_seller/__init__.py` — `__version__`
3. `server.json` — `version` и `packages[0].version`

Затем: собрать → залить на PyPI → `mcp-publisher publish`.
