# Задание 1. Phone Address API

Это RESTful API сервис для управления данными о номерах телефонов и их связанных адресах с использованием FastAPI, Redis и асинхронных функций. API позволяет записывать, обновлять и получать данные об адресах по номерам телефонов.

## Стек технологий

- Python 3.10+
- FastAPI
- Redis (асинхронный клиент)
- Pydantic
- PostgreSQL
- Docker & Docker Compose
- pytest для тестирования

## Установка и запуск

### Клонирование репозитория

```bash
git clone git@github.com:poligrafo/phone-address-api.git
cd phone-address-api
```

## Настройка переменных окружения

Проект использует файл `.env` для хранения конфигураций. В репозитории уже есть пример файла с переменными окружения:

```bash
cp .envexample .env
```
Откройте файл .env и при необходимости настройте переменные окружения, такие как хост и порт Redis:
```
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_PORT=5433

DEBUG=True/False
```

## Запуск с использованием Docker

Соберите и запустите контейнеры:

```bash
docker-compose up --build
```
# Задание 2.Сравнение методов обновления данных в таблице PostgreSQL

## Описание задачи

Имеются две таблицы в базе данных PostgreSQL:

1. `short_names` — содержит имена файлов без расширения и статус файла.
2. `full_names` — содержит имена файлов с расширением и статус, который необходимо обновить.

Цель: обновить статусы в таблице `full_names`, используя данные из таблицы `short_names`. 

## Генерация данных

- Таблица `short_names` содержит 700,000 записей.
- Таблица `full_names` содержит 500,000 записей, каждый файл имеет различные расширения (например, `.mp3`, `.wav`).

## Методы обновления статусов

Реализованы 2 метода:

1. **JOIN Method** — использует `JOIN` с разделением имени файла через `split_part`.
2. **CTE Method** — использует CTE и регулярные выражения `regexp_replace` для разделения имени.

Скрипт из файла [migrate_data.py](scripts/migrate_data.py):
   ```python
   import time
   import psycopg2

   def update_status_join_method(conn):
    """Option 1: Update via JOIN"""
    print("Starting JOIN method update...")
    start_time = time.time()
    query = """
    UPDATE full_names
    SET status = short_names.status
    FROM short_names
    WHERE short_names.name = split_part(full_names.name, '.', 1);
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
    conn.commit()
    end_time = time.time()
    print(f"JOIN Method Update Time: {end_time - start_time:.2f} seconds")


   def update_status_cte_method(conn):
       """Option 2: Update via CTE and regexp_replace"""
       print("Starting CTE method update...")
       start_time = time.time()
       query = """
       WITH stripped_full_names AS (
         SELECT name, regexp_replace(name, '\\..*$', '') AS stripped_name
         FROM full_names
       )
       UPDATE full_names
       SET status = short_names.status
       FROM short_names, stripped_full_names
       WHERE stripped_full_names.stripped_name = short_names.name
       AND full_names.name = stripped_full_names.name;
       """
       with conn.cursor() as cursor:
           cursor.execute(query)
       conn.commit()
       end_time = time.time()
       print(f"CTE Method Update Time: {end_time - start_time:.2f} seconds")


   def compare_methods():
       """Comparison of all options"""
       print("Starting comparison of methods...")
       conn = psycopg2.connect(
           dbname="postgres",
           user="postgres",
           password="password",
           host="postgres_db",
           port=5432
       )

    try:
        print("Running JOIN method:")
        update_status_join_method(conn)

        print("Running CTE method:")
        update_status_cte_method(conn)

        print("Data migration completed successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        conn.close()


   if __name__ == "__main__":
       compare_methods()
   ```

## Запуск в Docker

1. Сначала создайте и наполните таблицы с данными:
   ```bash
   docker-compose exec web python scripts/generate_data.py
   ```

2. Затем выполните скрипт для сравнения методов:
   ```bash
   docker-compose exec web python scripts/migrate_data.py
   ```
   
3. В выводе будет отображено время выполнения каждого метода.
Результаты
Каждый метод измеряет время выполнения и выводит результат в формате:
   ```bash
   Running JOIN method:
   JOIN Method Update Time: X seconds
   Running CTE method:
   CTE Method Update Time: X seconds
   ```