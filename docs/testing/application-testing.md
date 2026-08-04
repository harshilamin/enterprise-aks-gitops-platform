# Application Testing

## Test layers

### Configuration tests

Validate supported environments, logging levels, service names, and versions.

### Endpoint tests

Validate service metadata, health endpoints, runtime information, request IDs, security headers, and 404 behavior.

### Lifecycle tests

Confirm readiness changes during application startup and shutdown.

### Container smoke test

CI starts the hardened image and calls liveness, readiness, and information endpoints.

## Quality gates

- Ruff formatter
- Ruff linter
- Strict mypy
- pytest
- Branch coverage
- Minimum total coverage of 90%
- Python 3.12 and Python 3.14
