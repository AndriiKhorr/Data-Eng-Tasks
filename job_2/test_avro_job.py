import requests  # Імпортуємо бібліотеку для виконання HTTP-запитів


# Встановлюємо URL, за яким запущений Flask-сервер другої джоби
url: str = "http://127.0.0.1:8082/run-job"

# Формуємо тіло POST-запиту з параметрами:
# raw_dir — шлях до директорії, де зберігаються JSON-файли
# stg_dir — шлях до директорії, куди збережуться Avro-файли
data: dict[str, str] = {
    "raw_dir": "raw/sales",
    "stg_dir": "stg/sales"
}

# Виконуємо POST-запит до Flask-сервера
response: requests.Response = requests.post(url, json=data)

# Виводимо статус-код відповіді (200 — успіх, 500 — помилка сервера і т.д.)
print("Відповідь від сервера:")
print(response.status_code)

# Виводимо тіло відповіді у форматі JSON
print(response.json())
