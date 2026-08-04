# Changelog

## [1.4.0] - 2026-08-04

### Added

- Microsoft Entra Workload ID Helm values
- Workload Identity ServiceAccount annotations
- Required pod identity label
- Azure Key Vault `SecretProviderClass`
- Read-only Secrets Store CSI volume and mount
- Identity-enabled Dev, QA, and Production rendering
- Azure CLI bootstrap automation for OIDC, Workload Identity, CSI add-on, managed identity, RBAC, and federation
- Non-secret GitOps values generator
- Live verification scripts that do not print secret contents
- Six values-generation unit tests
- Purpose-built identity manifest validation
- Workload Identity CI workflow
- AppProject permission for namespaced `SecretProviderClass`
- Architecture, security, operations, testing, interview, and release documentation
- ADRs for Workload Identity and file-based Key Vault mounts

### Changed

- Helm chart version updated to `1.4.0`
- Helm packaging artifact updated to `sample-api-1.4.0.tgz`
- AppProject namespace resource allowlist expanded for `SecretProviderClass`
- AppProject `Namespace` cluster allowlist corrected to the supported group/kind schema
- Helm and GitOps CI corrected to the published Kubeconform `v0.7.0` image

### Security

- Uses `Key Vault Secrets User` role ID `4633458b-17de-408a-b874-0445c86b69e6`
- Requires Azure RBAC authorization
- Does not synchronize Key Vault values into Kubernetes Secrets
- Does not store or print secret values

## [1.3.0] - 2026-08-04

- Argo CD AppProject and ApplicationSet
- Dev automatic sync
- QA and Production manual synchronization
- Digest promotion
- Drift and rollback documentation

## [1.2.0] - 2026-08-03

- Reusable Helm chart
- Kubernetes security, reliability, and network controls

## [1.1.0] - 2026-08-03

- Secure FastAPI service
- Hardened container, tests, scanning, and SBOM

## [1.0.0] - 2026-08-03

- Repository foundation and architecture
