$ErrorActionPreference = "Stop"

function Invoke-CheckedCommand {
    param(
        [Parameter(Mandatory)]
        [string]$Description,

        [Parameter(Mandatory)]
        [scriptblock]$Command
    )

    Write-Host "`n--- $Description ---"
    & $Command

    if ($LASTEXITCODE -ne 0) {
        throw "$Description failed with exit code $LASTEXITCODE."
    }
}

Write-Host "=== Validating secure sample API ==="

Invoke-CheckedCommand "Check Python version" {
    python --version
}

Invoke-CheckedCommand "Check Ruff formatting" {
    python -m ruff format --check .
}

Invoke-CheckedCommand "Run Ruff linting" {
    python -m ruff check .
}

Invoke-CheckedCommand "Run mypy type checking" {
    python -m mypy apps/sample-api/src
}

Invoke-CheckedCommand "Run application tests" {
    python -m pytest
}

Write-Host "`nSample API validation passed."