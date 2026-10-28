import pandas as pd
from sqlalchemy import select

from connect_db import get_engine
from models import pse_actual, pse_forecast_pkd


TABLE_NAME = "pse_actual_vs_forecast"
BATCH_SIZE = 5000


def main():
    engine = get_engine()

    try:
        query = select(
            pse_actual.c.dtime_utc,
            pse_actual.c.business_date,
            pse_actual.c.pv.label("actual_PV"),
            pse_actual.c.wi.label("actual_FW"),
            pse_forecast_pkd.c.publication_ts_utc,
            pse_forecast_pkd.c.gen_fv.label("forecast_PV"),
            pse_forecast_pkd.c.gen_wi.label("forecast_FW"),
        ).join(
            pse_forecast_pkd,
            pse_actual.c.dtime_utc == pse_forecast_pkd.c.dtime_utc,
        )

        processed = 0

        for data in pd.read_sql(query, engine, chunksize=BATCH_SIZE):
            numeric_columns = [
                "actual_PV",
                "actual_FW",
                "forecast_PV",
                "forecast_FW",
            ]
            data[numeric_columns] = data[numeric_columns].astype(float)
            data["pv_error"] = data["forecast_PV"] - data["actual_PV"]
            data["wi_error"] = data["forecast_FW"] - data["actual_FW"]

            data.to_sql(
                TABLE_NAME,
                engine,
                if_exists="replace" if processed == 0 else "append",
                index=False,
                method="multi",
            )
            processed += len(data)
            print(f"[{TABLE_NAME}] Przetworzono: {processed}")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
