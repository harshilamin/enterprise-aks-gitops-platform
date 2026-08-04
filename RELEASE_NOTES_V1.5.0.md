# v1.5.0 — OpenTelemetry, Prometheus, Grafana, and SLOs

## Highlights

- Vendor-neutral OpenTelemetry instrumentation
- OTLP/HTTP traces and metrics
- Collector contrib `0.157.0`
- Prometheus and Grafana integration
- 99.5% availability objective
- Multi-window error-budget burn alerts
- p95 latency objective
- Trace-correlated JSON logs
- Dedicated observability CI

## Operational boundary

Metrics are production-oriented. Traces use the Collector debug exporter and are not retained in a durable trace backend in this release.

## Next release

v1.6.0 adds scaling, resilience testing, capacity controls, and advanced networking.
