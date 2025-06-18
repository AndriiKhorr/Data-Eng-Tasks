from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, IntegerType, StringType
from pyspark.sql.functions import input_file_name, to_date, regexp_extract, col

# Ініціалізація SparkSession
spark = SparkSession.builder \
    .appName("Process Customers Data") \
    .config("spark.sql.legacy.timeParserPolicy", "LEGACY") \
    .getOrCreate()

# Шляхи
raw_customers_path = "/opt/airflow/data/raw/customers"
bronze_path = "/opt/airflow/data/bronze/customers"
silver_path = "/opt/airflow/data/silver/customers"

# Схема для Bronze (залишаємо назви як у CSV)
schema_bronze = StructType() \
    .add("client_id", IntegerType()) \
    .add("first_name", StringType()) \
    .add("last_name", StringType()) \
    .add("email", StringType()) \
    .add("registration_date", StringType()) \
    .add("state", StringType())

# Зчитування всіх CSV-файлів з усіх підпапок
df_bronze = spark.read.option("header", True) \
    .schema(schema_bronze) \
    .csv(f"{raw_customers_path}/*/*.csv")

# Збереження в Bronze
df_bronze.write.mode("overwrite").parquet(bronze_path)

# Silver: чистимо типи + прибираємо дублікати
df_silver = df_bronze.withColumn(
    "registration_date", to_date("registration_date", "yyyy-MM-dd")
).dropDuplicates(["client_id"])

# Збереження в Silver (без партиціонування)
df_silver.write.mode("overwrite").parquet(silver_path)

# Перевірка схеми
df_silver.printSchema()

# Завершення
spark.stop()
