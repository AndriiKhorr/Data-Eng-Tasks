import os
import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

def process_iris_data(ds: str, **context):
    """
    Завантажує дані з бази, тренує модель без data leakage,
    обчислює точність і важливість фіч, повертає все через XCom.
    """

    # Параметри бази
    db_user = os.getenv("POSTGRES_ANALYTICS_DATAUSER", "analytics_admin")
    db_password = os.getenv("POSTGRES_ANALYTICS_DATAPASSWORD", "admin123")
    db_host = os.getenv("POSTGRES_ANALYTICS_HOST", "analytics_db")
    db_port = "5432"
    db_name = os.getenv("POSTGRES_ANALYTICS_DB", "analytics")

    # Підключення
    engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
    query = f"SELECT * FROM homework.iris_processed WHERE source_date = '{ds}'"
    df = pd.read_sql(query, con=engine)

    if df.empty:
        raise ValueError(f"Немає даних для дати {ds}")
    if "species" not in df.columns:
        raise ValueError("Колонка 'species' не знайдена")

    # Вилучаємо всі фічі, пов’язані з target
    forbidden_cols = [
        "species", "source_date", "species_label_encoded"
    ] + [col for col in df.columns if col.startswith("is_species__")]

    X = df.drop(columns=[col for col in forbidden_cols if col in df.columns])
    y = df["species"]

    # Train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    accuracy = clf.score(X_test, y_test)

    # Top 5 фіч
    importances = pd.Series(clf.feature_importances_, index=X.columns)
    top_features = importances.sort_values(ascending=False).head(5).to_dict()

    # Логування звітів
    print("\n=== Classification Report ===")
    print(classification_report(y_test, y_pred))
    print("\n=== Confusion Matrix ===")
    print(confusion_matrix(y_test, y_pred))

    # Збереження моделі
    output_dir = "/opt/airflow/models"
    os.makedirs(output_dir, exist_ok=True)
    model_path = os.path.join(output_dir, f"iris_model_{ds}.joblib")
    joblib.dump(clf, model_path)

    # Повернення через XCom
    context['ti'].xcom_push(key='accuracy', value=accuracy)
    context['ti'].xcom_push(key='top_features', value=top_features)

    print(f"[INFO] Модель збережена у: {model_path}")
    print(f"[INFO] Accuracy: {accuracy:.4f}")
    print(f"[INFO] Top 5 фіч:\n{top_features}")
