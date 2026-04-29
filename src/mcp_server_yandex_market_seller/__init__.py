"""MCP server for Yandex Market Partner API."""

import sys

__version__ = "0.4.2"


def main():
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        from .cli import main as cli_main
        cli_main()
    elif "--version" in sys.argv:
        print(f"mcp-server-yandex-market-seller {__version__}")
    else:
        from .server import mcp
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
