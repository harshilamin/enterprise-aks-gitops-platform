# sample-api Helm Chart

A secure application chart for the Enterprise AKS GitOps Platform.

## v1.4.0 capabilities

- Hardened Deployment and ServiceAccount
- Startup, liveness, and readiness probes
- Requests, limits, HPA, PDB, and topology spreading
- Default-deny-style NetworkPolicy controls
- Microsoft Entra Workload ID annotations and pod label
- Azure Key Vault provider `SecretProviderClass`
- Read-only Secrets Store CSI volume
- File-based secret consumption without Kubernetes Secret synchronization

## Workload Identity values

```yaml
workloadIdentity:
  enabled: true
  clientId: "11111111-1111-1111-1111-111111111111"
  tenantId: "22222222-2222-2222-2222-222222222222"
  serviceAccountTokenExpirationSeconds: 3600
```

When enabled, the chart adds these ServiceAccount annotations:

```text
azure.workload.identity/client-id
azure.workload.identity/tenant-id
azure.workload.identity/service-account-token-expiration
```

It also adds this required pod label:

```text
azure.workload.identity/use: "true"
```

## Azure Key Vault values

```yaml
azureKeyVault:
  enabled: true
  name: kv-sample-api-dev
  cloudName: ""
  mountPath: /mnt/secrets-store
  objects:
    - objectName: sample-api-signing-key
      objectVersion: ""
      objectAlias: signing-key
```

The chart renders a namespaced `SecretProviderClass` and mounts the objects at the configured path.

Secret values are not:

- Stored in this repository
- Rendered into Helm manifests
- Synchronized to Kubernetes `Secret` resources
- Printed by validation scripts

## Render identity integration

```powershell
helm template sample-api .\charts\sample-api `
  --namespace sample-api-dev `
  --values .\charts\sample-api\values-dev.yaml `
  --values .\gitops\environments\dev\values.yaml `
  --values .\charts\sample-api\values-workload-identity-ci.yaml
```

## Generate environment configuration

```powershell
.\scripts\generate-workload-identity-values.ps1 `
  -Environment dev `
  -ClientId "11111111-1111-1111-1111-111111111111" `
  -TenantId "22222222-2222-2222-2222-222222222222" `
  -KeyVaultName "kv-sample-api-dev" `
  -SecretNames @("sample-api-signing-key")
```

Add `-MergeGitOps` only after reviewing the Azure identity, federated credential, Key Vault role assignment, and referenced secret names.

## Security boundary

The integration uses:

- One user-assigned managed identity
- One federated identity credential per namespace and ServiceAccount subject
- The built-in `Key Vault Secrets User` role
- Azure RBAC authorization
- Secrets Store CSI file mounts
- No client secret or certificate credential

## Prerequisites for a live cluster

- AKS OIDC issuer enabled
- AKS Workload Identity enabled
- Azure Key Vault Secrets Provider add-on enabled
- Key Vault using Azure RBAC
- User-assigned managed identity
- Federated identity credential
- Referenced secrets already present in Key Vault
