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

Write-Host "=== Validating AKS Workload Identity and Azure Key Vault integration ==="

New-Item `
    -ItemType Directory `
    -Force `
    -Path .\.rendered\identity |
    Out-Null

Invoke-Native "Run Workload Identity values unit tests" {
    python -m unittest discover `
        -s .\tests\identity `
        -p "test_*.py" `
        -v
}

foreach ($environment in @("dev", "qa", "prod")) {
    $chartValues = ".\charts\sample-api\values-$environment.yaml"
    $gitopsValues = ".\gitops\environments\$environment\values.yaml"
    $identityValues = ".\charts\sample-api\values-workload-identity-ci.yaml"
    $outputFile = ".\.rendered\identity\sample-api-$environment.yaml"

    Invoke-Native "Lint identity-enabled desired state for $environment" {
        helm lint .\charts\sample-api `
            --strict `
            --values $chartValues `
            --values $gitopsValues `
            --values $identityValues
    }

    Write-Host "`n--- Render identity-enabled desired state for $environment ---"
    $rendered = & helm template sample-api .\charts\sample-api `
        --namespace "sample-api-$environment" `
        --values $chartValues `
        --values $gitopsValues `
        --values $identityValues `
        --include-crds

    if ($LASTEXITCODE -ne 0) {
        throw "Identity rendering for $environment failed with exit code $LASTEXITCODE."
    }

    $outputPath = [System.IO.Path]::GetFullPath($outputFile)
    $outputContent = ($rendered -join "`n") + "`n"
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)

    [System.IO.File]::WriteAllText(
        $outputPath,
        $outputContent,
        $utf8NoBom
    )

    Invoke-Native "Validate base workload invariants for $environment" {
        python .\scripts\validate-rendered-manifests.py `
            $outputFile `
            --environment $environment
    }

    Invoke-Native "Validate Workload Identity and Key Vault invariants for $environment" {
        python .\scripts\validate_identity.py `
            $outputFile `
            --environment $environment `
            --repository-root .
    }
}

Write-Host "`nAKS Workload Identity and Azure Key Vault validation passed."
