#!/usr/bin/env bash
set -euo pipefail

echo "=== Validating Repository 2 v1.2.0 ==="

"$(dirname "$0")/validate-foundation.sh"
"$(dirname "$0")/validate-app.sh"
"$(dirname "$0")/validate-helm.sh"
python -m mkdocs build --strict

echo "Repository 2 v1.2.0 validation passed."
