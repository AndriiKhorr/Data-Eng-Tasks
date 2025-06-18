from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, split, to_date
from pyspark.sql.types import StructType, StringType

# 1. Створення SparkSession
spark = SparkSession.builder \
    .appName("Enrich Customers from User Profiles") \
    .getOrCreate()

# 2. Шляхи до даних
customers_path = "/opt/airflow/data/silver/customers"
profiles_path = "/opt/airflow/data/raw/user_profiles/user_profiles.json"
output_path = "/opt/airflow/data/silver/customers_updated_from_user_profiles"

# 3. Читання silver/customers
df_customers = spark.read.parquet(customers_path)
df_customers = df_customers.withColumn("registration_date", to_date(col("registration_date")))

# 4. Схема для JSON user_profiles
schema_profiles = StructType() \
    .add("email", StringType()) \
    .add("full_name", StringType()) \
    .add("state", StringType()) \
    .add("birth_date", StringType()) \
    .add("phone_number", StringType())

# 5. Читання JSON-файлу з user_profiles
df_profiles = spark.read.schema(schema_profiles).json(profiles_path)

# 6. Розділення full_name та перейменування state
df_profiles = df_profiles \
    .withColumn("first_name_profile", split(col("full_name"), " ").getItem(0)) \
    .withColumn("last_name_profile", split(col("full_name"), " ").getItem(1)) \
    .withColumnRenamed("state", "state_profile")

# 7. Join по email
df_joined = df_customers.join(df_profiles, on="email", how="left")

# 8. Заповнення пропусків лише там, де потрібно
df_enriched = df_joined.select(
    "client_id",
    when(col("first_name").isNull(), col("first_name_profile")).otherwise(col("first_name")).alias("first_name"),
    when(col("last_name").isNull(), col("last_name_profile")).otherwise(col("last_name")).alias("last_name"),
    "email",
    "registration_date",
    when(col("state").isNull(), col("state_profile")).otherwise(col("state")).alias("state")
)

# 9. Запис збагачених даних у silver/customers_updated_from_user_profiles
df_enriched.write.mode("overwrite").parquet(output_path)

print(f"Збагачені дані збережено в: {output_path}")
spark.stop()
