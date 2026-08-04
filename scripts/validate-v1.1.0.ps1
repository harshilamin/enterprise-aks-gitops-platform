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

Write-Host "=== Validating Repository 2 v1.1.0 ==="

& "$PSScriptRoot\validate-foundation.ps1"
& "$PSScriptRoot\validate-app.ps1"

Invoke-CheckedCommand "Build MkDocs documentation" {
    python -m mkdocs build --strict
}

Write-Host "`nRepository 2 v1.1.0 validation passed."