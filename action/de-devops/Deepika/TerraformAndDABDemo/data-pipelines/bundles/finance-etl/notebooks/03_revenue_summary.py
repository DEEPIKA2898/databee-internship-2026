# Databricks notebook source
# ============================================================
# 03_revenue_summary.py
# Stage 3 — Revenue summary silver → gold
# Writes to dev.gold.revenue_summary
# ============================================================

# COMMAND ----------
# MAGIC %md
# MAGIC ## Gold Layer — Revenue Summary
# MAGIC Aggregates transaction data into business-ready revenue metrics.

# COMMAND ----------
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, count, sum, avg, max, min,
    round as spark_round, current_timestamp,
    countDistinct
)

spark = SparkSession.builder.getOrCreate()

# COMMAND ----------
catalog      = dbutils.widgets.get("catalog") if dbutils.widgets.getAll() else "dev"
source_table = f"{catalog}.silver.transactions"
target_table = f"{catalog}.gold.revenue_summary"

# COMMAND ----------
df_silver = spark.read.table(source_table)
print(f"Silver rows: {df_silver.count()}")

# COMMAND ----------
# Revenue summary by category and country
df_gold = df_silver \
    .filter(col("is_completed") == True) \
    .groupBy("category", "country") \
    .agg(
        count("transaction_id").alias("total_transactions"),
        countDistinct("customer_id").alias("unique_customers"),
        spark_round(sum("amount"), 2).alias("total_revenue"),
        spark_round(avg("amount"), 2).alias("avg_transaction_value"),
        spark_round(sum(col("is_high_value").cast("integer")) / count("transaction_id") * 100, 1).alias("high_value_pct"),
        max("transaction_date").alias("latest_transaction"),
        min("transaction_date").alias("earliest_transaction")
    ) \
    .withColumn("_aggregated_at", current_timestamp()) \
    .orderBy("total_revenue", ascending=False)

# COMMAND ----------
print(f"Writing to {target_table}...")

df_gold.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(target_table)

print(f"✅ Written {df_gold.count()} rows to {target_table}")
df_gold.show(20)
