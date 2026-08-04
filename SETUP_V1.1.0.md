# Apply v1.1.0

This package is an overlay for the existing v1.0.0 repository.

## Branch

```powershell
git checkout main
git pull origin main
git checkout -b feature/release-1.1.0-secure-api
```

Extract the ZIP to a temporary location and copy the inner files into the repository.

## Python 3.14.6

```powershell
Remove-Item -Recurse -Force .venv -ErrorAction SilentlyContinue

py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1

python --version
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Expected Python output:

```text
Python 3.14.6
```

## Validate

```powershell
powershell.exe -ExecutionPolicy Bypass `
  -File .\scripts\validate-app.ps1

python -m mkdocs build --strict
```

## Container

```powershell
docker compose build
docker compose up -d
docker compose ps
Invoke-RestMethod http://127.0.0.1:8080/health/ready
docker compose down
```

## Commit

```powershell
git add .
git commit -m "feat: add secure containerized FastAPI service"
git push -u origin feature/release-1.1.0-secure-api
```

## Release

After the pull request is merged:

```powershell
git checkout main
git pull origin main
git tag -a v1.1.0 -m "Release v1.1.0: secure containerized FastAPI service"
git push origin v1.1.0
```
