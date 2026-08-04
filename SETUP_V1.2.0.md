# Apply v1.2.0

This ZIP is an overlay for the merged and tagged v1.1.0 repository.

## Create the branch

```powershell
git checkout main
git pull origin main
git checkout -b feature/release-1.2.0-helm
```

Extract the ZIP to a temporary folder and copy the inner files into the repository.

## Install Helm

```powershell
winget install --id Helm.Helm --exact
```

Close and reopen PowerShell, then verify:

```powershell
helm version
```

## Install the validator

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-helm.txt
```

## Validate

```powershell
powershell.exe -ExecutionPolicy Bypass `
  -File .\scripts\validate-v1.2.0.ps1
```

## Commit

```powershell
git add .
git commit -m "feat: add reusable Helm chart and Kubernetes controls"
git push -u origin feature/release-1.2.0-helm
```

## Release

After merge:

```powershell
git checkout main
git pull origin main
git tag -a v1.2.0 -m "Release v1.2.0: Helm packaging and Kubernetes controls"
git push origin v1.2.0
```
