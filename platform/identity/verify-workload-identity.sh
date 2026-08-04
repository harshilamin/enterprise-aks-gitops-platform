#!/usr/bin/env bash
set -euo pipefail

environment="${1:?Usage: verify-workload-identity.sh <dev|qa|prod> [release-name]}"
release_name="${2:-sample-api}"
namespace="sample-api-${environment}"
mount_path="${MOUNT_PATH:-/mnt/secrets-store}"

kubectl rollout status \
  "deployment/${release_name}" \
  --namespace "${namespace}" \
  --timeout 5m

kubectl get serviceaccount "${release_name}" \
  --namespace "${namespace}" \
  --output yaml

kubectl get secretproviderclass "${release_name}-azure-key-vault" \
  --namespace "${namespace}" \
  --output yaml

pod_name="$(kubectl get pods \
  --namespace "${namespace}" \
  --selector "app.kubernetes.io/instance=${release_name}" \
  --field-selector status.phase=Running \
  --output jsonpath='{.items[0].metadata.name}')"

kubectl exec "${pod_name}" \
  --namespace "${namespace}" \
  -- ls -1 "${mount_path}"

echo "Workload Identity verification completed without printing secret contents."
