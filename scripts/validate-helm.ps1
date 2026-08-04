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

Write-Host "=== Validating Helm chart ==="

Invoke-CheckedCommand "Check Helm version" {
    helm version
}

$renderDirectory = Join-Path $PSScriptRoot "..\.rendered"
New-Item -ItemType Directory -Force $renderDirectory | Out-Null

foreach ($environment in @("dev", "qa", "prod")) {
    $valuesFile = ".\charts\sample-api\values-$environment.yaml"
    $outputFile = Join-Path $renderDirectory "sample-api-$environment.yaml"

    Invoke-CheckedCommand "Lint $environment values" {
        helm lint .\charts\sample-api --strict --values $valuesFile
    }

    Invoke-CheckedCommand "Render $environment manifests" {
        helm template sample-api .\charts\sample-api `
            --namespace "sample-api-$environment" `
            --values $valuesFile `
            --output-dir $renderDirectory
    }

    Invoke-CheckedCommand "Create combined $environment manifest" {
        helm template sample-api .\charts\sample-api `
            --namespace "sample-api-$environment" `
            --values $valuesFile `
            --include-crds | Set-Content -Path $outputFile -Encoding utf8
    }

    Invoke-CheckedCommand "Validate $environment security invariants" {
        python .\scripts\validate-rendered-manifests.py `
            $outputFile `
            --environment $environment
    }
}

Invoke-CheckedCommand "Package chart" {
    helm package .\charts\sample-api --destination $renderDirectory
}

Write-Host "`nHelm chart validation passed."
