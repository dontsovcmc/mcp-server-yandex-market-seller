import os

import pytest

os.environ.setdefault("YM_TOKEN", "test-fake-token")
os.environ.setdefault("YM_CAMPAIGN_ID", "12345")
os.environ.setdefault("YM_BUSINESS_ID", "67890")


@pytest.fixture(autouse=True)
def _reset_api_singleton():
    """Reset cached API instance between tests."""
    import mcp_server_yandex_market_seller.server as srv
    srv._api_instance = None
    yield
    srv._api_instance = None
