import time

import pandas as pd
from sqlalchemy import select, text

from connect_db import get_engine
from models import pse_actual


engine = get_engine()

start = time.time()
data = pd.read_sql(select(pse_actual), engine)
dataframe_count = len(data)
dataframe_time = time.time() - start

start = time.time()
with engine.connect() as connection:
    database_count = connection.scalar(
        text("SELECT COUNT(*) FROM pse_actual")
    )
database_time = time.time() - start

engine.dispose()

print(f"DataFrame: {dataframe_count} rekordow, {dataframe_time:.4f} s")
print(f"Database:  {database_count} rekordow, {database_time:.4f} s")
