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

Invoke-Native "Apply sample API AppProject" {
    kubectl apply --filename .\gitops\projects\sample-api-project.yaml
}

Invoke-Native "Apply sample API ApplicationSet" {
    kubectl apply --filename .\gitops\applicationsets\sample-api.yaml
}

Start-Sleep -Seconds 5

Invoke-Native "List generated Argo CD resources" {
    kubectl get appprojects,applicationsets,applications `
        --namespace argocd
}

Write-Host "`nGitOps bootstrap completed."
