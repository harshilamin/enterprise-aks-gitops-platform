"""OpenTelemetry tracing and metrics for the sample API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from opentelemetry import context as otel_context
from opentelemetry import propagate, trace
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.metrics import Counter, Histogram, Meter, UpDownCounter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import MetricReader, PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.sampling import ParentBased, TraceIdRatioBased
from opentelemetry.trace import SpanKind, Status, StatusCode, Tracer

from sample_api.config import Settings

INSTRUMENTATION_SCOPE = "sample_api"


@dataclass(slots=True)
class Telemetry:
    """Application-scoped telemetry providers and instruments."""

    tracer: Tracer
    meter: Meter
    request_counter: Counter
    request_duration: Histogram
    active_requests: UpDownCounter
    tracer_provider: TracerProvider
    meter_provider: MeterProvider
    enabled: bool

    def shutdown(self) -> None:
        """Flush and stop exporters during graceful application shutdown."""
        if not self.enabled:
            return
        self.tracer_provider.force_flush(timeout_millis=5000)
        self.meter_provider.force_flush(timeout_millis=5000)
        self.tracer_provider.shutdown()
        self.meter_provider.shutdown()


def _signal_endpoint(base_endpoint: str, signal: str) -> str:
    return f"{base_endpoint.rstrip('/')}/v1/{signal}"


def create_telemetry(settings: Settings) -> Telemetry:
    """Create isolated providers so tests do not mutate global OpenTelemetry state."""
    resource = Resource.create(
        {
            "service.name": settings.otel_service_name,
            "service.version": settings.app_version,
            "deployment.environment.name": settings.environment,
            "telemetry.sdk.language": "python",
        }
    )

    tracer_provider = TracerProvider(
        resource=resource,
        sampler=ParentBased(TraceIdRatioBased(settings.otel_trace_sample_ratio)),
    )
    metric_readers: list[MetricReader] = []

    if settings.otel_enabled:
        span_exporter = OTLPSpanExporter(
            endpoint=_signal_endpoint(settings.otel_exporter_otlp_endpoint, "traces")
        )
        tracer_provider.add_span_processor(BatchSpanProcessor(span_exporter))

        metric_exporter = OTLPMetricExporter(
            endpoint=_signal_endpoint(settings.otel_exporter_otlp_endpoint, "metrics")
        )
        metric_readers.append(
            PeriodicExportingMetricReader(
                metric_exporter,
                export_interval_millis=settings.otel_metric_export_interval_ms,
            )
        )

    meter_provider = MeterProvider(resource=resource, metric_readers=metric_readers)
    tracer = tracer_provider.get_tracer(INSTRUMENTATION_SCOPE, settings.app_version)
    meter = meter_provider.get_meter(INSTRUMENTATION_SCOPE, settings.app_version)

    return Telemetry(
        tracer=tracer,
        meter=meter,
        request_counter=meter.create_counter(
            "http.server.request.count",
            unit="{request}",
            description="Completed inbound HTTP requests",
        ),
        request_duration=meter.create_histogram(
            "http.server.request.duration",
            unit="s",
            description="Inbound HTTP request duration",
        ),
        active_requests=meter.create_up_down_counter(
            "http.server.active_requests",
            unit="{request}",
            description="Currently active inbound HTTP requests",
        ),
        tracer_provider=tracer_provider,
        meter_provider=meter_provider,
        enabled=settings.otel_enabled,
    )


def extract_context(headers: Any) -> otel_context.Context:
    """Extract W3C trace context from request headers."""
    return propagate.extract(headers)


def request_attributes(method: str, route: str, status_code: int | None = None) -> dict[str, Any]:
    """Return bounded-cardinality HTTP metric and span attributes."""
    attributes: dict[str, Any] = {
        "http.request.method": method,
        "http.route": route,
    }
    if status_code is not None:
        attributes["http.response.status_code"] = status_code
    return attributes


def span_context_ids() -> tuple[str | None, str | None]:
    """Return current trace and span identifiers for logs and response correlation."""
    span_context = trace.get_current_span().get_span_context()
    if not span_context.is_valid:
        return None, None
    return f"{span_context.trace_id:032x}", f"{span_context.span_id:016x}"


def mark_span_result(span: trace.Span, status_code: int) -> None:
    """Set stable HTTP result attributes and span status."""
    span.set_attribute("http.response.status_code", status_code)
    if status_code >= 500:
        span.set_status(Status(StatusCode.ERROR, f"HTTP {status_code}"))


__all__ = [
    "SpanKind",
    "Telemetry",
    "create_telemetry",
    "extract_context",
    "mark_span_result",
    "request_attributes",
    "span_context_ids",
]
