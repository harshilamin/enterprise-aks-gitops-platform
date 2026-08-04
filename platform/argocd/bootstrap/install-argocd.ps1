param(
    [string]$Version = "v3.4.2"
)

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

Invoke-Native "Check kubectl" {
    kubectl version --client
}

Invoke-Native "Create Argo CD namespace" {
    kubectl create namespace argocd --dry-run=client -o yaml |
        kubectl apply -f -
}

$manifestUrl = "https://raw.githubusercontent.com/argoproj/argo-cd/$Version/manifests/install.yaml"

Invoke-Native "Install Argo CD $Version" {
    kubectl apply `
        --namespace argocd `
        --server-side `
        --force-conflicts `
        --filename $manifestUrl
}

Invoke-Native "Wait for Argo CD server" {
    kubectl rollout status deployment/argocd-server `
        --namespace argocd `
        --timeout 5m
}

Invoke-Native "Wait for repository server" {
    kubectl rollout status deployment/argocd-repo-server `
        --namespace argocd `
        --timeout 5m
}

Invoke-Native "Wait for ApplicationSet controller" {
    kubectl rollout status deployment/argocd-applicationset-controller `
        --namespace argocd `
        --timeout 5m
}

Invoke-Native "Wait for application controller" {
    kubectl rollout status statefulset/argocd-application-controller `
        --namespace argocd `
        --timeout 5m
}

Write-Host "`nArgo CD $Version installation completed."
