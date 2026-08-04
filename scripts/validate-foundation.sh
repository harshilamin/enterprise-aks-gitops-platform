#!/usr/bin/env bash
set -euo pipefail

echo "=== Validating Repository 2 foundation ==="

required_files=(
  "README.md"
  "CHANGELOG.md"
  "ROADMAP.md"
  "SECURITY.md"
  "CONTRIBUTING.md"
  "mkdocs.yml"
  "requirements-docs.txt"
  ".github/workflows/repository-ci.yml"
  ".github/workflows/docs-ci.yml"
  "docs/architecture/overview.md"
  "docs/security/security-model.md"
)

for file in "${required_files[@]}"; do
  test -f "${file}"
  echo "Found ${file}"
done

required_directories=(
  "apps/sample-api"
  "charts/sample-api"
  "gitops/applications"
  "gitops/projects"
  "gitops/environments/dev"
  "gitops/environments/qa"
  "gitops/environments/prod"
  "platform/argocd"
  "platform/observability"
  "platform/policies"
  "platform/secrets"
)

for directory in "${required_directories[@]}"; do
  test -d "${directory}"
  echo "Found ${directory}"
done

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  forbidden="$(
    git ls-files |
      grep -E '(^|/)\.env($|\.)|.*\.(pem|pfx|key)$|(^|/)kubeconfig$' ||
      true
  )"

  if [[ -n "${forbidden}" ]]; then
    echo "Sensitive files are tracked:"
    echo "${forbidden}"
    exit 1
  fi
fi

echo "Repository 2 foundation validation passed."
