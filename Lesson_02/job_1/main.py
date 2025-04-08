from flask import Flask, request, jsonify
from job_1.fetch_sales import fetch_sales_data
import os

# Ініціалізуємо Flask-додаток
app = Flask(__name__)


@app.route("/run-job", methods=["POST"])
def run_job() -> tuple:
    """
    Обробляє POST-запит для запуску джоби завантаження даних продажів.
    Очікує JSON-тіло з параметром 'raw_dir'.
    Повертає статус виконання та повідомлення у форматі JSON.
    """
    # Отримуємо JSON-тіло запиту
    data = request.get_json()

    # Перевіряємо наявність параметра 'raw_dir'
    raw_dir = data.get("raw_dir") if isinstance(data, dict) else None
    if not raw_dir:
        return jsonify({"error": "Missing 'raw_dir' in request"}), 400

    try:
        # Запускаємо основну функцію для завантаження даних
        fetch_sales_data(raw_dir)

        # Повертаємо успішну відповідь
        return jsonify({
            "status": "success",
            "message": f"Data saved to {raw_dir}"
        }), 200

    except Exception as e:
        # Обробляємо будь-які винятки під час виконання
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    # Запускаємо локальний Flask-сервер на порту 8081
    app.run(port=8081)
