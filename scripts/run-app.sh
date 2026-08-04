#!/usr/bin/env bash
set -euo pipefail

export APP_ENVIRONMENT="${APP_ENVIRONMENT:-local}"

python -m uvicorn sample_api.main:app \
  --host 0.0.0.0 \
  --port 8080 \
  --no-access-log
