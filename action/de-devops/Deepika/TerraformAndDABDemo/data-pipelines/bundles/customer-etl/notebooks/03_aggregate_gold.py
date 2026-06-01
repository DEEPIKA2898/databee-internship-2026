# Databricks notebook source
# ============================================================
# 03_aggregate_gold.py
# Stage 3 — Aggregate silver → gold
# Reads dev.silver.customers
# Writes to dev.gold.customer_summary
# ============================================================

# COMMAND ----------
# MAGIC %md
# MAGIC ## Gold Layer — Business Aggregations
# MAGIC Aggregates customer data into business-ready summary metrics.

# COMMAND ----------
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, count, sum, avg, max, min,
    round, current_timestamp
)

spark = SparkSession.builder.getOrCreate()

# COMMAND ----------
catalog = dbutils.widgets.get("catalog") if dbutils.widgets.getAll() else "dev"

source_table = f"{catalog}.silver.customers"
target_table = f"{catalog}.gold.customer_summary"

print(f"Reading from: {source_table}")

# COMMAND ----------
# Read from silver
df_silver = spark.read.table(source_table)
print(f"Silver rows: {df_silver.count()}")

# COMMAND ----------
# Aggregate by country
df_gold = df_silver \
    .groupBy("country") \
    .agg(
        count("customer_id").alias("total_customers"),
        sum("total_orders").alias("total_orders"),
        round(sum("total_spend"), 2).alias("total_revenue"),
        round(avg("total_spend"), 2).alias("avg_spend_per_customer"),
        round(avg("total_orders"), 1).alias("avg_orders_per_customer"),
        sum(col("is_high_value").cast("integer")).alias("high_value_customers"),
        max("signup_date").alias("latest_signup"),
        min("signup_date").alias("earliest_signup")
    ) \
    .withColumn("_aggregated_at", current_timestamp()) \
    .orderBy("total_revenue", ascending=False)

# COMMAND ----------
# Write to gold
print(f"Writing to {target_table}...")

df_gold.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(target_table)

print(f"✅ Written {df_gold.count()} rows to {target_table}")
df_gold.show()
