from fastapi.testclient import TestClient

from sample_api.config import Settings
from sample_api.main import create_app


def test_readiness_is_false_before_lifespan() -> None:
    app = create_app(Settings(environment="test", log_level="CRITICAL"))

    assert app.state.ready is False


def test_lifespan_sets_and_clears_readiness() -> None:
    app = create_app(Settings(environment="test", log_level="CRITICAL"))

    with TestClient(app):
        assert app.state.ready is True

    assert app.state.ready is False


def test_production_disables_interactive_api_docs() -> None:
    app = create_app(Settings(environment="production", log_level="CRITICAL"))

    with TestClient(app) as client:
        assert client.get("/docs").status_code == 404
        assert client.get("/openapi.json").status_code == 404
