#!/usr/bin/env bash
set -euo pipefail

echo "=== Validating Argo CD GitOps configuration ==="

mkdir -p .rendered/gitops

python scripts/validate_gitops.py

python -m unittest discover \
  -s tests/gitops \
  -p "test_*.py" \
  -v

python scripts/render_gitops_applications.py \
  --output .rendered/gitops/applications.yaml

for environment in dev qa prod; do
  chart_values="charts/sample-api/values-${environment}.yaml"
  gitops_values="gitops/environments/${environment}/values.yaml"
  output_file=".rendered/gitops/sample-api-${environment}.yaml"

  helm lint charts/sample-api \
    --strict \
    --values "${chart_values}" \
    --values "${gitops_values}"

  helm template sample-api charts/sample-api \
    --namespace "sample-api-${environment}" \
    --values "${chart_values}" \
    --values "${gitops_values}" \
    --include-crds > "${output_file}"

  python scripts/validate-rendered-manifests.py \
    "${output_file}" \
    --environment "${environment}"
done

echo "Argo CD GitOps validation passed."
