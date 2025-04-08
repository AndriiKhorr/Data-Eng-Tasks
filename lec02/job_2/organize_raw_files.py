import os
import shutil

# Отримуємо абсолютний шлях до директорії, де зберігаються сирі файли (JSON)
# Абсолютний шлях гарантує правильну роботу незалежно від того, звідки запускається скрипт
raw_dir: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'raw', 'sales'))

# Перебираємо всі файли, що знаходяться у вказаній директорії
for filename in os.listdir(raw_dir):

    # Фільтруємо тільки ті файли, які починаються на 'sales_' і закінчуються на '.json'
    if filename.startswith("sales_") and filename.endswith(".json"):

        # Отримуємо частину імені файлу з датою (у форматі YYYY-MM-DD)
        # Наприклад: 'sales_2022-08-09.json' → '2022-08-09'
        date_part: str = filename.split("_")[1].replace(".json", "")

        # Створюємо шлях до підпапки з назвою дати (наприклад, raw/sales/2022-08-09)
        date_folder: str = os.path.join(raw_dir, date_part)

        # Якщо така папка ще не існує — створюємо її
        os.makedirs(date_folder, exist_ok=True)

        # Формуємо повний шлях до поточного (вихідного) файлу
        src_path: str = os.path.join(raw_dir, filename)

        # Формуємо шлях, куди потрібно перемістити файл
        dst_path: str = os.path.join(date_folder, filename)

        # Переміщуємо файл у відповідну папку за датою
        shutil.move(src_path, dst_path)

        # Виводимо повідомлення про успішне переміщення файлу
        print(f"✅ Переміщено {filename} у {date_folder}/")
