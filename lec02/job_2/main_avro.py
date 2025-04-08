from flask import Flask, request, jsonify
from lec02.job_2.convert_to_avro import convert_json_to_avro

# Ініціалізація Flask-додатку
app = Flask(__name__)


@app.route("/run-job", methods=["POST"])
def run_avro_job() -> tuple:
    """
    Обробник POST-запиту для запуску джоби конвертації JSON → Avro.

    Очікує JSON у форматі:
    {
        "raw_dir": "шлях до директорії з JSON-файлами",
        "stg_dir": "шлях до директорії для збереження Avro-файлів"
    }

    Повертає JSON-відповідь з результатом виконання.
    """
    try:
        # Отримання вхідних параметрів з тіла запиту
        raw_dir = request.json.get("raw_dir")
        stg_dir = request.json.get("stg_dir")

        # Перевірка, чи обидва параметри присутні
        if not raw_dir or not stg_dir:
            return (
                jsonify({
                    "status": "error",
                    "message": "Потрібно вказати 'raw_dir' та 'stg_dir'"
                }),
                400
            )

        # Виклик функції конвертації
        convert_json_to_avro(raw_dir, stg_dir)

        # Повернення позитивної відповіді
        return jsonify({
            "status": "success",
            "message": f"Дані збережено в {stg_dir}"
        })

    except Exception as e:
        # Обробка помилок
        print(f"Помилка під час виконання джоби: {e}")
        return (
            jsonify({
                "status": "error",
                "message": str(e)
            }),
            500
        )


if __name__ == "__main__":
    # Запуск Flask-сервера на порту 8082
    print("Запускаємо Flask-сервер для Avro-джоби...")
    app.run(port=8082)
