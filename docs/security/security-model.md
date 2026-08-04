# Security Model

## Build security

- Dependency and image scanning
- SBOM generation
- Image signing
- Immutable image digests

## Deployment security

- OIDC for CI authentication
- Argo CD least-privilege access
- Protected Production promotion
- Environment isolation

## Runtime security

- Non-root containers
- Read-only filesystem where practical
- Dropped Linux capabilities
- Resource limits
- NetworkPolicies
- Pod-security controls
- Workload identity
- Key Vault integration

Secrets must not be committed to Git, values files, images, or ConfigMaps.
