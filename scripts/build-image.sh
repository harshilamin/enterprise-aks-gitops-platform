#!/usr/bin/env bash
set -euo pipefail

image="${IMAGE_NAME:-enterprise-aks-sample-api:1.1.0}"

docker build \
  --file apps/sample-api/Dockerfile \
  --tag "${image}" \
  .

docker run --rm \
  --read-only \
  --tmpfs /tmp:size=16m \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  "${image}" \
  python -c "from sample_api.main import app; print(app.title)"

echo "Container image validation passed: ${image}"
