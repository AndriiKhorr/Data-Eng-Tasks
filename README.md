# Домашнє завдання: Data Engineering — Lesson 02

## Структура проєкту
```
Lesson_02/
|
├── job_1/                         # Папка для першої джоби
│   ├── fetch_sales.py             # Отримання даних з API
│   ├── main.py                    # Flask-сервер для job_1
│   └── test_request.py           # Тестовий запит до Flask-сервера
│
├── job_2/                         # Папка для другої джоби
│   ├── convert_to_avro.py        # Конвертація JSON у Avro
│   ├── main_avro.py              # Flask-сервер для job_2
│   ├── organize_raw_files.py     # Структурування raw-даних
│   └── test_avro_job.py         # Тестовий запит до Flask job_2
│
├── raw/                          # Сирі дані у JSON
│   └── sales/                    # sales_{date}.json
│
├── stg/                          # Стандартнізовані Avro-дані
│   └── sales/                    # Поділ по датах
│
├── .env                          # Файл зі секретами (не пушити)
├── .gitignore                    # Файл ігнору для Git
├── requirements.txt             # Список залежностей
└── README.md                    # Цей документ
```

---

## Джоба 1: Отримання JSON-даних

- **Flask-сервер:** `job_1/main.py`
- **Основна логіка:** `job_1/fetch_sales.py`
- **Результат:** Зберігає всі сторінки з API у файли `sales_{date}.json`
- **Шлях:** `raw/sales/sales_YYYY-MM-DD.json`
- **Ідемпотентність:** Перед запуском очищує `raw/sales`

### Як запустити job_1:
```bash
cd Lesson_02
python -m job_1.main
```
### Як протестувати job_1:
```bash
python job_1/test_request.py
```

---

## Джоба 2: Конвертація JSON у Avro

- **Flask-сервер:** `job_2/main_avro.py`
- **Основна логіка:** `job_2/convert_to_avro.py`
- **Підготовка:** `job_2/organize_raw_files.py` структурує `raw/sales` по підпапках дат
- **Результат:** Зберігає `sales_{date}.avro` у `stg/sales/YYYY-MM-DD/`
- **Ідемпотентність:** Перед запуском очищує `stg/sales`

### Як запустити job_2:
```bash
cd Lesson_02
python -m job_2.main_avro
```
### Як протестувати job_2:
```bash
python job_2/test_avro_job.py
```

---

## Залежності
```bash
pip install -r requirements.txt
```

---

## Секрети
- У `.env` знаходиться ключ `AUTH_TOKEN=...`
- У запитах **не** використовується `Bearer`, лише значення

---

## Формат результуючої структури
```
raw/sales/2022-08-09/sales_2022-08-09.json
stg/sales/2022-08-09/sales_2022-08-09.avro
```

---

## Автор
Завдання виконав Андрій \U0001f4bb

