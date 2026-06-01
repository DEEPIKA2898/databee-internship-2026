# Databricks notebook source
# ============================================================
# 02_clean_transactions.py
# Stage 2 — Clean and validate bronze → silver
# Writes to dev.silver.transactions
# ============================================================

# COMMAND ----------
# MAGIC %md
# MAGIC ## Silver Layer — Clean Transactions
# MAGIC Validates, deduplicates, and enriches transaction data.

# COMMAND ----------
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, trim, upper, lower, to_date,
    when, current_timestamp, round as spark_round,
    regexp_replace, abs as spark_abs
)

spark = SparkSession.builder.getOrCreate()

# COMMAND ----------
catalog      = dbutils.widgets.get("catalog") if dbutils.widgets.getAll() else "dev"
source_table = f"{catalog}.bronze.raw_transactions"
target_table = f"{catalog}.silver.transactions"

print(f"Reading from: {source_table}")

# COMMAND ----------
df_bronze = spark.read.table(source_table)
print(f"Bronze rows: {df_bronze.count()}")

# COMMAND ----------
df_silver = df_bronze \
    .withColumn("transaction_id",   trim(col("transaction_id"))) \
    .withColumn("customer_id",      trim(col("customer_id"))) \
    .withColumn("transaction_date", to_date(col("transaction_date"), "yyyy-MM-dd")) \
    .withColumn("amount",           spark_abs(col("amount").cast("double"))) \
    .withColumn("currency",         trim(upper(col("currency")))) \
    .withColumn("category",         trim(col("category"))) \
    .withColumn("status",           trim(lower(col("status")))) \
    .withColumn("payment_method",   trim(lower(col("payment_method")))) \
    .withColumn("country",          trim(col("country"))) \
    .withColumn("is_refunded",      when(col("status") == "refunded", True).otherwise(False)) \
    .withColumn("is_completed",     when(col("status") == "completed", True).otherwise(False)) \
    .withColumn("is_high_value",    when(col("amount") > 500, True).otherwise(False)) \
    .withColumn("_processed_at",    current_timestamp()) \
    .filter(col("transaction_id").isNotNull()) \
    .filter(col("amount") > 0) \
    .dropDuplicates(["transaction_id"])

print(f"Silver rows after cleaning: {df_silver.count()}")
print(f"Completed: {df_silver.filter(col('is_completed')).count()}")
print(f"Refunded:  {df_silver.filter(col('is_refunded')).count()}")

# COMMAND ----------
print(f"Writing to {target_table}...")

df_silver.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(target_table)

print(f"✅ Written {df_silver.count()} rows to {target_table}")
df_silver.show(5)
