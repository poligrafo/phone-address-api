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
