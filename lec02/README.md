# Домашнє завдання: Data Engineering — Lesson 02

## Структура проєкту

lec02/
│
├── job_1/                         # Папка для першої джоби
│   ├── fetch_sales.py             # Отримання даних з API
│   ├── main.py                    # Flask-сервер для job_1
│   └── test_request.py            # Тестовий запит до Flask-сервера job_1
│
├── job_2/                         # Папка для другої джоби
│   ├── convert_to_avro.py         # Конвертація JSON у Avro
│   ├── main_avro.py               # Flask-сервер для job_2
│   ├── organize_raw_files.py      # Структурування raw-даних по підпапках дат
│   └── test_avro_job.py           # Тестовий запит до Flask-сервера job_2
│
├── raw/                           # Сирі дані у JSON
│   └── sales/                     # sales_YYYY-MM-DD.json або по підпапках дат
│
├── stg/                           # Стандартизовані дані у форматі Avro
│   └── sales/                     # Поділ по датах
│
├── .env                           # Секрети (не пушити в репозиторій)
├── .gitignore                     # Ігнорування службових файлів
├── requirements.txt               # Список залежностей
└── README.md                      # Цей документ

## Джоба 1: Завантаження JSON-даних з API

- Flask-сервер: lec02/job_1/main.py
- Основна логіка: lec02/job_1/fetch_sales.py
- Результат: Зберігає всі сторінки з API у файли sales_YYYY-MM-DD.json
- Шлях: lec02/raw/sales/sales_YYYY-MM-DD.json
- Ідемпотентність: Перед запуском очищує цільову директорію, якщо вона вже існує

### Як запустити job_1:
python -m lec02.job_1.main

### Як протестувати job_1:
python -m lec02.job_1.test_request

## Джоба 2: Конвертація JSON у Avro

- Flask-сервер: lec02/job_2/main_avro.py
- Основна логіка: lec02/job_2/convert_to_avro.py
- Підготовка: lec02/job_2/organize_raw_files.py структурує файли у raw/sales/ по датах
- Результат: Зберігає sales_YYYY-MM-DD.avro у lec02/stg/sales/YYYY-MM-DD/
- Ідемпотентність: Перед запуском очищує цільову директорію

### Як запустити job_2:
python -m lec02.job_2.main_avro

### Як протестувати job_2:
python -m lec02.job_2.test_avro_job

## Залежності

Для запуску проєкту встанови залежності з requirements.txt:
pip install -r requirements.txt

## Токени

- У файлі .env зберігається токен авторизації:
AUTH_TOKEN=тут_значення_токена

- У запитах не використовується Bearer, лише саме значення токена

## Формат результуючих даних

lec02/raw/sales/2022-08-09/sales_2022-08-09.json  
lec02/stg/sales/2022-08-09/sales_2022-08-09.avro

## Автор

Завдання виконав Андрій
