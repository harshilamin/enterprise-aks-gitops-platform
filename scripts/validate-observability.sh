#!/usr/bin/env bash
set -euo pipefail

echo "=== Validating OpenTelemetry, Prometheus, Grafana, and SLOs ==="
mkdir -p .rendered/observability

python -m unittest discover \
  -s tests/observability \
  -p "test_*.py" \
  -v

for environment in dev qa prod; do
  chart_values="charts/sample-api/values-${environment}.yaml"
  gitops_values="gitops/environments/${environment}/values.yaml"
  output_file=".rendered/observability/sample-api-${environment}.yaml"

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

  python scripts/validate_observability.py \
    "${output_file}" \
    --environment "${environment}" \
    --repository-root .
done

echo "OpenTelemetry, Prometheus, Grafana, and SLO validation passed."
