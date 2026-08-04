# sample-api Helm Chart — v2.0.0

The final chart packages a hardened FastAPI workload with environment-specific delivery and scaling patterns.

## Environment composition

| Environment | Workload | Autoscaler |
|---|---|---|
| Dev | Kubernetes Deployment | HPA |
| QA | Argo Rollout canary | HPA targeting the Rollout scale subresource |
| Prod | Kubernetes Deployment | KEDA Prometheus ScaledObject |

## Platform features

- Startup, liveness, and readiness probes
- Requests, limits, HPA, KEDA, PDB, topology spreading, and pod anti-affinity
- Default-deny-style NetworkPolicy with DNS, monitoring, collector, and optional ingress-controller allowances
- Microsoft Entra Workload ID and Azure Key Vault Secrets Store CSI
- OpenTelemetry Collector, ServiceMonitor, PrometheusRule, and Grafana dashboard
- Argo Rollouts AnalysisTemplate with availability and p95 latency checks
- Immutable image digest support

## Validate

```powershell
helm lint . --strict --values values-qa.yaml
helm template sample-api . --namespace sample-api-qa --values values-qa.yaml
```

The chart intentionally prevents KEDA and progressive delivery from being enabled together in the same environment. This avoids two controllers competing for the same scaling target in the reference architecture.
