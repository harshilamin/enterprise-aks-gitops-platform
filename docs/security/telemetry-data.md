# Telemetry Data Security

## Data minimization

The instrumentation does not attach:

- Query strings
- Request or response bodies
- Authorization headers
- Cookies
- Key Vault values
- User identifiers
- Raw request IDs as metric labels

Request IDs remain in logs for operational correlation but are not metric attributes.

## Cardinality protection

Metrics use bounded dimensions:

- HTTP method
- Route template
- HTTP status code
- Deployment environment resource attribute

Raw paths are retained only in structured logs, where they are not converted into Prometheus labels.

## Trace correlation

JSON logs include `trace_id` and `span_id` only when an active valid span exists. Responses include `X-Trace-ID` to support incident correlation.

## Network boundary

The application NetworkPolicy permits OTLP egress only to the in-namespace Collector. The Collector accepts OTLP only from the application and metrics scrapes only from the `monitoring` namespace.

The Collector has no egress in this release because traces use the local debug exporter and metrics are pulled by Prometheus.

## Credentials

No Prometheus, Grafana, Azure, or OTLP credential is committed. Grafana uses an existing Kubernetes Secret created interactively without writing the password to disk.
