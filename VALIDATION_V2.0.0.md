# v2.0.0 Validation Notes

## Passed in the generation environment

- Python syntax compilation
- JSON syntax validation
- YAML syntax validation for files that do not contain Helm templates
- GitHub Actions workflow YAML parsing
- Bash syntax validation
- Helm values JSON Schema validation
- Dev, QA, and Production value composition
- Six final-platform configuration tests
- Thirty-two FastAPI application tests
- Application test coverage of 96.01 percent
- MkDocs navigation target existence checks
- Final package and ZIP integrity checks

## Test results

```text
Final-platform tests: 6 passed
Application tests:    32 passed
Application coverage: 96.01%
```

## Required local and GitHub validation

The generation environment did not provide Helm, Kubeconform, Docker, Ruff,
mypy, MkDocs, PowerShell, a Kubernetes cluster, or Azure/GitHub OIDC
credentials. Run the supplied validation scripts and CI workflows to complete:

- Ruff formatting and linting
- mypy type checking
- Helm strict linting and Dev, QA, and Production rendering
- Kubernetes and custom-resource contract assertions
- Kubeconform validation where schemas are available
- MkDocs strict build
- PowerShell execution
- KEDA live scaling and fallback behavior
- Argo Rollouts canary progression, analysis, promotion, and abort
- Kyverno admission-policy behavior
- Cosign keyless signing and attestation in GitHub Actions
- Trivy image scanning in GitHub Actions
- Azure-connected Workload Identity, Key Vault, and failure testing

## Security boundary

No Azure credential, Kubernetes credential, signing key, registry token, or
secret value is embedded in this package. Destructive resilience testing is
opt-in and requires an explicit execution switch.
