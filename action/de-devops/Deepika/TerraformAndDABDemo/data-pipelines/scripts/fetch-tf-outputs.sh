#!/bin/bash
# Fetch Terraform outputs from Key Vault
# Usage: source ./scripts/fetch-tf-outputs.sh dev kv-platform-dev-001

ENV=${1:-dev}
KV_NAME=${2:-"kv-platform-dev-001"}

echo ">> Fetching outputs from Key Vault: $KV_NAME"

TF_JSON=$(az keyvault secret show \
  --vault-name "$KV_NAME" \
  --name "tf-outputs" \
  --query "value" -o tsv)

export DATABRICKS_HOST=$(echo "$TF_JSON"  | jq -r '.workspace_url.value')
export CLUSTER_ID=$(echo "$TF_JSON"       | jq -r '.cluster_id.value')
export CATALOG_NAME=$(echo "$TF_JSON"     | jq -r '.catalog_name.value')
export SECRET_SCOPE=$(echo "$TF_JSON"     | jq -r '.secret_scope_name.value')

echo "Workspace: $DATABRICKS_HOST"
echo "Cluster:   $CLUSTER_ID"
echo "Catalog:   $CATALOG_NAME"
