$ErrorActionPreference = "Stop"

function Invoke-Native {
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

Write-Host "=== Validating Repository 2 v1.5.0 ==="

& "$PSScriptRoot\validate-foundation.ps1"
& "$PSScriptRoot\validate-app.ps1"
& "$PSScriptRoot\validate-helm.ps1"
& "$PSScriptRoot\validate-gitops.ps1"
& "$PSScriptRoot\validate-identity.ps1"
& "$PSScriptRoot\validate-observability.ps1"

Invoke-Native "Build MkDocs documentation" {
    python -m mkdocs build --strict
}

Write-Host "`nRepository 2 v1.5.0 validation passed."
