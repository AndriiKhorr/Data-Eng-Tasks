import os
import requests
import json
import shutil
from datetime import datetime, timedelta
from typing import List, Dict, Any
from dotenv import load_dotenv

# Завантажуємо змінні середовища з файлу .env
load_dotenv()

# Отримуємо значення токена з середовища
AUTH_TOKEN: str | None = os.getenv("AUTH_TOKEN")

# Базова URL-адреса API
BASE_URL: str = "https://fake-api-vycpfa6oca-uc.a.run.app/sales"

# Заголовки для HTTP-запитів (без Bearer)
HEADERS: Dict[str, str] = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": AUTH_TOKEN or ""
}


def fetch_sales_data(raw_dir: str) -> None:
    """
    Функція отримує дані з API за кожну дату з 2022-01-01 до вчорашнього дня,
    і зберігає їх у JSON-файли по одному файлу на день.

    :param raw_dir: Абсолютний або відносний шлях до директорії для збереження файлів
    """

    print("Старт запиту до API")
    print(f"AUTH_TOKEN = {AUTH_TOKEN}")

    # Перевіряємо, чи токен заданий
    if not AUTH_TOKEN:
        raise Exception("AUTH_TOKEN не знайдено. Перевір .env")

    # Ідемпотентність: якщо директорія існує — видаляємо її повністю
    if os.path.exists(raw_dir):
        shutil.rmtree(raw_dir)

    # Створюємо нову порожню директорію
    os.makedirs(raw_dir, exist_ok=True)

    # Початкова дата — 1 січня 2022 року
    start_date: datetime = datetime(2022, 1, 1)

    # Кінцева дата — вчорашній день
    end_date: datetime = datetime.today() - timedelta(days=1)

    # Ітерація по всім датам
    current_date: datetime = start_date
    while current_date <= end_date:
        date_str: str = current_date.strftime("%Y-%m-%d")
        print(f"Обробка дати {date_str}")

        page: int = 1
        combined_items: List[Dict[str, Any]] = []

        while True:
            print(f"  Завантаження сторінки {page} для {date_str}")

            # Параметри запиту: дата та номер сторінки
            params: Dict[str, Any] = {"date": date_str, "page": page}

            response = requests.get(BASE_URL, headers=HEADERS, params=params)

            # Якщо даних немає — перериваємо обробку цієї дати
            if response.status_code == 404:
                print(f"  Немає даних за {date_str}")
                break

            # Якщо інша помилка — піднімаємо виняток
            if response.status_code != 200:
                raise Exception(f"Помилка при запиті до API: {response.status_code}\n{response.text}")

            items: List[Dict[str, Any]] = response.json()

            if not items:
                print(f"  Порожня сторінка {page} для {date_str}")
                break

            # Додаємо знайдені записи до спільного списку
            combined_items.extend(items)
            page += 1

        # Якщо знайдено записи — зберігаємо їх у файл
        if combined_items:
            filename: str = os.path.join(raw_dir, f"sales_{date_str}.json")
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(combined_items, f, indent=2, ensure_ascii=False)

            print(f"Збережено файл: {filename}")

        # Переходимо до наступної дати
        current_date += timedelta(days=1)

    print("Завершено: усі доступні дані завантажено")
