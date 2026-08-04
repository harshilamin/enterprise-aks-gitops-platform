import logging
import sys

from fastapi.testclient import TestClient

from sample_api.config import Settings
from sample_api.logging_config import JsonFormatter
from sample_api.main import create_app


def test_not_ready_endpoints_return_503() -> None:
    app = create_app(Settings(environment="test", log_level="CRITICAL"))

    with TestClient(app) as client:
        app.state.ready = False

        ready_response = client.get("/health/ready")
        startup_response = client.get("/health/startup")

        assert ready_response.status_code == 503
        assert ready_response.json()["status"] == "starting"
        assert startup_response.status_code == 503
        assert startup_response.json()["status"] == "starting"


def test_unhandled_error_returns_500_when_server_exceptions_are_disabled() -> None:
    app = create_app(Settings(environment="test", log_level="CRITICAL"))

    @app.get("/failure")
    async def failure() -> None:
        raise RuntimeError("expected test failure")

    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/failure")

    assert response.status_code == 500


def test_json_formatter_includes_structured_fields() -> None:
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="sample_api",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="request complete",
        args=(),
        exc_info=None,
    )
    record.event = "request_completed"
    record.request_id = "abc-123"
    record.method = "GET"
    record.path = "/health/live"
    record.status_code = 200
    record.duration_ms = 1.25

    output = formatter.format(record)

    assert '"event":"request_completed"' in output
    assert '"request_id":"abc-123"' in output
    assert '"status_code":200' in output


def test_json_formatter_includes_exception() -> None:
    formatter = JsonFormatter()

    try:
        raise RuntimeError("formatter test")
    except RuntimeError:
        exc_info = sys.exc_info()

    record = logging.LogRecord(
        name="sample_api",
        level=logging.ERROR,
        pathname=__file__,
        lineno=1,
        msg="failure",
        args=(),
        exc_info=exc_info,
    )

    output = formatter.format(record)

    assert '"exception":' in output
    assert "RuntimeError: formatter test" in output
