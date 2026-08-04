#!/usr/bin/env bash
set -euo pipefail

echo "=== Validating AKS Workload Identity and Azure Key Vault integration ==="

mkdir -p .rendered/identity

python -m unittest discover \
  -s tests/identity \
  -p "test_*.py" \
  -v

for environment in dev qa prod; do
  chart_values="charts/sample-api/values-${environment}.yaml"
  gitops_values="gitops/environments/${environment}/values.yaml"
  identity_values="charts/sample-api/values-workload-identity-ci.yaml"
  output_file=".rendered/identity/sample-api-${environment}.yaml"

  helm lint charts/sample-api \
    --strict \
    --values "${chart_values}" \
    --values "${gitops_values}" \
    --values "${identity_values}"

  helm template sample-api charts/sample-api \
    --namespace "sample-api-${environment}" \
    --values "${chart_values}" \
    --values "${gitops_values}" \
    --values "${identity_values}" \
    --include-crds > "${output_file}"

  python scripts/validate-rendered-manifests.py \
    "${output_file}" \
    --environment "${environment}"

  python scripts/validate_identity.py \
    "${output_file}" \
    --environment "${environment}" \
    --repository-root .
done

echo "AKS Workload Identity and Azure Key Vault validation passed."
