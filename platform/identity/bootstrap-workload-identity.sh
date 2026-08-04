#!/usr/bin/env bash
set -euo pipefail

required_variables=(
  SUBSCRIPTION_ID
  RESOURCE_GROUP
  CLUSTER_NAME
  IDENTITY_NAME
  KEY_VAULT_NAME
  ENVIRONMENT
)

for variable in "${required_variables[@]}"; do
  if [[ -z "${!variable:-}" ]]; then
    echo "${variable} is required." >&2
    exit 1
  fi
done

case "${ENVIRONMENT}" in
  dev|qa|prod) ;;
  *)
    echo "ENVIRONMENT must be dev, qa, or prod." >&2
    exit 1
    ;;
esac

if [[ "$#" -lt 1 ]]; then
  echo "Pass one or more Key Vault secret names as arguments." >&2
  exit 1
fi

namespace="${NAMESPACE:-sample-api-${ENVIRONMENT}}"
service_account_name="${SERVICE_ACCOUNT_NAME:-sample-api}"
federated_credential_name="${FEDERATED_CREDENTIAL_NAME:-${IDENTITY_NAME}-${ENVIRONMENT}}"
role_id="4633458b-17de-408a-b874-0445c86b69e6"

az account show --output none --only-show-errors
az account set --subscription "${SUBSCRIPTION_ID}" --only-show-errors

az aks update \
  --resource-group "${RESOURCE_GROUP}" \
  --name "${CLUSTER_NAME}" \
  --enable-oidc-issuer \
  --enable-workload-identity \
  --output none \
  --only-show-errors

az aks enable-addons \
  --resource-group "${RESOURCE_GROUP}" \
  --name "${CLUSTER_NAME}" \
  --addons azure-keyvault-secrets-provider \
  --output none \
  --only-show-errors

if ! az identity show \
  --resource-group "${RESOURCE_GROUP}" \
  --name "${IDENTITY_NAME}" \
  --output none \
  --only-show-errors 2>/dev/null; then
  az identity create \
    --resource-group "${RESOURCE_GROUP}" \
    --name "${IDENTITY_NAME}" \
    --output none \
    --only-show-errors
fi

client_id="$(az identity show \
  --resource-group "${RESOURCE_GROUP}" \
  --name "${IDENTITY_NAME}" \
  --query clientId \
  --output tsv \
  --only-show-errors)"

principal_id="$(az identity show \
  --resource-group "${RESOURCE_GROUP}" \
  --name "${IDENTITY_NAME}" \
  --query principalId \
  --output tsv \
  --only-show-errors)"

tenant_id="$(az account show \
  --query tenantId \
  --output tsv \
  --only-show-errors)"

oidc_issuer="$(az aks show \
  --resource-group "${RESOURCE_GROUP}" \
  --name "${CLUSTER_NAME}" \
  --query oidcIssuerProfile.issuerUrl \
  --output tsv \
  --only-show-errors)"

key_vault_rbac="$(az keyvault show \
  --name "${KEY_VAULT_NAME}" \
  --query properties.enableRbacAuthorization \
  --output tsv \
  --only-show-errors)"

if [[ "${key_vault_rbac}" != "true" ]]; then
  echo "Key Vault ${KEY_VAULT_NAME} must use Azure RBAC authorization." >&2
  exit 1
fi

key_vault_scope="$(az keyvault show \
  --name "${KEY_VAULT_NAME}" \
  --query id \
  --output tsv \
  --only-show-errors)"

role_assignment="$(az role assignment list \
  --assignee-object-id "${principal_id}" \
  --scope "${key_vault_scope}" \
  --query "[?roleDefinitionId && contains(roleDefinitionId, '${role_id}')].id | [0]" \
  --output tsv \
  --only-show-errors)"

if [[ -z "${role_assignment}" ]]; then
  az role assignment create \
    --assignee-object-id "${principal_id}" \
    --assignee-principal-type ServicePrincipal \
    --role "${role_id}" \
    --scope "${key_vault_scope}" \
    --output none \
    --only-show-errors
fi

if ! az identity federated-credential show \
  --resource-group "${RESOURCE_GROUP}" \
  --identity-name "${IDENTITY_NAME}" \
  --name "${federated_credential_name}" \
  --output none \
  --only-show-errors 2>/dev/null; then
  az identity federated-credential create \
    --resource-group "${RESOURCE_GROUP}" \
    --identity-name "${IDENTITY_NAME}" \
    --name "${federated_credential_name}" \
    --issuer "${oidc_issuer}" \
    --subject "system:serviceaccount:${namespace}:${service_account_name}" \
    --audiences api://AzureADTokenExchange \
    --output none \
    --only-show-errors
fi

generator_arguments=(
  scripts/generate_workload_identity_values.py
  --repository-root .
  --environment "${ENVIRONMENT}"
  --client-id "${client_id}"
  --tenant-id "${tenant_id}"
  --key-vault-name "${KEY_VAULT_NAME}"
)

for secret_name in "$@"; do
  generator_arguments+=(--secret-name "${secret_name}")
done

if [[ "${MERGE_GITOPS:-false}" == "true" ]]; then
  generator_arguments+=(--merge-gitops)
fi

python "${generator_arguments[@]}"

echo "Workload Identity bootstrap completed."
echo "Namespace: ${namespace}"
echo "Service account: ${service_account_name}"
echo "Managed identity client ID: ${client_id}"
echo "No secret values were written or displayed."
