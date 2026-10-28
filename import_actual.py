from datetime import date
from decimal import Decimal
from pathlib import Path

from sqlalchemy.dialects.mysql import insert

from connect_db import get_engine
from helper import import_csv_in_batches, parse_utc_datetime
from models import pse_actual


CSV_PATH = Path(__file__).resolve().parent / "data" / "pse_actual.csv"


def parse_row(row):
    return {
        "business_date": date.fromisoformat(row["business_date"]),
        "dtime": row["dtime"],
        "dtime_utc": parse_utc_datetime(row["dtime_utc"]),
        "period": row["period"],
        "period_utc": row["period_utc"],
        "demand": Decimal(row["demand"]),
        "swm_p": Decimal(row["swm_p"]),
        "swm_np": Decimal(row["swm_np"]),
        "jg": Decimal(row["jg"]),
        "jgw1": Decimal(row["jgw1"]),
        "jgm1": Decimal(row["jgm1"]),
        "jnwrb": Decimal(row["jnwrb"]),
        "jgm": Decimal(row["jgm"]),
        "wi": Decimal(row["wi"]),
        "pv": Decimal(row["pv"]),
    }


def get_upsert_statement():
    statement = insert(pse_actual)

    return statement.on_duplicate_key_update(
        business_date=statement.inserted.business_date,
        dtime=statement.inserted.dtime,
        period=statement.inserted.period,
        period_utc=statement.inserted.period_utc,
        demand=statement.inserted.demand,
        swm_p=statement.inserted.swm_p,
        swm_np=statement.inserted.swm_np,
        jg=statement.inserted.jg,
        jgw1=statement.inserted.jgw1,
        jgm1=statement.inserted.jgm1,
        jnwrb=statement.inserted.jnwrb,
        jgm=statement.inserted.jgm,
        wi=statement.inserted.wi,
        pv=statement.inserted.pv,
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
