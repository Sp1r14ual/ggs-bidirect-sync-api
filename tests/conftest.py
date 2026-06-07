import pytest
import httpx
from fast_bitrix24 import Bitrix

from app.settings import settings
from tests.settings import test_settings as _test_settings


@pytest.fixture(scope="session")
def test_settings():
    return _test_settings


@pytest.fixture(scope="session")
def api_client():
    with httpx.Client(base_url=_test_settings.TEST_API_BASE_URL, timeout=60.0) as client:
        yield client


@pytest.fixture(scope="session")
def bitrix():
    return Bitrix(settings.BITRIX_WEBHOOK, ssl=False)


@pytest.fixture(scope="module")
def house_sync_result(api_client, test_settings):
    """First sync of the test house. Shared across all tests in the module."""
    response = api_client.post(f"/forward_sync/house/{test_settings.TEST_HOUSE_ID}")
    assert response.status_code == 200, f"Initial sync failed: {response.text}"
    return response.json()
