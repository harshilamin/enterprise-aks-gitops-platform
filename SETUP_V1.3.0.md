# Apply v1.3.0

This ZIP is an overlay for the merged v1.2.0 repository.

## Create the branch

```powershell
git checkout main
git pull origin main
git checkout -b feature/release-1.3.0-gitops
```

Extract the ZIP into a temporary folder and copy its inner contents into the repository.

## Install dependencies

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-gitops.txt
```

## Validate

```powershell
powershell.exe -ExecutionPolicy Bypass `
  -File .\scripts\validate-gitops.ps1

powershell.exe -ExecutionPolicy Bypass `
  -File .\scripts\validate-v1.3.0.ps1
```

## Commit

```powershell
git add .
git commit -m "feat: add Argo CD GitOps and environment promotion"
git push -u origin feature/release-1.3.0-gitops
```

## Release

After the pull request is merged:

```powershell
git checkout main
git pull origin main
git tag -a v1.3.0 -m "Release v1.3.0: Argo CD GitOps and environment promotion"
git push origin v1.3.0
```
