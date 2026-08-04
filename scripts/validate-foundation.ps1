$ErrorActionPreference = "Stop"

Write-Host "=== Validating Repository 2 foundation ==="

$requiredFiles = @(
    "README.md",
    "CHANGELOG.md",
    "ROADMAP.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "mkdocs.yml",
    "requirements-docs.txt",
    ".github\workflows\repository-ci.yml",
    ".github\workflows\docs-ci.yml",
    "docs\architecture\overview.md",
    "docs\security\security-model.md"
)

foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        throw "Missing required file: $file"
    }
    Write-Host "Found $file"
}

$requiredDirectories = @(
    "apps\sample-api",
    "charts\sample-api",
    "gitops\applications",
    "gitops\projects",
    "gitops\environments\dev",
    "gitops\environments\qa",
    "gitops\environments\prod",
    "platform\argocd",
    "platform\observability",
    "platform\policies",
    "platform\secrets"
)

foreach ($directory in $requiredDirectories) {
    if (-not (Test-Path $directory -PathType Container)) {
        throw "Missing required directory: $directory"
    }
    Write-Host "Found $directory"
}

$trackedFiles = git ls-files 2>$null
if ($LASTEXITCODE -eq 0) {
    $forbidden = $trackedFiles | Where-Object {
    (
        $_ -match '(^|/)\.env($|\.)' -and
        $_ -notmatch '(^|/)\.env\.example$'
    ) -or
    $_ -match '\.(pem|pfx|key)$' -or
    $_ -match '(^|/)kubeconfig$'
}

    if ($forbidden) {
        throw "Sensitive files are tracked: $($forbidden -join ', ')"
    }
}

Write-Host "Repository 2 foundation validation passed."
