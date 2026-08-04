$ErrorActionPreference = "Stop"

Write-Host "=== Validating Repository 2 v1.1.0 ==="

& "$PSScriptRoot\validate-foundation.ps1"
& "$PSScriptRoot\validate-app.ps1"
python -m mkdocs build --strict

Write-Host "Repository 2 v1.1.0 validation passed."
