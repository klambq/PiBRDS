from sqlalchemy import inspect, text

from connect_db import get_engine
from models import pse_actual


def migrate_dst_columns(engine):
    columns = {
        column["name"]: column["type"]
        for column in inspect(engine).get_columns(pse_actual.name)
    }

    dtime_length = getattr(columns["dtime"], "length", None)
    period_length = getattr(columns["period"], "length", None)

    if dtime_length == 20 and period_length == 15:
        return

    with engine.begin() as connection:
        connection.execute(text("""
            ALTER TABLE pse_actual
                MODIFY COLUMN dtime VARCHAR(20) NOT NULL,
                MODIFY COLUMN period VARCHAR(15) NOT NULL
        """))


def main():
    engine = get_engine()

    try:
        pse_actual.create(engine, checkfirst=True)
        migrate_dst_columns(engine)
        print("Tabela `pse_actual` jest gotowa.")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
