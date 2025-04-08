import os
import requests  # Імпортуємо бібліотеку для виконання HTTP-запитів (POST, GET тощо)


def main() -> None:
    """
    Надсилає POST-запит до Flask-сервера другої джоби (convert_to_avro),
    передаючи шляхи до сирих JSON-файлів та директорії для збереження Avro-файлів.
    """

    # Отримуємо абсолютний шлях до кореня проєкту
    # __file__ — це шлях до поточного файлу (test_avro_job.py)
    project_root: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    # Формуємо абсолютні шляхи до директорій:
    # - raw_dir: де лежать JSON-файли (вхідні)
    # - stg_dir: куди зберігати Avro-файли (вихідні)
    raw_dir: str = os.path.join(project_root, 'lec02', 'raw', 'sales')
    stg_dir: str = os.path.join(project_root, 'lec02', 'stg', 'sales')

    # Встановлюємо адресу, на якій працює Flask-сервер для job_2 (порт 8082)
    url: str = "http://127.0.0.1:8082/run-job"

    # Формуємо словник із параметрами, які будуть відправлені на сервер
    data: dict[str, str] = {
        "raw_dir": raw_dir,
        "stg_dir": stg_dir
    }

    # Надсилаємо POST-запит до Flask-сервера
    response: requests.Response = requests.post(url, json=data)

    # Виводимо HTTP-статус відповіді (200 — успіх, 400/500 — помилка)
    print("Відповідь від сервера:")
    print(response.status_code)

    # Виводимо повідомлення від сервера у форматі JSON
    print(response.json())


# Запуск функції main тільки при прямому виконанні скрипта (не при імпорті)
if __name__ == "__main__":
    main()
