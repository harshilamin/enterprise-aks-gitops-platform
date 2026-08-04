# sample-api Helm Chart

A secure, observable application chart for the Enterprise AKS GitOps Platform.

## v1.5.0 capabilities

- Hardened FastAPI Deployment
- Microsoft Entra Workload Identity and Azure Key Vault CSI
- OpenTelemetry Collector deployment
- OTLP/HTTP and OTLP/gRPC receivers
- Prometheus application metric exporter
- Collector internal telemetry endpoint
- ServiceMonitor
- SLI recording rules
- Multi-window availability burn alerts
- p95 latency alert
- Grafana dashboard ConfigMap
- NetworkPolicy for telemetry flows

## Render

```powershell
helm template sample-api .\charts\sample-api `
  --namespace sample-api-dev `
  --values .\charts\sample-api\values-dev.yaml `
  --values .\gitops\environments\dev\values.yaml
```

## Signal behavior

- Traces: OTLP -> Collector -> debug exporter
- Metrics: OTLP -> Collector -> Prometheus exporter
- Logs: structured stdout with `trace_id` and `span_id`

## SLO defaults

```yaml
observability:
  prometheusRule:
    availabilityTarget: 0.995
    latencyThresholdSeconds: 0.5
```

## Production note

Replace the debug trace exporter with a durable backend before relying on distributed tracing for retention or search.
