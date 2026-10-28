from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

from sqlalchemy.dialects.mysql import insert

from connect_db import get_engine
from helper import import_csv_in_batches, parse_utc_datetime
from models import pse_forecast_pkd


CSV_PATH = Path(__file__).resolve().parent / "data" / "pse_forecast_pkd.csv"


def parse_row(row):
    return {
        "dtime": row["dtime"],
        "gen_fv": Decimal(row["gen_fv"]),
        "gen_wi": Decimal(row["gen_wi"]),
        "period": row["period"],
        "dtime_utc": parse_utc_datetime(row["dtime_utc"]),
        "period_utc": row["period_utc"],
        "business_date": date.fromisoformat(row["business_date"]),
        "publication_ts": datetime.fromisoformat(row["publication_ts"]),
        "publication_ts_utc": parse_utc_datetime(
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


def main():
    engine = get_engine()

    try:
        processed = import_csv_in_batches(
            engine=engine,
            csv_path=CSV_PATH,
            parse_row=parse_row,
            statement=get_upsert_statement(),
        )
        print(f"Import zakonczony. Przetworzono {processed} rekordow.")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
