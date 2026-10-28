from connect_db import get_engine
from helper import import_csv
from import_actual import CSV_PATH as ACTUAL_CSV
from import_actual import prepare as prepare_actual
from import_forecast_pkd import CSV_PATH as FORECAST_CSV
from import_forecast_pkd import prepare as prepare_forecast
from models import metadata, pse_actual, pse_forecast_pkd


def main():
    engine = get_engine()

    try:
        metadata.drop_all(engine)
        metadata.create_all(engine)

        actual_count = import_csv(
            engine,
            ACTUAL_CSV,
            pse_actual,
            prepare_actual,
        )
        forecast_count = import_csv(
            engine,
            FORECAST_CSV,
            pse_forecast_pkd,
            prepare_forecast,
        )

        print(f"pse_actual: {actual_count} rekordow")
        print(f"pse_forecast_pkd: {forecast_count} rekordow")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
