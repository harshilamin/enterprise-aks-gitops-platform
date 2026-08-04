# Final v2.0.0 Platform Architecture

```mermaid
flowchart LR
  Dev[Developer] --> PR[Pull request controls]
  PR --> CI[Tests, scans, SBOM]
  CI --> Sign[Cosign keyless signing]
  Sign --> Registry[GHCR immutable digest]
  Registry --> Promote[Digest promotion]
  Promote --> ArgoCD[Argo CD]
  ArgoCD --> DevEnv[Dev Deployment + HPA]
  ArgoCD --> QA[QA Argo Rollout + analysis]
  ArgoCD --> Prod[Prod Deployment + KEDA]
  QA --> Prom[Prometheus SLO queries]
  Prod --> Prom
  Prod --> KV[Key Vault through Workload Identity]
  Policy[Kyverno audit policies] --> DevEnv
  Policy --> QA
  Policy --> Prod
```

## Environment design

| Environment | Delivery | Scaling | Approval |
|---|---|---|---|
| Development | Deployment | HPA | Automatic Argo CD sync |
| QA | Argo Rollout canary | HPA | Manual sync and metric analysis |
| Production | Deployment | KEDA Prometheus scaler | Manual sync and immutable digest |

The environments deliberately demonstrate separate patterns rather than enabling every controller against the same scale target.
