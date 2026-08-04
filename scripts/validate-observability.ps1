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

Write-Host "=== Validating OpenTelemetry, Prometheus, Grafana, and SLOs ==="

New-Item -ItemType Directory -Force .\.rendered\observability | Out-Null

Invoke-Native "Run observability contract tests" {
    python -m unittest discover `
        -s .\tests\observability `
        -p "test_*.py" `
        -v
}

foreach ($environment in @("dev", "qa", "prod")) {
    $chartValues = ".\charts\sample-api\values-$environment.yaml"
    $gitopsValues = ".\gitops\environments\$environment\values.yaml"
    $outputFile = ".\.rendered\observability\sample-api-$environment.yaml"

    Invoke-Native "Lint observable desired state for $environment" {
        helm lint .\charts\sample-api `
            --strict `
            --values $chartValues `
            --values $gitopsValues
    }

    Write-Host "`n--- Render observable desired state for $environment ---"
    $rendered = & helm template sample-api .\charts\sample-api `
        --namespace "sample-api-$environment" `
        --values $chartValues `
        --values $gitopsValues `
        --include-crds

    if ($LASTEXITCODE -ne 0) {
        throw "Observability rendering for $environment failed with exit code $LASTEXITCODE."
    }

    $outputPath = [System.IO.Path]::GetFullPath($outputFile)
    $outputContent = ($rendered -join "`n") + "`n"
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($outputPath, $outputContent, $utf8NoBom)

    Invoke-Native "Validate base workload controls for $environment" {
        python .\scripts\validate-rendered-manifests.py `
            $outputFile `
            --environment $environment
    }

    Invoke-Native "Validate observability contracts for $environment" {
        python .\scripts\validate_observability.py `
            $outputFile `
            --environment $environment `
            --repository-root .
    }
}

Write-Host "`nOpenTelemetry, Prometheus, Grafana, and SLO validation passed."
