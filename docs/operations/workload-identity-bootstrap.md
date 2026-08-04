# Workload Identity Bootstrap

## Prerequisites

- Merged v1.4.0 repository
- Azure CLI authenticated
- Existing AKS cluster
- Existing Azure Key Vault using Azure RBAC
- Referenced secrets already created
- Permission to update AKS, create a managed identity and federated credential, and assign Azure roles

## PowerShell

```powershell
powershell.exe -ExecutionPolicy Bypass `
  -File .\platform\identity\bootstrap-workload-identity.ps1 `
  -SubscriptionId "<subscription-id>" `
  -ResourceGroup "<resource-group>" `
  -ClusterName "<aks-cluster>" `
  -IdentityName "id-sample-api-dev" `
  -KeyVaultName "kv-sample-api-dev" `
  -Environment dev `
  -SecretNames @(
      "sample-api-signing-key",
      "sample-api-database-password"
  )
```

The script:

1. Enables the AKS OIDC issuer.
2. Enables AKS Workload Identity.
3. Enables the Azure Key Vault Secrets Provider add-on.
4. Creates or reuses a user-assigned managed identity.
5. Confirms that Key Vault uses Azure RBAC.
6. Assigns `Key Vault Secrets User`.
7. Creates the federated identity credential.
8. Generates non-secret Helm values under `.rendered/workload-identity`.

## Review before GitOps merge

Inspect:

```powershell
Get-Content .\.rendered\workload-identity\dev.yaml
```

The file should contain only identifiers and secret object names.

After review, merge into the Development desired state:

```powershell
.\scripts\generate-workload-identity-values.ps1 `
  -Environment dev `
  -ClientId "<managed-identity-client-id>" `
  -TenantId "<tenant-id>" `
  -KeyVaultName "kv-sample-api-dev" `
  -SecretNames @(
      "sample-api-signing-key",
      "sample-api-database-password"
  ) `
  -MergeGitOps
```

Open a pull request rather than editing the live Application directly.

## Federated subject

For Development, the expected subject is:

```text
system:serviceaccount:sample-api-dev:sample-api
```

QA and Production use their corresponding namespaces.

## Propagation

New federated credentials and Azure role assignments can require time to propagate. A pod started immediately after creation can temporarily receive authorization errors.
