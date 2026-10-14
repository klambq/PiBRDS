import pymysql
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)


def connect_to_db():
    load_dotenv()
    host = os.getenv("host")
    port = int(os.getenv("port"))
    user = os.getenv("user")
    password = os.getenv("password")
    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
    )
    logger.info("Connected to the database")
    return connection


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    connection = None
    try:
        connection = connect_to_db()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 2+2;")
            logger.info(f"test: {cursor.fetchone()}")
    finally:
        if connection is not None:
            connection.close()
            logger.info("connection closed")
