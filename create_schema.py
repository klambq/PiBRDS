import os

from dotenv import load_dotenv

from connect_db import connect_to_db


load_dotenv()

DATABASE_NAME = os.getenv("DATABASE_NAME")

if not DATABASE_NAME:
    raise ValueError("Brakuje DATABASE_NAME w pliku .env")


def create_table(connection):
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pse_actual (
                id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
                business_date DATE NOT NULL,
                dtime DATETIME NOT NULL,
                dtime_utc DATETIME NOT NULL,
                period VARCHAR(13) NOT NULL,
                period_utc VARCHAR(13) NOT NULL,

                demand DECIMAL(10, 3) NOT NULL,
                swm_p DECIMAL(10, 3) NOT NULL,
                swm_np DECIMAL(10, 3) NOT NULL,
                jg DECIMAL(10, 3) NOT NULL,
                jgw1 DECIMAL(10, 3) NOT NULL,
                jgm1 DECIMAL(10, 3) NOT NULL,
                jnwrb DECIMAL(10, 3) NOT NULL,
                jgm DECIMAL(10, 3) NOT NULL,
                wi DECIMAL(10, 3) NOT NULL,
                pv DECIMAL(10, 3) NOT NULL,

                PRIMARY KEY (id),
                UNIQUE KEY uq_pse_actual_dtime_utc (dtime_utc)
            );
        """)


def main():
    connection = connect_to_db()

    try:
        connection.select_db(DATABASE_NAME)
        create_table(connection)
        connection.commit()
        print(f"Tabela  została utworzona w bazie.")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
