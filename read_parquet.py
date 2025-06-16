import pandas as pd
import glob

# Зчитуємо всі .parquet файли з усіх purchase_date підпапок
parquet_files = glob.glob("data/silver/sales/purchase_date=*/part-*.parquet")

# Перевіримо, скільки файлів знайшлось
print(f"🗂️ Found {len(parquet_files)} parquet files.")

# Зчитаємо всі файли у один DataFrame
df = pd.concat([pd.read_parquet(p) for p in parquet_files], ignore_index=True)

# Виводимо перші рядки
print(df.head())
