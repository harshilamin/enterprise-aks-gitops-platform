# Repository Setup

## 1. Create the GitHub repository

Create a public repository named:

```text
enterprise-aks-gitops-platform
```

Do not initialize it with a README, license, or `.gitignore`.

## 2. Extract locally

Extract this package so that the repository files are inside:

```text
C:\DevOps\enterprise-aks-gitops-platform
```

## 3. Initialize Git

```powershell
cd C:\DevOps\enterprise-aks-gitops-platform

git init
git branch -M main
```

## 4. Validate

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-docs.txt

powershell.exe -ExecutionPolicy Bypass -File .\scripts\validate-foundation.ps1
python -m mkdocs build --strict
```

## 5. Push the foundation

```powershell
git add .
git commit -m "feat: establish AKS GitOps platform foundation"
git remote add origin https://github.com/harshilamin/enterprise-aks-gitops-platform.git
git push -u origin main
```

## 6. Tag v1.0.0

```powershell
git tag -a v1.0.0 -m "Release v1.0.0: repository foundation"
git push origin v1.0.0
```

## Repository description

```text
Production-inspired AKS application platform using Helm, Argo CD, GitOps, workload identity, OpenTelemetry, Prometheus, Grafana, progressive delivery, and secure CI/CD.
```

## Recommended topics

```text
aks
kubernetes
gitops
argocd
helm
azure
devops
platform-engineering
opentelemetry
prometheus
grafana
github-actions
```
