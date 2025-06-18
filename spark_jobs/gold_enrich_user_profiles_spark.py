from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date

# Ініціалізація SparkSession
spark = SparkSession.builder.appName("gold_enrich_user_profiles").getOrCreate()

# === 1. Зчитуємо raw user_profiles.json ===
raw_user_profiles_path = "/opt/airflow/data/raw/user_profiles/user_profiles.json"
user_profiles_raw_df = spark.read.json(raw_user_profiles_path)

# === 2. Записуємо user_profiles у SILVER (перетворюємо в Parquet) ===
silver_user_profiles_path = "/opt/airflow/data/silver/user_profiles"
user_profiles_raw_df.write.mode("overwrite").parquet(silver_user_profiles_path)

# === 3. Зчитуємо customers_updated_from_user_profiles ===
customers_path = "/opt/airflow/data/silver/customers_updated_from_user_profiles"
customers_df = spark.read.parquet(customers_path)

# === 4. Зчитуємо user_profiles з silver, перетворюємо birth_date на тип date ===
user_profiles_df = spark.read.parquet(silver_user_profiles_path)
user_profiles_df = user_profiles_df.withColumn("birth_date", to_date("birth_date", "yyyy-MM-dd"))

# === 5. Join по email ===
enriched_df = customers_df.join(
    user_profiles_df.select("email", "birth_date", "phone_number"),
    on="email",
    how="left"
)

# === 6. Запис у GOLD ===
output_path = "/opt/airflow/data/gold/user_profiles_enriched"
enriched_df.write.mode("overwrite").parquet(output_path)

# Завершення
spark.stop()
