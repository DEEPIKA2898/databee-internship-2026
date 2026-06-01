# Databricks notebook source
# ============================================================
# 04_payment_analysis.py
# Stage 4 — Payment method analysis → gold
# Writes to dev.gold.payment_analysis
# ============================================================

# COMMAND ----------
# MAGIC %md
# MAGIC ## Gold Layer — Payment Method Analysis
# MAGIC Breaks down transactions by payment method and currency.

# COMMAND ----------
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, count, sum, avg,
    round as spark_round, current_timestamp
)

spark = SparkSession.builder.getOrCreate()

# COMMAND ----------
catalog      = dbutils.widgets.get("catalog") if dbutils.widgets.getAll() else "dev"
source_table = f"{catalog}.silver.transactions"
target_table = f"{catalog}.gold.payment_analysis"

# COMMAND ----------
df_silver = spark.read.table(source_table)

# COMMAND ----------
df_gold = df_silver \
    .groupBy("payment_method", "currency") \
    .agg(
        count("transaction_id").alias("total_transactions"),
        spark_round(sum("amount"), 2).alias("total_amount"),
        spark_round(avg("amount"), 2).alias("avg_amount"),
        count(col("is_refunded").cast("integer") == 1).alias("refund_count"),
    ) \
    .withColumn("_aggregated_at", current_timestamp()) \
    .orderBy("total_amount", ascending=False)

# COMMAND ----------
print(f"Writing to {target_table}...")

df_gold.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(target_table)

print(f"✅ Written {df_gold.count()} rows to {target_table}")
df_gold.show()
