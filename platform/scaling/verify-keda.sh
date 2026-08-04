#!/usr/bin/env bash
set -euo pipefail
environment="${1:-prod}"
namespace="sample-api-${environment}"
kubectl get scaledobject sample-api -n "${namespace}" -o wide
kubectl get hpa -n "${namespace}"
kubectl describe scaledobject sample-api -n "${namespace}"
