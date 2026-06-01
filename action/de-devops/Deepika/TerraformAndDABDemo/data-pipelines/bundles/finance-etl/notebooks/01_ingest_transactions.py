# Databricks notebook source
# ============================================================
# 01_ingest_transactions.py
# Stage 1 — Ingest raw transactions CSV into bronze layer
# Writes to dev.bronze.raw_transactions
# ============================================================

# COMMAND ----------
# MAGIC %md
# MAGIC ## Bronze Layer — Raw Transaction Ingestion
# MAGIC Reads transactions.csv and writes raw data to bronze schema.

# COMMAND ----------
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, lit
from datetime import datetime

spark = SparkSession.builder.getOrCreate()

# COMMAND ----------
catalog   = dbutils.widgets.get("catalog")   if dbutils.widgets.getAll() else "dev"
file_path = dbutils.widgets.get("file_path") if dbutils.widgets.getAll() else "/Volumes/dev/default/landing/transactions.csv"

print(f"Catalog:   {catalog}")
print(f"File path: {file_path}")

# COMMAND ----------
print("Reading transactions CSV...")
df_raw = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(file_path)

print(f"Rows read: {df_raw.count()}")
df_raw.printSchema()

# COMMAND ----------
df_bronze = df_raw \
    .withColumn("_ingested_at",   current_timestamp()) \
    .withColumn("_source_file",   lit(file_path)) \
    .withColumn("_pipeline_run",  lit(datetime.now().strftime("%Y%m%d_%H%M%S")))

# COMMAND ----------
target_table = f"{catalog}.bronze.raw_transactions"
print(f"Writing to {target_table}...")

df_bronze.write \
    .format("delta") \
    .mode("append") \
    .saveAsTable(target_table)

print(f"✅ Written {df_bronze.count()} rows to {target_table}")
df_bronze.show(5)
