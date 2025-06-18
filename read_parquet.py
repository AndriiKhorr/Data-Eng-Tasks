import pandas as pd
from pathlib import Path

# Шлях до директорії з parquet-файлами
silver_path = Path("data/silver/customers")

# Зчитуємо всі .parquet файли в директорії
all_files = list(silver_path.glob("*.parquet"))

# Об'єднуємо всі файли в один DataFrame
df = pd.concat([pd.read_parquet(file) for file in all_files], ignore_index=True)

# Виводимо кілька перших рядків
print(df.head())

# Перевіримо типи колонок
print("\n Типи колонок:")
print(df.dtypes)
