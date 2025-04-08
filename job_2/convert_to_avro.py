import os
import json
from typing import List, Dict
from fastavro import writer, parse_schema


def convert_json_to_avro(raw_dir: str, stg_dir: str) -> None:
    """
    Конвертує всі JSON-файли в raw_dir у формат Avro
    і зберігає результати у відповідні підпапки в stg_dir.
    """

    print("Починаємо конвертацію JSON → Avro")

    # Перевіряємо, чи існує директорія з вхідними файлами
    if not os.path.exists(raw_dir):
        raise Exception(f"Директорія {raw_dir} не існує")

    # Ідемпотентність: очищення вмісту вихідної директорії stg_dir
    for root, dirs, files in os.walk(stg_dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))  # Видаляємо всі файли
        for name in dirs:
            os.rmdir(os.path.join(root, name))  # Видаляємо всі підкаталоги

    os.makedirs(stg_dir, exist_ok=True)  # Переконуємось, що stg_dir існує

    # Визначаємо схему Avro — вона має відповідати структурі даних
    schema: Dict = {
        "doc": "Sales records",
        "name": "Sale",
        "namespace": "sales",
        "type": "record",
        "fields": [
            {"name": "client", "type": "string"},
            {"name": "purchase_date", "type": "string"},
            {"name": "product", "type": "string"},
            {"name": "price", "type": "int"},
        ],
    }

    # Проходимося по кожній підпапці у raw_dir (наприклад: raw/sales/2022-08-09)
    for date_folder_name in os.listdir(raw_dir):
        date_folder_path = os.path.join(raw_dir, date_folder_name)

        # Пропускаємо, якщо це не папка
        if not os.path.isdir(date_folder_path):
            continue

        combined_data: List[Dict] = []  # Масив для об'єднання всіх JSON-даних по даті

        # Читаємо всі JSON-файли в цій підпапці
        for file_name in os.listdir(date_folder_path):
            if file_name.endswith(".json"):
                file_path = os.path.join(date_folder_path, file_name)
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                    # Додаємо дані у масив, якщо це список
                    if isinstance(data, list):
                        combined_data.extend(data)

        # Якщо дані відсутні — пропускаємо створення файлу
        if not combined_data:
            continue

        # Створюємо вихідну папку для цієї дати, якщо ще не існує
        output_folder = os.path.join(stg_dir, date_folder_name)
        os.makedirs(output_folder, exist_ok=True)

        # Формуємо повний шлях до Avro-файлу
        avro_path = os.path.join(output_folder, f"sales_{date_folder_name}.avro")

        # Записуємо дані у Avro-файл
        with open(avro_path, "wb") as out:
            writer(out, parse_schema(schema), combined_data)

        print(f"Збережено Avro файл: {avro_path}")

    print("Усі дані конвертовано!")

    

