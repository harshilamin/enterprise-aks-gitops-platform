# Secret Rotation Operations

The Azure Key Vault provider supports rotation of mounted content when the AKS add-on is configured for autorotation.

## Application behavior

The chart mounts the full CSI directory and does not use a Kubernetes `subPath`.

Applications that cache secret values in memory still need a reload mechanism. Common patterns are:

- Watch the mounted file for changes
- Re-read the file for each use when appropriate
- Trigger a controlled rollout after rotation

## Verify without exposing values

List object names only:

```powershell
.\platform\identity\verify-workload-identity.ps1 `
  -Environment dev
```

The verification script does not run `cat`, `Get-Content`, or another command that prints secret values.

## Rotation test

1. Record the pod start time.
2. Update the Key Vault secret.
3. Wait for the configured provider poll interval.
4. Confirm the mounted file timestamp changes.
5. Confirm application behavior without printing the value.
6. Review Key Vault diagnostics and pod events.

## Incident handling

For `FailedMount` events, check:

- `SecretProviderClass` exists in the same namespace
- Object name exists in Key Vault
- ServiceAccount annotation client ID
- Pod Workload Identity label
- Federated credential issuer and subject
- `Key Vault Secrets User` role assignment
- Key Vault network accessibility
- CSI driver and Azure provider pods in `kube-system`
