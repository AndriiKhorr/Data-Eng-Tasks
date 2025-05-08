import os
import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

def process_iris_data(ds: str):
    """
    Завантажує дані з бази, фільтрує по даті, тренує модель і зберігає її.
    """
    # Зчитування змінних середовища або використання дефолтних значень
    db_user = os.getenv("POSTGRES_ANALYTICS_DATAUSER", "analytics_admin")
    db_password = os.getenv("POSTGRES_ANALYTICS_DATAPASSWORD", "admin123")
    db_host = os.getenv("POSTGRES_ANALYTICS_HOST", "analytics_db")  
    db_port = "5432"
    db_name = os.getenv("POSTGRES_ANALYTICS_DB", "analytics")

    # Підключення до бази
    engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

    # SQL-запит
    query = f"""
        SELECT * FROM homework.iris_processed
        WHERE source_date = '{ds}'
    """
    df = pd.read_sql(query, con=engine)

    if df.empty:
        raise ValueError(f"Немає даних для дати {ds}")

    if "species" not in df.columns:
        raise ValueError("Колонка 'species' не знайдена у даних.")

    # Train/test
    X = df.drop(columns=["species", "source_date"])
    y = df["species"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    accuracy = clf.score(X_test, y_test)
    print(f"[INFO] Модель натренована. Accuracy = {accuracy:.4f}")

    # Сховище для моделей
    output_dir = "/opt/airflow/models"
    os.makedirs(output_dir, exist_ok=True)
    model_path = os.path.join(output_dir, f"iris_model_{ds}.joblib")
    joblib.dump(clf, model_path)

    print(f"[INFO] Модель успішно збережено у: {model_path}")
