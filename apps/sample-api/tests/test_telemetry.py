from opentelemetry import trace

from sample_api.config import Settings
from sample_api.telemetry import (
    create_telemetry,
    mark_span_result,
    request_attributes,
    span_context_ids,
)


def test_disabled_telemetry_creates_local_instruments() -> None:
    telemetry = create_telemetry(Settings(environment="test", otel_enabled=False))

    assert telemetry.enabled is False
    assert telemetry.request_counter is not None
    assert telemetry.request_duration is not None
    assert telemetry.active_requests is not None
    telemetry.shutdown()


def test_signal_span_context_ids_are_hex() -> None:
    telemetry = create_telemetry(Settings(environment="test", otel_enabled=False))

    with telemetry.tracer.start_as_current_span("unit-test"):
        trace_id, span_id = span_context_ids()

    assert trace_id is not None and len(trace_id) == 32
    assert span_id is not None and len(span_id) == 16
    int(trace_id, 16)
    int(span_id, 16)


def test_no_active_span_has_no_ids() -> None:
    assert span_context_ids() == (None, None)


def test_request_attributes_are_low_cardinality() -> None:
    attributes = request_attributes("GET", "/api/v1/items/{item_id}", 200)

    assert attributes == {
        "http.request.method": "GET",
        "http.route": "/api/v1/items/{item_id}",
        "http.response.status_code": 200,
    }


def test_server_error_marks_span_as_error() -> None:
    telemetry = create_telemetry(Settings(environment="test", otel_enabled=False))

    with telemetry.tracer.start_as_current_span("failure") as span:
        mark_span_result(span, 503)
        assert span.status.status_code is trace.StatusCode.ERROR
