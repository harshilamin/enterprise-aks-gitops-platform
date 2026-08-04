#!/usr/bin/env bash
set -euo pipefail

echo "=== Validating Helm chart ==="

helm version
mkdir -p .rendered

for environment in dev qa prod; do
  values_file="charts/sample-api/values-${environment}.yaml"
  output_file=".rendered/sample-api-${environment}.yaml"

  helm lint charts/sample-api --strict --values "${values_file}"
  helm template sample-api charts/sample-api \
    --namespace "sample-api-${environment}" \
    --values "${values_file}" \
    --output-dir .rendered
  helm template sample-api charts/sample-api \
    --namespace "sample-api-${environment}" \
    --values "${values_file}" \
    --include-crds > "${output_file}"
  python scripts/validate-rendered-manifests.py \
    "${output_file}" \
    --environment "${environment}"
done

helm package charts/sample-api --destination .rendered

echo "Helm chart validation passed."
