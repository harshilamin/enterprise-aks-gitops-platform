# v1.4.0 — AKS Workload Identity and Azure Key Vault Integration

## Highlights

- Passwordless Microsoft Entra Workload ID
- Exact Kubernetes ServiceAccount federation
- Azure Key Vault Secrets Provider add-on bootstrap
- Least-privilege `Key Vault Secrets User`
- Helm-managed `SecretProviderClass`
- Read-only CSI secret mounts
- No Kubernetes Secret synchronization
- GitOps-safe identifier generation
- Dev, QA, and Production validation
- Live verification without printing secret values

## Security model

The pod receives a projected Kubernetes ServiceAccount token. Microsoft Entra validates the token through the AKS OIDC issuer and exchanges it for a managed-identity token. The identity can read only the permitted Key Vault secrets.

## Validation

- Six generator unit tests
- Three environment renders
- Base workload security checks
- Workload Identity annotation and label checks
- CSI volume and mount checks
- SecretProviderClass checks
- Kubernetes Secret rejection
- Kubernetes schema validation

## Next release

v1.5.0 adds OpenTelemetry, OTLP Collector, Prometheus, Grafana, traces, metrics, logs, and SLOs.
