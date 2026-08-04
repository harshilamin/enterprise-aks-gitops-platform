#!/usr/bin/env bash
set -euo pipefail

echo "=== Validating secure sample API ==="

python --version
python -m ruff format --check .
python -m ruff check .
python -m mypy apps/sample-api/src
python -m pytest

echo "Sample API validation passed."
