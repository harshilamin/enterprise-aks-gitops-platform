$ErrorActionPreference = "Stop"
Write-Host "=== Validating Repository 2 v2.0.0 ==="
& "$PSScriptRoot\validate-foundation.ps1"
& "$PSScriptRoot\validate-app.ps1"
& "$PSScriptRoot\validate-helm.ps1"
& "$PSScriptRoot\validate-gitops.ps1"
& "$PSScriptRoot\validate-identity.ps1"
& "$PSScriptRoot\validate-observability.ps1"
& "$PSScriptRoot\validate-final-platform.ps1"
python -m mkdocs build --strict
if ($LASTEXITCODE -ne 0) { throw "MkDocs strict build failed." }
Write-Host "`nRepository 2 v2.0.0 validation passed."
