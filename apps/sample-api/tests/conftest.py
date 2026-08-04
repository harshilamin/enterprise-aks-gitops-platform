from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from sample_api.config import Settings
from sample_api.main import create_app


@pytest.fixture
def client() -> Iterator[TestClient]:
    settings = Settings(environment="test", log_level="CRITICAL")
    with TestClient(create_app(settings)) as test_client:
        yield test_client
