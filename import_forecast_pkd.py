import csv
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

from sqlalchemy.dialects.mysql import insert

from connect_db import get_engine
from models import pse_forecast_pkd


CSV_PATH = Path(__file__).resolve().parent / "data" / "pse_forecast_pkd.csv"
BATCH_SIZE = 1000


def parse_row(row):
    return {
        "dtime": row["dtime"],
        "gen_fv": Decimal(row["gen_fv"]),
        "gen_wi": Decimal(row["gen_wi"]),
        "period": row["period"],
        "dtime_utc": datetime.fromisoformat(row["dtime_utc"]),
        "period_utc": row["period_utc"],
        "business_date": date.fromisoformat(row["business_date"]),
        "publication_ts": datetime.fromisoformat(row["publication_ts"]),
        "publication_ts_utc": datetime.fromisoformat(
            row["publication_ts_utc"]
        ),
    }


def get_upsert_statement():
    statement = insert(pse_forecast_pkd)

    return statement.on_duplicate_key_update(
        dtime=statement.inserted.dtime,
        gen_fv=statement.inserted.gen_fv,
        gen_wi=statement.inserted.gen_wi,
        period=statement.inserted.period,
        period_utc=statement.inserted.period_utc,
        business_date=statement.inserted.business_date,
        publication_ts=statement.inserted.publication_ts,
    )


def import_csv(engine):
    if not CSV_PATH.is_file():
        raise FileNotFoundError(f"Nie znaleziono pliku: {CSV_PATH}")

    processed = 0
    batch = []
    statement = get_upsert_statement()

    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        with engine.begin() as connection:
            for row in reader:
                batch.append(parse_row(row))

                if len(batch) == BATCH_SIZE:
                    connection.execute(statement, batch)
                    processed += len(batch)
                    print(f"Przetworzono: {processed}")
                    batch.clear()

            if batch:
                connection.execute(statement, batch)
                processed += len(batch)

    return processed


def main():
    engine = get_engine()

    try:
        processed = import_csv(engine)
        print(f"Import zakonczony. Przetworzono {processed} rekordow.")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
