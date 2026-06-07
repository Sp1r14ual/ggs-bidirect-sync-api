import subprocess
import time
import pytest
import httpx
from fast_bitrix24 import Bitrix

from app.settings import settings
from tests.settings import test_settings as _test_settings


@pytest.fixture(scope="session")
def test_settings():
    return _test_settings


@pytest.fixture(scope="session", autouse=True)
def ensure_server(test_settings):
    """
    Starts uvicorn if the server is not already running.
    If you start the server manually in another terminal, this fixture detects it
    and skips the automatic startup -- useful when debugging the app during test runs.
    """
    health_url = f"{test_settings.TEST_API_BASE_URL}/docs"

    try:
        httpx.get(health_url, timeout=2.0)
        yield
        return
    except (httpx.ConnectError, httpx.TimeoutException):
        pass

    proc = subprocess.Popen(
        ["uvicorn", "app.app:app", "--port", "8000"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    for _ in range(30):
        try:
            httpx.get(health_url, timeout=1.0)
            break
        except (httpx.ConnectError, httpx.TimeoutException):
            time.sleep(1)
    else:
        proc.kill()
        pytest.exit("FastAPI server did not start within 30 seconds")

    yield

    proc.kill()
    proc.wait(timeout=5)


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
