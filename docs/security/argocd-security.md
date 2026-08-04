# Argo CD Security

## AppProject restrictions

The `sample-api` AppProject permits:

- One trusted Git repository
- One in-cluster destination
- Three exact namespaces
- Only the namespaced resource kinds used by the Helm chart

Only `Namespace` is allowed at cluster scope, and its name must match `sample-api-*`.

## Repository access

The portfolio repository is public, so no repository credential is required.

For a private enterprise repository, use a dedicated read-only credential, GitHub App, or workload identity pattern rather than a personal token embedded in YAML.

## Synchronization permissions

- Development uses automatic synchronization.
- QA and Production require explicit synchronization.
- Production promotion should be protected by branch review and Argo CD RBAC.

## Secret handling

Argo CD manifests and Helm values must not contain application secrets. Azure workload identity and Key Vault integration are introduced in v1.4.0.

## Administrative access

The initial local administrator password is for bootstrap only. Enterprise deployments should integrate SSO, disable unnecessary local accounts, and apply least-privilege project roles.
