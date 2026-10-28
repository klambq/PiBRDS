import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text


load_dotenv()


def get_engine():
    required_variables = ("host", "user", "password", "DATABASE_NAME")
    missing_variables = [
        variable
        for variable in required_variables
        if not os.getenv(variable)
    ]

    if missing_variables:
        missing = ", ".join(missing_variables)
        raise ValueError(f"Brakuje zmiennych w pliku .env: {missing}")

    url = URL.create(
        drivername="mysql+pymysql",
        username=os.getenv("user"),
        password=os.getenv("password"),
        host=os.getenv("host"),
        port=int(os.getenv("port", "3306")),
        database=os.getenv("DATABASE_NAME"),
    )

    return create_engine(url, pool_pre_ping=True)


def main():
    engine = get_engine()

    with engine.connect() as connection:
        result = connection.scalar(text("SELECT 2 + 2"))
        print(f"Test polaczenia: 2 + 2 = {result}")

    engine.dispose()


if __name__ == "__main__":
    main()
