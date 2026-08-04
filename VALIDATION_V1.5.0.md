# v1.5.0 Validation Notes

## Passed in the generation environment

- Python syntax compilation for application and validation modules
- 32 FastAPI tests
- 96.01% application coverage against a 90% minimum
- Six observability contract unit tests
- JSON parsing, including the Helm values schema and Grafana dashboard
- YAML parsing for files that do not contain Helm templates
- Dev, QA, and Production values composition against `values.schema.json`
- MkDocs navigation target existence checks
- Relative Markdown link target checks
- Bash syntax validation
- Overlay-to-merged-tree consistency checks

## Results

```text
Application tests: 32 passed
Application coverage: 96.01%
Observability contract tests: 6 passed
Values schema errors: dev 0, qa 0, prod 0
```

## Required local and GitHub validation

The generation environment did not contain Helm, Kubeconform, PowerShell,
Ruff, mypy, or MkDocs. Run the supplied validation scripts to complete:

- Ruff formatting and linting
- Strict mypy checking
- Helm strict linting
- Dev, QA, and Production Helm rendering
- Existing workload security and reliability assertions
- Workload Identity and Key Vault CSI assertions
- OpenTelemetry, Prometheus, Grafana, and SLO manifest assertions
- Kubeconform validation
- Helm packaging
- MkDocs strict rendering
- PowerShell execution

## Live validation boundary

A connected cluster is still required to verify:

- Prometheus target health
- Grafana dashboard sidecar import
- Alertmanager routing
- Real OTLP flow under load
- SLO alert firing behavior
- Key Vault integration carried forward from v1.4.0

Traces use the Collector debug exporter and are not retained by a durable
trace backend in this release.

## Security boundary

No telemetry credential, Grafana administrator password, application secret,
or Key Vault secret value is embedded in this package.
