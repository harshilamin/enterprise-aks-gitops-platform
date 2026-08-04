#!/usr/bin/env bash
set -euo pipefail
environment="${1:-qa}"
execute="${2:-}"
if [[ "${execute}" != "--execute" ]]; then
  echo "This test deletes one application pod. Re-run with --execute after confirming the target cluster." >&2
  exit 1
fi
namespace="sample-api-${environment}"
pod="$(kubectl get pods -n "${namespace}" -l app.kubernetes.io/instance=sample-api -o jsonpath='{.items[0].metadata.name}')"
kubectl delete pod "${pod}" -n "${namespace}" --wait=false
kubectl wait --for=condition=Ready pod -l app.kubernetes.io/instance=sample-api -n "${namespace}" --timeout=5m
kubectl get pods -n "${namespace}" -o wide
