# v1.4.0 Validation Notes

## Passed in the generation environment

- Python syntax compilation
- JSON syntax, including the Helm values schema
- YAML syntax for files that do not contain Helm templates
- Six Workload Identity values-generation unit tests
- Bash syntax validation
- AppProject permission and configuration checks
- MkDocs navigation target existence
- Overlay file and packaging checks

## Unit-test result

```text
Ran 6 tests
OK
```

The tests cover:

- Absence of secret values
- Client ID validation
- Key Vault name validation
- Secret object-name validation
- ServiceAccount token-expiration limits
- GitOps merge behavior and image-reference preservation

## Local and GitHub validation still required

The generation environment did not contain Helm, PowerShell, Kubeconform, or
an Azure-connected Kubernetes cluster. Run the supplied scripts to complete:

- Ruff formatting and linting
- Helm strict linting
- Dev, QA, and Production identity rendering
- Existing workload security and reliability assertions
- Workload Identity and Key Vault CSI assertions
- Kubeconform validation
- Helm packaging
- MkDocs strict rendering
- PowerShell execution
- Optional Azure CLI bootstrap
- Optional live AKS federation and Key Vault mount verification

## Security boundary

No Azure credential, Key Vault secret value, or Kubernetes Secret data is
embedded in this release package.
