# OpenTelemetry Collector Troubleshooting

## Workload cannot send OTLP

Check:

```powershell
kubectl get service sample-api-otel-collector -n sample-api-dev
kubectl get networkpolicy -n sample-api-dev
kubectl logs deployment/sample-api -n sample-api-dev
kubectl logs deployment/sample-api-otel-collector -n sample-api-dev
```

Confirm the application ConfigMap contains:

```text
OTEL_ENABLED=true
OTEL_EXPORTER_OTLP_ENDPOINT=http://sample-api-otel-collector:4318
```

## Collector is not ready

```powershell
kubectl describe pod -n sample-api-dev -l app.kubernetes.io/component=otel-collector
kubectl logs -n sample-api-dev deployment/sample-api-otel-collector
```

Common causes:

- Invalid Collector configuration
- Memory limiter exceeds the pod memory limit
- Port collision
- Read-only filesystem path not backed by `emptyDir`
- Unsupported component in the selected distribution

## Prometheus has no application metrics

Check the Collector endpoint:

```powershell
kubectl port-forward -n sample-api-dev service/sample-api-otel-collector 8889:8889
```

Then open `http://127.0.0.1:8889/metrics`.

Check Prometheus discovery:

```powershell
kubectl get servicemonitor sample-api -n sample-api-dev -o yaml
kubectl get prometheus -n monitoring -o yaml
```

## High cardinality

Inspect label counts before adding new attributes. Do not promote raw URLs, query parameters, request IDs, or customer identifiers into metric labels.
