import pyarrow.parquet as pq
import pandas as pd

# Шлях до директорії з паркеткою
folder_path = "data/gold/user_profiles_enriched"

# Читаємо всі файли в цій папці
table = pq.ParquetDataset(folder_path).read()
df = table.to_pandas()

# Виводимо схему
print("📄 Схема таблиці:")
print(table.schema)

# Рахуємо кількість пропусків у кожній колонці
print("\n📊 Пропуски у колонках:")
print(df.isnull().sum())
