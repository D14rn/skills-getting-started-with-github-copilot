import pytest
from copy import deepcopy

import src.app as app_module


@pytest.fixture
def app():
    """Return the FastAPI app instance from src.app."""
    return app_module.app


@pytest.fixture(autouse=True)
def reset_activities():
    """Snapshot and restore the module-level `activities` to isolate tests."""
    original = deepcopy(app_module.activities)
    yield
    app_module.activities = deepcopy(original)


@pytest.fixture
async def async_client(app):
    """Provide an httpx AsyncClient bound to the FastAPI app."""
    from httpx import AsyncClient, ASGITransport

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
