# Azure Key Vault Secret Security

## No credentials in Git

This release never stores:

- Managed identity client secrets
- Service principal passwords
- Key Vault secret values
- Kubernetes Secret data

Client IDs, tenant IDs, vault names, and secret object names are identifiers, not secret values.

## Least privilege

The workload identity receives the built-in Azure role:

```text
Key Vault Secrets User
4633458b-17de-408a-b874-0445c86b69e6
```

That role is read-only for Key Vault secret contents and metadata.

The bootstrap script refuses to continue when the Key Vault uses the legacy access-policy authorization model.

## File mount instead of Kubernetes Secret synchronization

The chart mounts secrets directly through the Secrets Store CSI Driver.

It intentionally omits `secretObjects`, so secret values are not duplicated into Kubernetes `Secret` resources or stored in etcd through this chart.

## Read-only runtime

The CSI volume and container mount both use:

```yaml
readOnly: true
```

The existing container hardening remains enabled:

- Non-root UID and GID
- Read-only root filesystem
- All Linux capabilities dropped
- Privilege escalation disabled
- `RuntimeDefault` seccomp

## Namespace and Argo CD controls

The `SecretProviderClass` is namespaced with the workload.

The Argo CD AppProject allows only the `SecretProviderClass` custom resource in addition to the existing workload resource kinds.

## Private networking

For an isolated AKS design, Repository 1 should provide:

- Key Vault private endpoint
- Private DNS resolution
- Required outbound access for AKS and the CSI provider
- Firewall rules for Azure control-plane dependencies
