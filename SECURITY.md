# Security Policy

Do not report credentials or exploitable vulnerabilities in a public issue.

## Principles

- OIDC instead of long-lived CI credentials
- Workload identity for pod-to-Azure access
- Key Vault references instead of committed secrets
- Immutable image digests
- Non-root containers
- Read-only filesystems where practical
- Resource limits and NetworkPolicies
- Least-privilege RBAC
- Scanned and signed images
- Protected Production promotion
