$ErrorActionPreference = "Stop"

Write-Host "=== Validating secure sample API ==="

python --version
python -m ruff format --check .
python -m ruff check .
python -m mypy apps/sample-api/src
python -m pytest

Write-Host "Sample API validation passed."
