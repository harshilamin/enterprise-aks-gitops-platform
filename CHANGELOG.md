# Changelog

## [1.1.0] - 2026-08-03

### Added

- Secure FastAPI application
- Python 3.14.6 local and container baseline
- Python 3.12 and 3.14 CI matrix
- Liveness, readiness, and startup endpoints
- Structured JSON logging
- Request-correlation middleware
- Security response headers
- Runtime environment validation
- Production API-documentation hardening
- Graceful application lifecycle
- Unit and lifecycle tests
- 90% coverage quality gate
- Ruff formatting and linting
- Strict mypy type checking
- Multi-stage non-root Docker image
- Read-only hardened Compose runtime
- Container health and smoke testing
- Trivy vulnerability scanning
- CycloneDX SBOM generation
- Dependabot for Python, Docker, and GitHub Actions
- Application architecture, security, testing, and operations documentation

### Changed

- GitHub Actions were updated to Node 24-compatible major versions.
- Root secret-directory ignore rules now allow `platform/secrets` to remain tracked.

## [1.0.0] - 2026-08-03

### Added

- Repository foundation
- AKS GitOps architecture
- Dev, QA, and Production delivery model
- Repository skeleton
- Architecture Decision Records
- Governance and security policies
- MkDocs documentation site
- Repository and documentation CI
- Foundation validation scripts
- Release roadmap
