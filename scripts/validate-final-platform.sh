#!/usr/bin/env bash
set -euo pipefail
python -m unittest discover -s tests/final-platform -p 'test_*.py' -v
mkdir -p .rendered/final
for environment in dev qa prod; do
  helm lint charts/sample-api --strict \
    --values "charts/sample-api/values-${environment}.yaml" \
    --values "gitops/environments/${environment}/values.yaml"
  output=".rendered/final/sample-api-${environment}.yaml"
  helm template sample-api charts/sample-api \
    --namespace "sample-api-${environment}" \
    --values "charts/sample-api/values-${environment}.yaml" \
    --values "gitops/environments/${environment}/values.yaml" \
    --include-crds > "${output}"
  python scripts/validate_final_platform.py "${output}" --environment "${environment}" --repository-root .
done
echo "Repository 2 final v2.0.0 platform validation passed."
