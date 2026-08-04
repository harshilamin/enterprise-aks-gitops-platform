# Changelog

## [1.5.0] - 2026-08-04

### Added

- OpenTelemetry Python traces and metrics
- OTLP/HTTP exporters
- Trace-correlated JSON logs and `X-Trace-ID`
- OpenTelemetry Collector contrib `0.157.0`
- Memory limiter, resource, and batch processors
- Prometheus application metric exporter
- Collector internal telemetry
- ServiceMonitor for application and Collector metrics
- Grafana dashboard ConfigMap
- SLI recording rules
- 99.5% availability objective
- Fast and slow multi-window burn alerts
- p95 latency objective and alert
- Collector export-failure alert
- kube-prometheus-stack GitOps Application pinned to `86.0.0`
- Interactive Grafana administrator Secret creation
- Observability contract tests and CI
- Architecture, security, testing, runbook, ADR, and interview documentation

### Changed

- Application version updated to `1.5.0`
- Helm chart version and appVersion updated to `1.5.0`
- GitOps image references updated to `1.5.0`
- Base and identity validators updated for multi-component charts
- AppProject expanded for ServiceMonitor and PrometheusRule

### Security

- Telemetry excludes request bodies, credentials, cookies, and query strings
- Collector runs non-root with a read-only root filesystem
- NetworkPolicy restricts OTLP and Prometheus traffic
- Grafana password is not stored in Git

## [1.4.0] - 2026-08-04

- Microsoft Entra Workload Identity and Azure Key Vault CSI integration

## [1.3.0] - 2026-08-04

- Argo CD AppProject, ApplicationSet, and immutable promotion

## [1.2.0] - 2026-08-03

- Helm and Kubernetes controls

## [1.1.0] - 2026-08-03

- Secure FastAPI service and hardened container

## [1.0.0] - 2026-08-03

- Repository foundation and architecture
