from pathlib import Path

import pandas as pd

from connect_db import get_engine
from helper import import_csv, utc_datetime
from models import pse_actual


CSV_PATH = Path(__file__).parent / "data" / "pse_actual.csv"


def prepare(data):
    data["business_date"] = pd.to_datetime(data["business_date"]).dt.date
    data["dtime_utc"] = utc_datetime(data["dtime_utc"])
    return data


def main():
    engine = get_engine()

    try:
        processed = import_csv(engine, CSV_PATH, pse_actual, prepare)
        print(f"Zaimportowano {processed} rekordow do `pse_actual`.")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
