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
