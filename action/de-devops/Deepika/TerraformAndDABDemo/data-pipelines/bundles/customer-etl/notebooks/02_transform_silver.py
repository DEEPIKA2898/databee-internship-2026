# Databricks notebook source
# ============================================================
# 02_transform_silver.py
# Stage 2 — Clean and conform bronze → silver
# Reads dev.bronze.raw_customers
# Writes to dev.silver.customers
# ============================================================

# COMMAND ----------
# MAGIC %md
# MAGIC ## Silver Layer — Cleanse & Conform
# MAGIC Reads from bronze, applies data quality rules, writes clean data to silver.

# COMMAND ----------
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, trim, upper, lower, to_date,
    when, current_timestamp, regexp_replace
)

spark = SparkSession.builder.getOrCreate()

# COMMAND ----------
catalog = dbutils.widgets.get("catalog") if dbutils.widgets.getAll() else "dev"

source_table = f"{catalog}.bronze.raw_customers"
target_table = f"{catalog}.silver.customers"

print(f"Reading from: {source_table}")

# COMMAND ----------
# Read from bronze
df_bronze = spark.read.table(source_table)
print(f"Bronze rows: {df_bronze.count()}")

# COMMAND ----------
# Apply transformations
df_silver = df_bronze \
    .withColumn("customer_id",  trim(col("customer_id"))) \
    .withColumn("first_name",   trim(col("first_name"))) \
    .withColumn("last_name",    trim(col("last_name"))) \
    .withColumn("email",        lower(trim(col("email")))) \
    .withColumn("country",      trim(col("country"))) \
    .withColumn("signup_date",  to_date(col("signup_date"), "yyyy-MM-dd")) \
    .withColumn("total_orders", col("total_orders").cast("integer")) \
    .withColumn("total_spend",  col("total_spend").cast("double")) \
    .withColumn("is_high_value", when(col("total_spend") > 1000, True).otherwise(False)) \
    .withColumn("_processed_at", current_timestamp()) \
    .filter(col("customer_id").isNotNull()) \
    .filter(col("email").contains("@")) \
    .dropDuplicates(["customer_id"])

print(f"Silver rows after cleaning: {df_silver.count()}")

# COMMAND ----------
# Write to silver
print(f"Writing to {target_table}...")

df_silver.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(target_table)

print(f"✅ Written {df_silver.count()} rows to {target_table}")
df_silver.show(5)
