$ErrorActionPreference = "Stop"

$env:APP_ENVIRONMENT = if ($env:APP_ENVIRONMENT) {
    $env:APP_ENVIRONMENT
}
else {
    "local"
}

python -m uvicorn sample_api.main:app `
    --host 0.0.0.0 `
    --port 8080 `
    --no-access-log
