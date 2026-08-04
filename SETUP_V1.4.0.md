# Apply v1.4.0

This ZIP is an overlay for the merged v1.3.0 repository.

## Create the branch

```powershell
git checkout main
git pull origin main
git checkout -b feature/release-1.4.0-workload-identity
```

Extract the ZIP into a temporary folder and copy its inner contents into the repository.

## Install dependencies

```powershell
.\.venv\Scripts\Activate.ps1

python -m pip install -e ".[dev]"
python -m pip install -r requirements-docs.txt
python -m pip install -r requirements-helm.txt
python -m pip install -r requirements-gitops.txt
python -m pip install -r requirements-identity.txt
```

## Validate

```powershell
python -m ruff format --check .
python -m ruff check .

powershell.exe -ExecutionPolicy Bypass `
  -File .\scripts\validate-identity.ps1

powershell.exe -ExecutionPolicy Bypass `
  -File .\scripts\validate-v1.4.0.ps1
```

## Commit

```powershell
git add .
git commit -m "feat: add AKS Workload Identity and Azure Key Vault integration"
git push -u origin feature/release-1.4.0-workload-identity
```

## Release

After merge:

```powershell
git checkout main
git pull origin main
git tag -a v1.4.0 -m "Release v1.4.0: AKS Workload Identity and Azure Key Vault integration"
git push origin v1.4.0
```
