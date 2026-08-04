$ErrorActionPreference = "Stop"
Write-Host "=== Validating Repository 2 final v2.0.0 platform ==="
python -m unittest discover -s .\tests\final-platform -p "test_*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Final configuration unit tests failed." }
New-Item -ItemType Directory -Force -Path .\.rendered\final | Out-Null
foreach ($environment in @("dev", "qa", "prod")) {
  helm lint .\charts\sample-api --strict `
    --values ".\charts\sample-api\values-$environment.yaml" `
    --values ".\gitops\environments\$environment\values.yaml"
  if ($LASTEXITCODE -ne 0) { throw "Helm lint failed for $environment." }
  $output = ".\.rendered\final\sample-api-$environment.yaml"
  $rendered = & helm template sample-api .\charts\sample-api `
    --namespace "sample-api-$environment" `
    --values ".\charts\sample-api\values-$environment.yaml" `
    --values ".\gitops\environments\$environment\values.yaml" `
    --include-crds
  if ($LASTEXITCODE -ne 0) { throw "Helm rendering failed for $environment." }
  $encoding = New-Object System.Text.UTF8Encoding($false)
  [System.IO.File]::WriteAllText([System.IO.Path]::GetFullPath($output), (($rendered -join "`n") + "`n"), $encoding)
  python .\scripts\validate_final_platform.py $output --environment $environment --repository-root .
  if ($LASTEXITCODE -ne 0) { throw "Final contract validation failed for $environment." }
}
Write-Host "`nRepository 2 final v2.0.0 platform validation passed."
