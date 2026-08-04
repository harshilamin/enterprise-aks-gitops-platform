#!/usr/bin/env bash
set -euo pipefail

namespace="${NAMESPACE:-monitoring}"
secret_name="${SECRET_NAME:-grafana-admin-credentials}"
admin_user="${ADMIN_USER:-admin}"

read -r -s -p "Enter the Grafana administrator password: " admin_password
printf '\n'

kubectl create namespace "${namespace}" \
  --dry-run=client \
  --output yaml | kubectl apply -f -

kubectl create secret generic "${secret_name}" \
  --namespace "${namespace}" \
  --from-literal="admin-user=${admin_user}" \
  --from-literal="admin-password=${admin_password}" \
  --dry-run=client \
  --output yaml | kubectl apply -f -

unset admin_password
echo "Grafana administrator secret created without writing the password to disk."
