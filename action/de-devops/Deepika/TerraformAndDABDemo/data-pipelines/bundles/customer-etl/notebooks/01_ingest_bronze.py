# Databricks notebook source
# ============================================================
# 01_ingest_bronze.py
# Stage 1 — Ingest raw CSV into bronze layer
# Reads customers.csv and writes to dev.bronze.raw_customers
# ============================================================

# COMMAND ----------
# MAGIC %md
# MAGIC ## Bronze Layer — Raw Ingestion
# MAGIC Reads the raw CSV file and writes it to the bronze schema as-is.
# MAGIC No transformations — this is the source of truth.

# COMMAND ----------
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, lit
from datetime import datetime

spark = SparkSession.builder.getOrCreate()

# COMMAND ----------
# Configuration — passed as job parameters
catalog   = dbutils.widgets.get("catalog")    if dbutils.widgets.getAll() else "dev"
file_path = dbutils.widgets.get("file_path")  if dbutils.widgets.getAll() else "/Volumes/dev/default/landing/customers.csv"

print(f"Catalog:   {catalog}")
print(f"File path: {file_path}")

# COMMAND ----------
# Read raw CSV
print("Reading raw CSV...")
df_raw = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(file_path)

print(f"Rows read: {df_raw.count()}")
df_raw.printSchema()

# COMMAND ----------
# Add ingestion metadata
df_bronze = df_raw \
    .withColumn("_ingested_at", current_timestamp()) \
    .withColumn("_source_file", lit(file_path)) \
    .withColumn("_pipeline_run", lit(datetime.now().strftime("%Y%m%d_%H%M%S")))

# COMMAND ----------
# Write to bronze — append only
target_table = f"{catalog}.bronze.raw_customers"
print(f"Writing to {target_table}...")

df_bronze.write \
    .format("delta") \
    .mode("append") \
    .saveAsTable(target_table)

print(f"✅ Written {df_bronze.count()} rows to {target_table}")
df_bronze.show(5)
