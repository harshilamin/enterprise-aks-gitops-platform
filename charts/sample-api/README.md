# Sample API Helm Chart

A reusable Helm chart for the secure FastAPI workload introduced in v1.1.0.

## Capabilities

- Deployment and ClusterIP Service
- Dedicated ServiceAccount with token automount disabled
- ConfigMap-based non-secret configuration
- Startup, liveness, and readiness probes
- Restricted pod and container security contexts
- CPU and memory requests and limits
- HorizontalPodAutoscaler using `autoscaling/v2`
- PodDisruptionBudget using `policy/v1`
- Default-deny-style NetworkPolicy with explicit DNS and same-namespace access
- Optional Ingress using `networking.k8s.io/v1`
- Topology spread constraints
- Graceful termination and rolling-update controls
- Helm test Pod
- JSON Schema validation for values
- Dev, QA, and Production values

## Validate

```powershell
.\scripts\validate-helm.ps1
```

## Render one environment

```powershell
helm template sample-api .\charts\sample-api `
  --namespace sample-api-dev `
  --values .\charts\sample-api\values-dev.yaml
```

## Install into a connected cluster

```powershell
helm upgrade --install sample-api .\charts\sample-api `
  --namespace sample-api-dev `
  --create-namespace `
  --values .\charts\sample-api\values-dev.yaml `
  --atomic `
  --wait
```

Cluster installation is not required for portfolio validation.
