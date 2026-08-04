#!/usr/bin/env bash
set -euo pipefail
"$(dirname "$0")/validate-foundation.sh"
"$(dirname "$0")/validate-app.sh"
"$(dirname "$0")/validate-helm.sh"
"$(dirname "$0")/validate-gitops.sh"
"$(dirname "$0")/validate-identity.sh"
"$(dirname "$0")/validate-observability.sh"
"$(dirname "$0")/validate-final-platform.sh"
python -m mkdocs build --strict
echo "Repository 2 v2.0.0 validation passed."
