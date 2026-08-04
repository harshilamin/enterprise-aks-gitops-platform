# Workload Identity Testing

## Static tests

The release validates:

- Client ID and tenant ID UUID format
- Key Vault and secret object naming
- ServiceAccount token expiration range
- GitOps merge behavior
- Existing image desired state preservation
- Absence of secret values

## Rendered manifest tests

For Dev, QA, and Production, CI asserts:

- Required ServiceAccount annotations
- Required `azure.workload.identity/use` pod label
- `automountServiceAccountToken: false` remains in place
- Read-only CSI volume
- Read-only container mount
- Azure provider `SecretProviderClass`
- `usePodIdentity: "false"`
- Expected client ID, tenant ID, and Key Vault name
- Secret object type only
- No Kubernetes `Secret`
- No `secretObjects` synchronization

## Schema validation

Kubeconform validates built-in Kubernetes resources. The `SecretProviderClass` CRD is validated by the repository's purpose-built Python assertions.

## Live testing

A live AKS test requires Azure resources and cannot be completed by static CI alone.

Use the bootstrap and verification scripts after enabling the environment through a reviewed GitOps change.
