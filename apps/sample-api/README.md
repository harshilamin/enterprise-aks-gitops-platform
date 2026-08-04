# Secure Sample API

A small FastAPI workload designed to demonstrate production-oriented container and Kubernetes practices.

## Features

- Application factory for isolated testing
- Liveness, readiness, and startup endpoints
- Structured JSON logging
- Request correlation with `X-Request-ID`
- Security response headers
- Environment validation
- Production API-documentation disablement
- Graceful startup and shutdown lifecycle
- Strict type checking
- Test coverage threshold
- Non-root multi-stage container image

## Endpoints

| Endpoint | Purpose |
|---|---|
| `/` | Service metadata |
| `/health/live` | Container liveness |
| `/health/ready` | Traffic readiness |
| `/health/startup` | Startup completion |
| `/api/v1/info` | Runtime information |
| `/docs` | Local, Dev, and QA API documentation |

Production disables `/docs` and `/openapi.json`.

## Run locally

```powershell
python -m pip install -e ".[dev]"
sample-api
```

Open `http://127.0.0.1:8080`.
