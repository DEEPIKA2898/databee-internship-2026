# Use Case — Data Engineering & DevOps

**Track Lead:** Sanjeev Kumar

---

## Smart Retail Analytics Platform

A retail company operates both online and offline stores. They receive raw data from multiple sources — transactional databases, REST APIs, flat files, and real-time clickstream logs — and need an end-to-end data platform to power business reporting and customer intelligence.

---

## Data Sources

| Source | Type | Ingestion Method |
|---|---|---|
| Customer & Orders DB | PostgreSQL (OLTP) | CDC via Debezium |
| Product catalog | REST API (paginated JSON) | Python Requests |
| Store inventory & suppliers | CSV files (daily drops) | PySpark / Pandas |
| User clickstream / behavior | JSON event stream | Kafka → Structured Streaming |

---

## Pipeline Stages

### Stage 1 — Batch Ingestion (Bronze)

Ingest from batch sources (API, CSV, initial DB full load) into cloud storage (S3 / Azure Blob / GCS), partitioned by ingestion date. Raw data stored as-is in a lakehouse table format (Delta Lake, Iceberg, or Hudi).

**Skills:** Python, REST APIs, file handling, cloud storage basics, lakehouse table format fundamentals (ACID transactions, time travel, schema enforcement).

---

### Stage 2 — CDC & Incremental Ingestion (Bronze)

Set up Change Data Capture on the PostgreSQL source to capture inserts, updates, and deletes incrementally rather than full extracts.

**Skills:** Debezium, MERGE/upsert into lakehouse tables, understanding of CDC log structure, idempotent writes.

---

### Stage 3 — Streaming Ingestion (Bronze)

Ingest clickstream events from Kafka using Spark Structured Streaming. Write to Bronze as a continuously updating table with trigger-based micro-batches.

**Skills:** Kafka basics (topics, partitions, offsets), Structured Streaming, checkpointing, watermarking for late data.

---

### Stage 4 — Silver (Cleaning, Enrichment & SCD)

- Remove nulls, duplicates, invalid records.
- Standardize timestamps, currency, and encoding.
- Deduplicate using SQL Window Functions (`ROW_NUMBER`).
- Use CTEs for readable transformation logic.
- Join orders → customers → products.
- Implement SCD Type 2 on `dim_customer` and `dim_product` to track historical changes (effective dates, `is_current` flag).
- Enforce schema expectations — reject or quarantine records that violate contracts.

**Skills:** SQL (window functions, CTEs, MERGE), data quality expectations (Great Expectations or equivalent), schema evolution handling.

---

### Stage 5 — Gold: Star Schema Modeling with dbt

Design and build a Star Schema using dbt models:

- **Facts:** `fact_orders`, `fact_clickstream_sessions`
- **Dimensions:** `dim_customer`, `dim_product`, `dim_date`, `dim_store`
- **Business metrics models:** revenue by product, customer lifetime value, customer segments (High/Mid/Low), store performance, inventory health.

Add dbt tests: `not_null`, `unique`, `accepted_values`, `relationships`, and custom SQL tests for business logic validation. Add dbt contracts for column-level type and not-null enforcement on Gold models.

**Skills:** Dimensional modeling (Kimball), dbt (models, tests, contracts, documentation, `ref()`), Jinja templating basics.

---

### Stage 6 — Scale with PySpark

Re-implement Silver → Gold transformations in PySpark to handle production-scale data.

- Partition strategies (date-based, product-category).
- Caching and persistence for iterative jobs.
- Table optimization: MERGE, OPTIMIZE, Z-ORDER or equivalent compaction/clustering features of your chosen table format.
- Compare Pandas vs PySpark at 10 MB, 1 GB, and 10 GB+ to understand where distributed compute becomes necessary.

**Skills:** PySpark (DataFrames, SQL, UDFs), partitioning, broadcast joins, table format optimization, Spark UI for debugging (stages, tasks, shuffle, spill).

---

### Stage 7 — Orchestration

Build a daily pipeline orchestrated by Airflow (or equivalent scheduler):

- **Schedule:** Daily at 10 AM — extract → silver → gold → dbt run → notify.
- Retry logic with exponential backoff on transient failures.
- Failure alerts (email / Slack).
- Backfill support for reprocessing historical dates.
- Data quality sensor tasks — gate Gold layer on Silver quality checks passing.
- Dependency management — streaming Bronze runs independently; batch pipeline triggers downstream.

**Skills:** Airflow (DAGs, sensors, operators, XCom) or equivalent orchestrator (Prefect, Dagster, Mage), cron expressions, idempotent task design.

---

### Stage 8 — CI/CD & Production Hardening

#### Version Control & Branching
- Git branching strategy: `feature/*` → `dev` → `staging` → `main`.
- PR reviews for all pipeline code changes.
- dbt slim CI: only build/test modified models on PRs.

#### CI Pipeline (GitHub Actions)
- Lint (`flake8`/`ruff` for Python, `sqlfluff` for SQL).
- Unit tests for Python ETL functions (`pytest`).
- Integration tests: run pipeline on a small test dataset, assert row counts and schema.
- dbt build on staging profile.

#### CD Pipeline
- Environment-based dbt profiles (dev / staging / prod).
- Infrastructure as Code (Terraform / Pulumi) for provisioning compute and storage resources.
- Secret management (environment variables, vault, or platform-native secret scopes — never hardcoded).

#### Monitoring & Observability
- Pipeline run dashboards: success/failure rates, durations, data freshness.
- Alerting on data freshness SLA breaches and quality drift.
- Logging standards for all pipeline stages.

**Skills:** Git workflows, GitHub Actions, pytest, Terraform, secret management, monitoring basics.

---

## Implementation Notes

- Start small (10 MB datasets), then scale to 10 GB+ to understand where distributed systems shine.
- Use sample data generators (Faker, or similar libraries) to create realistic datasets for each stage.
- Each stage should be completed and reviewed before moving to the next — resist the urge to skip ahead.
