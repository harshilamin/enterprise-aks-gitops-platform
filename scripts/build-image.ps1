$ErrorActionPreference = "Stop"

$Image = if ($env:IMAGE_NAME) {
    $env:IMAGE_NAME
}
else {
    "enterprise-aks-sample-api:1.1.0"
}

docker build `
    --file .\apps\sample-api\Dockerfile `
    --tag $Image `
    .

docker run --rm `
    --read-only `
    --tmpfs /tmp:size=16m `
    --cap-drop ALL `
    --security-opt no-new-privileges `
    $Image `
    python -c "from sample_api.main import app; print(app.title)"

Write-Host "Container image validation passed: $Image"
