# Enterprise AKS GitOps Platform

Repository 1 provisions Azure and AKS. Repository 2 demonstrates secure application packaging, Kubernetes controls, GitOps delivery, passwordless Azure identity, secret mounting, and operations.

## Current release

v1.4.0 adds:

- Microsoft Entra Workload ID
- User-assigned managed identity federation
- Azure Key Vault Secrets Provider
- Namespaced `SecretProviderClass`
- Read-only CSI secret files
- Azure RBAC bootstrap automation
- Non-secret GitOps values generation
- Identity validation for Dev, QA, and Production

## Security outcome

The workload uses no client secret. Key Vault values are not stored in Git, rendered into Helm output, or synchronized into Kubernetes Secrets.

## Next release

v1.5.0 introduces OpenTelemetry, OTLP, Prometheus, and Grafana.
