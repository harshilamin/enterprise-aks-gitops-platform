from uuid import UUID

from fastapi.testclient import TestClient


def test_root_returns_service_metadata(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "service": "enterprise-aks-sample-api",
        "version": "1.5.0",
        "environment": "test",
        "status": "running",
    }


def test_health_endpoints_are_available(client: TestClient) -> None:
    expected_statuses = {
        "/health/live": "alive",
        "/health/ready": "ready",
        "/health/startup": "ready",
    }

    for endpoint, expected_status in expected_statuses.items():
        response = client.get(endpoint)

        assert response.status_code == 200
        assert response.json()["status"] == expected_status


def test_info_reports_runtime_version(client: TestClient) -> None:
    response = client.get("/api/v1/info")

    assert response.status_code == 200
    assert response.json()["environment"] == "test"
    assert response.json()["python_version"]


def test_request_id_is_preserved(client: TestClient) -> None:
    response = client.get("/", headers={"X-Request-ID": "interview-demo-123"})

    assert response.headers["X-Request-ID"] == "interview-demo-123"


def test_request_id_is_generated(client: TestClient) -> None:
    response = client.get("/")

    UUID(response.headers["X-Request-ID"])


def test_security_headers_are_returned(client: TestClient) -> None:
    response = client.get("/")

    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Referrer-Policy"] == "no-referrer"
    assert response.headers["Cache-Control"] == "no-store"


def test_unknown_route_returns_not_found(client: TestClient) -> None:
    response = client.get("/does-not-exist")

    assert response.status_code == 404


def test_trace_id_is_returned(client: TestClient) -> None:
    response = client.get("/")

    trace_id = response.headers["X-Trace-ID"]
    assert len(trace_id) == 32
    int(trace_id, 16)
