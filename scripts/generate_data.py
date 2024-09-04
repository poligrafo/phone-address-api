import os
import random
import psycopg2
from psycopg2 import sql
import psycopg2.extras

SHORT_NAMES_COUNT = 700000
FULL_NAMES_COUNT = 500000
BATCH_SIZE = 10000

def batch_insert(cursor, table, columns, data):
    """A function for executing butches"""
    query = sql.SQL("INSERT INTO {} ({}) VALUES %s").format(
        sql.Identifier(table),
        sql.SQL(', ').join(map(sql.Identifier, columns))
    )
    psycopg2.extras.execute_values(cursor, query, data, page_size=BATCH_SIZE)

def generate_data():
    print("Data generation started...")

    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "postgres"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "password"),
        host=os.getenv("POSTGRES_HOST", "db"),
        port=os.getenv("POSTGRES_PORT", 5433)
    )

    try:
        with conn.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS short_names, full_names;")
            cursor.execute("""
            CREATE TABLE short_names (
                name VARCHAR(255) PRIMARY KEY,
                status INT
            );
            CREATE TABLE full_names (
                name VARCHAR(255) PRIMARY KEY,
                status INT
            );
            """)

            # Generating data for short_names
            short_names_data = [(f'nazvanie{i}', random.randint(0, 1)) for i in range(1, SHORT_NAMES_COUNT + 1)]
            for i in range(0, len(short_names_data), BATCH_SIZE):
                batch_insert(cursor, 'short_names', ['name', 'status'], short_names_data[i:i + BATCH_SIZE])

            # Generating data for  full_names
            extensions = ['mp3', 'wav', 'flac', 'aac', 'ogg', 'm4a', 'wma']
            full_names_data = [(f'{name}.{random.choice(extensions)}',) for name in [f'nazvanie{i}' for i in range(1, FULL_NAMES_COUNT + 1)]]
            for i in range(0, len(full_names_data), BATCH_SIZE):
                batch_insert(cursor, 'full_names', ['name'], full_names_data[i:i + BATCH_SIZE])

            conn.commit()

            cursor.execute("SELECT COUNT(*) FROM short_names;")
            short_names_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM full_names;")
            full_names_count = cursor.fetchone()[0]

            print(f"Data generation completed successfully!")
            print(f"Short names table contains: {short_names_count} records")
            print(f"Full names table contains: {full_names_count} records")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    generate_data()
