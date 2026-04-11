# silver_utils.py
def trim_string_columns(df):
    from pyspark.sql.functions import trim, col
    from pyspark.sql.types import StringType
    for field in df.schema.fields:
        if isinstance(field.dataType, StringType):
            df = df.withColumn(field.name, trim(col(field.name)))
    return df

# To import in any notebook:
# %run /path/to/silver_utils
# df = trim_string_columns(df)