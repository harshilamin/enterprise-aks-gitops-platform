# Observable Sample API

A secure FastAPI workload instrumented with OpenTelemetry traces and metrics.

## Telemetry

The application emits OTLP/HTTP protobuf to an OpenTelemetry Collector:

- Server spans for inbound requests
- Request count counter
- Request duration histogram in seconds
- Active request up/down counter
- Structured JSON logs containing `trace_id` and `span_id`
- `X-Trace-ID` response correlation header

## Configuration

```text
OTEL_ENABLED=true
OTEL_SERVICE_NAME=enterprise-aks-sample-api
OTEL_EXPORTER_OTLP_ENDPOINT=http://sample-api-otel-collector:4318
OTEL_METRIC_EXPORT_INTERVAL_MS=15000
OTEL_TRACE_SAMPLE_RATIO=1.0
```

Signal-specific OTLP/HTTP paths are added automatically:

```text
/v1/traces
/v1/metrics
```

## Cardinality controls

Metrics use route templates rather than raw URLs. Query strings, request IDs,
and user-controlled values are not metric attributes.

## Endpoints

| Endpoint | Purpose |
|---|---|
| `/` | Service metadata |
| `/health/live` | Container liveness |
| `/health/ready` | Traffic readiness |
| `/health/startup` | Startup completion |
| `/api/v1/info` | Runtime information |
| `/docs` | Local, Dev, and QA API documentation |

Production disables `/docs` and `/openapi.json`.
