import os
import pyarrow.parquet as pq

# Шлях до директорії
parquet_dir = os.path.join("data", "silver", "customers_updated_from_user_profiles")

# Знаходимо перший .parquet файл
files = [f for f in os.listdir(parquet_dir) if f.endswith(".parquet")]

if not files:
    raise FileNotFoundError("У директорії немає .parquet файлів")

# Побудова повного шляху
file_path = os.path.join(parquet_dir, files[0])

# Читання схеми
parquet_file = pq.ParquetFile(file_path)
print("Схема файлу:\n")
print(parquet_file.schema)
