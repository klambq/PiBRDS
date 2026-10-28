import pandas as pd
from sqlalchemy import select

from connect_db import get_engine
from models import pse_actual, pse_forecast_pkd


TABLE_NAME = "pse_actual_vs_forecast"


def main():
    engine = get_engine()

    try:
        actual = pd.read_sql(
            select(
                pse_actual.c.dtime_utc,
                pse_actual.c.business_date,
                pse_actual.c.pv.label("actual_pv"),
                pse_actual.c.wi.label("actual_wi"),
            ),
            engine,
        )
        forecast = pd.read_sql(
            select(
                pse_forecast_pkd.c.dtime_utc,
                pse_forecast_pkd.c.publication_ts_utc,
                pse_forecast_pkd.c.gen_fv.label("forecast_pv"),
                pse_forecast_pkd.c.gen_wi.label("forecast_wi"),
            ),
            engine,
        )

        data = actual.merge(forecast, on="dtime_utc")
        numeric_columns = [
            "actual_pv",
            "actual_wi",
            "forecast_pv",
            "forecast_wi",
        ]
        data[numeric_columns] = data[numeric_columns].astype(float)
        data["pv_error"] = data["forecast_pv"] - data["actual_pv"]
        data["wi_error"] = data["forecast_wi"] - data["actual_wi"]

        data.to_sql(
            TABLE_NAME,
            engine,
            if_exists="replace",
            index=False,
            chunksize=1000,
            method="multi",
        )
        print(f"[{TABLE_NAME}] Zapisano: {len(data)} rekordow")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
