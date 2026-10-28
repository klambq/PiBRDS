from connect_db import get_engine
from models import pse_forecast_pkd


def main():
    engine = get_engine()

    try:
        pse_forecast_pkd.create(engine, checkfirst=True)
        print("Tabela `pse_forecast_pkd` jest gotowa.")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
