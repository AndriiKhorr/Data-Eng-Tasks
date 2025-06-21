from pyspark.sql import SparkSession
from pyspark.sql.functions import col, input_file_name, regexp_extract, to_date, year, regexp_replace, sum as _sum, count as _count
from pyspark.sql.types import IntegerType, DoubleType

spark = SparkSession.builder.appName("TopTVSalesByStateRaw").getOrCreate()

# 1. Шлях до сирих продажів
raw_sales_path = "/opt/airflow/data/raw/sales/*/*.csv"

# 2. Читання продажів + дата з шляху
sales_df = (
    spark.read.option("header", True).csv(raw_sales_path)
    .withColumn("purchase_date", regexp_extract(input_file_name(), r"sales/(\d{4}-\d{2}-\d{1,2})", 1))
    .withColumn("purchase_date", to_date("purchase_date"))
)

# 3. Фільтрація: лише TV + перша декада вересня
sales_filtered = sales_df.filter(
    (col("Product") == "TV") &
    (col("purchase_date") >= "2022-09-01") &
    (col("purchase_date") <= "2022-09-10")
)

# 4. Очищення ціни: видалення $ + перетворення в число
sales_filtered = sales_filtered.withColumn(
    "Price", regexp_replace("Price", "[$]", "").cast(DoubleType())
)

# 5. Зчитування профілів клієнтів (gold)
profiles_path = "/opt/airflow/data/gold/user_profiles_enriched"
profiles_df = spark.read.parquet(profiles_path)

# 6. Додавання віку
profiles_df = profiles_df.withColumn(
    "age", (2022 - year(to_date("birth_date"))).cast(IntegerType())
)

# 7. Фільтрація віку 20–30
profiles_filtered = profiles_df.filter((col("age") >= 20) & (col("age") <= 30))

# 8. Join по CustomerId == client_id
joined_df = sales_filtered.join(
    profiles_filtered,
    sales_filtered.CustomerId == profiles_filtered.client_id,
    how="inner"
)

# 9. Агрегація
agg_df = joined_df.groupBy("state").agg(
    _count("*").alias("tv_count"),
    _sum("Price").alias("total_spent")
)

# 10. Топ 5 по кількості
print("Топ 5 штатів за кількістю покупок телевізорів:")
agg_df.orderBy(col("tv_count").desc()).show(5, truncate=False)

# 11. Топ 5 по сумі
print("Топ 5 штатів за витратами на телевізори:")
agg_df.orderBy(col("total_spent").desc()).show(5, truncate=False)

spark.stop()
