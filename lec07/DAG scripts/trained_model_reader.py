import os
import re
import pandas as pd
from joblib import load
from sqlalchemy import create_engine

# 1. Параметри БД
DB_USER = "analytics_admin"
DB_PASS = "admin123"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "analytics"
TABLE = "homework.iris_processed"

# 2. Підключення до PostgreSQL
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# 3. Отримуємо назви колонок
df_sample = pd.read_sql("SELECT * FROM homework.iris_processed WHERE source_date = '2025-04-22'", con=engine)
X_columns = df_sample.drop(columns=["species", "source_date"]).columns.tolist()

# 4. Папка з моделями
MODEL_DIR = "lec07/data-platform/airflow/models"
rows = []

# 5. Обхід .joblib файлів
for filename in sorted(os.listdir(MODEL_DIR)):
    if not filename.endswith(".joblib"):
        continue

    match = re.search(r'iris_model_(\d{4}-\d{2}-\d{2})\.joblib', filename)
    if not match:
        continue

    ds = match.group(1)
    model_path = os.path.join(MODEL_DIR, filename)

    try:
        model = load(model_path)
    except Exception as e:
        print(f"[ERROR] Не вдалося завантажити {filename}: {e}")
        continue

    if not hasattr(model, "feature_importances_"):
        print(f"[SKIP] {filename}: немає feature_importances_")
        continue

    importances = pd.Series(model.feature_importances_)
    top5 = importances.sort_values(ascending=False).head(5)

    for idx, importance in top5.items():
        feature_name = X_columns[idx] if idx < len(X_columns) else f"UNKNOWN_{idx}"
        rows.append({
            "date": ds,
            "feature": feature_name,
            "importance": round(importance, 4)
        })

# 6. Формуємо фінальний датафрейм
df = pd.DataFrame(rows)
print(df)

# (опціонально) Зберігаємо
#df.to_csv("iris_top5_features_with_names.csv", index=False)



