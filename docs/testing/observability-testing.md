# Observability Testing

## Application tests

The test suite verifies:

- OpenTelemetry settings parsing
- Boolean, interval, and sampling validation
- Trace response correlation
- Trace and span IDs in structured logs
- Low-cardinality request attributes
- Error span status
- No-op shutdown when export is disabled

## Helm rendering

Dev, QA, and Production renders validate:

- Application OTLP environment
- Dynamic pod identity fields
- Pinned Collector image
- Collector hardening
- OTLP receivers
- Prometheus exporter
- Collector internal telemetry
- ServiceMonitor endpoints
- SLI recording rules
- Multi-window SLO alerts
- Grafana dashboard JSON
- Environment-specific sampling and replicas

## CI boundary

Static CI does not prove:

- Live OTLP delivery
- Prometheus target health
- Grafana sidecar import
- Alertmanager routing
- Azure networking

Use the live verification scripts after GitOps synchronization.
