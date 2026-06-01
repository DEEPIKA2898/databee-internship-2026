# data-pipelines

> Customer ETL pipeline using Databricks Asset Bundles (DABs) — automated with GitHub Actions.

## Overview

This repository contains Databricks data pipelines that run on the infrastructure provisioned by the `platform-infra` repo. Pipelines are packaged as Databricks Asset Bundles and deployed via GitHub Actions.

```
GitHub Actions pipeline
        ↓
Reads infrastructure outputs from Azure Key Vault
        ↓
Deploys Databricks Asset Bundle
        ↓
Runs ETL job (CSV → bronze → silver → gold)
        ↓
Data available in Unity Catalog
```

---

## Pipeline — Customer ETL

Reads a CSV file of customer data and processes it through the medallion architecture.

```
customers.csv  (raw source)
      ↓
dev.bronze.raw_customers   (raw ingested — append only)
      ↓
dev.silver.customers       (cleaned, validated, conformed)
      ↓
dev.gold.customer_summary  (aggregated by country)
```

### What each layer does

| Layer | Table | Transformation |
|---|---|---|
| Bronze | `dev.bronze.raw_customers` | Raw CSV rows + metadata columns. Append-only, no changes. |
| Silver | `dev.silver.customers` | Trimmed, lowercased emails, cast types, deduplicated, `is_high_value` flag added. |
| Gold | `dev.gold.customer_summary` | Grouped by country — total customers, revenue, avg spend, high-value count. |

---

## Repository Structure

```
data-pipelines/
├── bundles/
│   └── customer-etl/
│       ├── databricks.yml          # Bundle config — job, tasks, targets
│       ├── notebooks/
│       │   ├── 01_ingest_bronze.py    # CSV → bronze
│       │   ├── 02_transform_silver.py # bronze → silver
│       │   └── 03_aggregate_gold.py   # silver → gold
│       └── data/
│           └── customers.csv          # Sample data (15 Nordic customers)
├── scripts/
│   └── fetch-tf-outputs.sh         # Read Key Vault outputs locally
└── .github/
    └── workflows/
        └── deploy.yml              # CI/CD pipeline
```

---

## Pipeline Flow

```
Push to branch → Open PR
        ↓
✅ Validate Bundle (databricks bundle validate)
        ↓
Merge PR to main
        ↓
✅ Fetch outputs from Key Vault (workspace URL, catalog name)
        ↓
✅ Deploy bundle to dev (databricks bundle deploy)
        ↓
✅ Run ETL job (databricks bundle run)
        ↓
🔐 Deploy to staging (manual approval)
```

---

## Prerequisites

| Tool | Version | Install |
|---|---|---|
| Databricks CLI | >= 0.210 | https://docs.databricks.com/dev-tools/cli/install.html |
| Azure CLI | latest | https://learn.microsoft.com/cli/azure/install-azure-cli |
| Git | any | https://git-scm.com |

---

## GitHub Secrets Required

Add these in **Settings → Secrets → Actions** (repository level):

| Secret | Description | Where to find |
|---|---|---|
| `DATABRICKS_HOST` | Workspace URL | `terraform output workspace_url` in platform-infra |
| `DATABRICKS_TOKEN` | Personal access token | Databricks workspace → Settings → Developer → Access tokens |
| `ARM_CLIENT_ID` | Service Principal client ID | Same as platform-infra repo |
| `ARM_CLIENT_SECRET` | Service Principal secret | Same as platform-infra repo |
| `ARM_TENANT_ID` | Azure tenant ID | Same as platform-infra repo |

### GitHub Environment Variables

Add under **Settings → Environments → dev**:

| Variable | Value |
|---|---|
| `KV_NAME_DEV` | Key Vault name (e.g. `kv-platform-dev-001`) |

---

## Upload Sample Data

Before running the pipeline, upload the CSV to a Databricks Volume:

**Option 1 — Databricks UI:**
```
Databricks workspace → Catalog
→ dev → default → Volumes → landing
→ Upload to this volume → select customers.csv
```

**Option 2 — Databricks CLI:**
```bash
# Create volume
databricks volumes create dev default landing MANAGED

# Upload CSV
databricks fs cp \
  bundles/customer-etl/data/customers.csv \
  dbfs:/Volumes/dev/default/landing/customers.csv
```

---

## Local Development

```bash
# Set credentials
export DATABRICKS_HOST="https://adb-xxxx.azuredatabricks.net"
export DATABRICKS_TOKEN="dapi..."

# Navigate to bundle
cd bundles/customer-etl

# Validate bundle
databricks bundle validate --target dev

# Deploy bundle
databricks bundle deploy --target dev

# Run job
databricks bundle run --target dev customer_etl_pipeline

# Check job status
databricks bundle run --target dev customer_etl_pipeline --no-wait
```

---

## Verify Results

After a successful run, query the gold table in Databricks SQL Editor:

```sql
-- Gold layer — business metrics by country
SELECT
  country,
  total_customers,
  total_revenue,
  avg_spend_per_customer,
  high_value_customers
FROM dev.gold.customer_summary
ORDER BY total_revenue DESC;
```

Expected output:
```
country  | customers | revenue  | avg_spend | high_value
─────────────────────────────────────────────────────────
Sweden   | 6         | 7750.75  | 1291.79   | 4
Norway   | 4         | 3791.25  | 947.81    | 1
Denmark  | 3         | 2420.75  | 806.92    | 1
Finland  | 2         | 1790.25  | 895.13    | 0
```

---

## How It Connects to platform-infra

The pipeline reads Terraform outputs from Azure Key Vault:

```bash
# Key Vault secret: tf-outputs
{
  "workspace_url":    "https://adb-xxxx.azuredatabricks.net",
  "catalog_name":     "dev",
  "cluster_id":       "xxxx-xxxxxx-xxxxxxxx",
  "secret_scope_name":"kv-dev"
}
```

This means the data pipeline always uses the correct workspace and catalog — no hardcoded values.

---

## Adding a New Pipeline

1. Create a new folder under `bundles/`:
```
bundles/
└── your-pipeline/
    ├── databricks.yml
    └── notebooks/
```

2. Define the job in `databricks.yml`
3. Push to a branch → open PR → pipeline validates and deploys

---

## Troubleshooting

| Error | Fix |
|---|---|
| `cannot configure default credentials` | Check `DATABRICKS_HOST` and `DATABRICKS_TOKEN` secrets are set at repo level (not env level) |
| `notebook not found` | Add `.py` extension to notebook paths in `databricks.yml` |
| `catalog not found` | Check catalog name matches Key Vault output (`catalog_name`) |
| `volume not found` | Upload `customers.csv` to `/Volumes/dev/default/landing/` |
| `workspace.host interpolation` | Remove `workspace:` block from targets in `databricks.yml` |

---

## Related Repositories

- **platform-infra** — Terraform infrastructure (workspace, Unity Catalog, Key Vault, cluster)
