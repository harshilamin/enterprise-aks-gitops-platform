# Enterprise AKS GitOps Platform — Final v2.0.0

A production-inspired Azure Kubernetes Service application platform demonstrating secure workload engineering, Helm packaging, Argo CD GitOps, Microsoft Entra Workload ID, Azure Key Vault CSI, OpenTelemetry, Prometheus, Grafana, SLOs, KEDA scaling, Argo Rollouts, software supply-chain security, and policy as code.

## Final environment model

| Environment | Workload | Scaling | Delivery |
|---|---|---|---|
| Dev | Deployment | HPA | Automatic Argo CD sync |
| QA | Argo Rollout | HPA | Canary steps with Prometheus analysis |
| Prod | Deployment | KEDA | Manual digest promotion |

## Complete release progression

- v1.0.0 — Repository and architecture foundation
- v1.1.0 — Secure FastAPI workload and hardened container
- v1.2.0 — Helm and Kubernetes controls
- v1.3.0 — Argo CD GitOps and environment promotion
- v1.4.0 — AKS Workload Identity and Azure Key Vault
- v1.5.0 — OpenTelemetry, Prometheus, Grafana, and SLOs
- v2.0.0 — KEDA, progressive delivery, resilience, supply-chain security, policy, and final integration

## Final validation

Install the application and all validation layers:

```powershell
python -m pip install -e ".[dev]"
python -m pip install -r requirements-docs.txt
python -m pip install -r requirements-helm.txt
python -m pip install -r requirements-gitops.txt
python -m pip install -r requirements-identity.txt
python -m pip install -r requirements-observability.txt
python -m pip install -r requirements-final.txt
```

Run the complete release validation:

```powershell
python -m ruff format --check .
python -m ruff check .
python -m mypy apps\sample-api\src
python -m pytest
powershell.exe -ExecutionPolicy Bypass `
  -File .\scripts\validate-v2.0.0.ps1
```

## Optional controllers

```powershell
.\platform\scaling\install-keda.ps1
.\platform\progressive-delivery\install-argo-rollouts.ps1
.\platform\policies\install-kyverno.ps1
```

## Security outcomes

- No static Azure credential in Git
- Key Vault values mounted as read-only files
- No chart-managed Kubernetes Secret synchronization
- Immutable production image digest policy
- Critical vulnerability gate
- Keyless image signing with GitHub OIDC
- CycloneDX SBOM attestation
- Audit-first Kyverno policy rollout

## Author

**Harshil Amin**  
Senior DevOps Engineer
