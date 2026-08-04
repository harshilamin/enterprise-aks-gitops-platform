# Apply v1.5.0

This ZIP is an overlay for the merged v1.4.0 repository.

## Branch

```powershell
git checkout main
git pull origin main
git checkout -b feature/release-1.5.0-observability
```

Extract the ZIP and copy the inner directory contents into the repository.

## Dependencies

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pip install -r requirements-docs.txt
python -m pip install -r requirements-helm.txt
python -m pip install -r requirements-gitops.txt
python -m pip install -r requirements-identity.txt
python -m pip install -r requirements-observability.txt
```

## Validation

```powershell
python -m ruff format .
python -m ruff check . --fix
python -m ruff format --check .
python -m ruff check .

powershell.exe -ExecutionPolicy Bypass `
  -File .\scripts\validate-observability.ps1

powershell.exe -ExecutionPolicy Bypass `
  -File .\scripts\validate-v1.5.0.ps1
```

## Commit

```powershell
git add .
git commit -m "feat: add OpenTelemetry Prometheus Grafana and SLOs"
git push -u origin feature/release-1.5.0-observability
```
