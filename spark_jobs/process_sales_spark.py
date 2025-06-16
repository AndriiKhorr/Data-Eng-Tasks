from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, regexp_replace
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

# Створення Spark сесії
spark = SparkSession.builder \
    .appName("Process Sales Data") \
    .getOrCreate()

# Шляхи до даних
raw_sales_path = "/opt/airflow/data/raw/sales"
bronze_path = "/opt/airflow/data/bronze/sales"
silver_path = "/opt/airflow/data/silver/sales"

# === Крок 1: Читаємо CSV у STRING-схемі (schema-on-read)
schema_bronze = StructType([
    StructField("CustomerId", StringType(), True),
    StructField("PurchaseDate", StringType(), True),
    StructField("Product", StringType(), True),
    StructField("Price", StringType(), True),
])

df_bronze = spark.read \
    .option("header", True) \
    .schema(schema_bronze) \
    .csv(f"{raw_sales_path}/*/*.csv")

# Зберігаємо як CSV без змін (bronze зона)
df_bronze.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv(bronze_path)

print("✅ Bronze sales CSV saved.")

# === Крок 2: Чистка та трансформація у Silver

df_silver = df_bronze \
    .withColumnRenamed("CustomerId", "client_id") \
    .withColumnRenamed("PurchaseDate", "purchase_date") \
    .withColumnRenamed("Product", "product_name") \
    .withColumnRenamed("Price", "price") \
    .withColumn(
        "purchase_date",
        to_date(
            regexp_replace("purchase_date", r"(\d{4}-\d{2})-(\d{1})$", r"\1-0\2"),
            "yyyy-MM-dd"
        )
    ) \
    .withColumn("price", col("price").cast(DoubleType()))

# Зберігаємо як partitioned Parquet (silver зона)
df_silver.write \
    .mode("overwrite") \
    .partitionBy("purchase_date") \
    .parquet(silver_path)

print("✅ Silver sales saved with proper schema and partitions.")

spark.stop()
