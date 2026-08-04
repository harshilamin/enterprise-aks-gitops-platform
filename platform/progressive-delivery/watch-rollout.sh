#!/usr/bin/env bash
set -euo pipefail
environment="${1:-qa}"
kubectl argo rollouts get rollout sample-api -n "sample-api-${environment}" --watch
