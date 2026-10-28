import logging

from sqlalchemy import func, select

from connect_db import get_engine
from helper import import_csv
from import_actual import CSV_PATH as ACTUAL_CSV
from import_actual import prepare as prepare_actual
from import_forecast_pkd import CSV_PATH as FORECAST_CSV
from import_forecast_pkd import prepare as prepare_forecast
from models import metadata, pse_actual, pse_forecast_pkd


logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def load_table(engine, table, csv_path, prepare):
    logger.info("[%s] Importuje dane z .csv", table.name)
    processed = import_csv(engine, csv_path, table, prepare)
    logger.info("[%s] Przetworzono: %s", table.name, processed)


def main():
    engine = get_engine()

    try:
        logger.info("Usuwam stare tabele")
        metadata.drop_all(engine)

        logger.info("Tworze nowe tabele")
        metadata.create_all(engine)

        load_table(
            engine,
            pse_actual,
            ACTUAL_CSV,
            prepare_actual,
        )
        load_table(
            engine,
            pse_forecast_pkd,
            FORECAST_CSV,
            prepare_forecast,
        )

        logger.info("Stan tabel po imporcie:")
        with engine.connect() as connection:
            for table in (pse_actual, pse_forecast_pkd):
                count = connection.scalar(select(func.count()).select_from(table))
                logger.info(
                    "[%s] SELECT COUNT(*): %s",
                    table.name,
                    count,
                )
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
