# Local Development

## Python 3.14.6

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Validate

```powershell
.\scripts\validate-app.ps1
```

## Run

```powershell
.\scripts\run-app.ps1
```

## Container

```powershell
docker compose up --build
```

## Test endpoints

```powershell
Invoke-RestMethod http://127.0.0.1:8080/health/live
Invoke-RestMethod http://127.0.0.1:8080/health/ready
Invoke-RestMethod http://127.0.0.1:8080/api/v1/info
```
