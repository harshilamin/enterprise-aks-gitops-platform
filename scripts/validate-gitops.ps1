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

Write-Host "=== Validating Argo CD GitOps configuration ==="

New-Item `
    -ItemType Directory `
    -Force `
    -Path .\.rendered\gitops |
    Out-Null

Invoke-Native "Validate Argo CD and environment configuration" {
    python .\scripts\validate_gitops.py
}

Invoke-Native "Run image-promotion unit tests" {
    python -m unittest discover `
        -s .\tests\gitops `
        -p "test_*.py" `
        -v
}

Invoke-Native "Render expected Argo CD Applications" {
    python .\scripts\render_gitops_applications.py `
        --output .\.rendered\gitops\applications.yaml
}

foreach ($environment in @("dev", "qa", "prod")) {
    $chartValues = ".\charts\sample-api\values-$environment.yaml"
    $gitopsValues = ".\gitops\environments\$environment\values.yaml"
    $outputFile = ".\.rendered\gitops\sample-api-$environment.yaml"

    Invoke-Native "Lint Helm desired state for $environment" {
        helm lint .\charts\sample-api `
            --strict `
            --values $chartValues `
            --values $gitopsValues
    }

    Write-Host "`n--- Render Helm desired state for $environment ---"
    $rendered = & helm template sample-api .\charts\sample-api `
        --namespace "sample-api-$environment" `
        --values $chartValues `
        --values $gitopsValues `
        --include-crds

    if ($LASTEXITCODE -ne 0) {
        throw "Helm rendering for $environment failed with exit code $LASTEXITCODE."
    }

    $outputPath = [System.IO.Path]::GetFullPath($outputFile)
    $outputContent = ($rendered -join "`n") + "`n"
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)

    [System.IO.File]::WriteAllText(
        $outputPath,
        $outputContent,
        $utf8NoBom
    )

    Invoke-Native "Validate rendered workload for $environment" {
        python .\scripts\validate-rendered-manifests.py `
            $outputFile `
            --environment $environment
    }
}

Write-Host "`nArgo CD GitOps validation passed."
