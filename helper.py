import pandas as pd
from sqlalchemy.dialects.mysql import insert


def import_csv(engine, csv_path, table, prepare, chunksize=1000):
    statement = insert(table)
    statement = statement.on_duplicate_key_update(
        **{
            column.name: statement.inserted[column.name]
            for column in table.columns
            if not column.primary_key
        }
    )

    processed = 0

    with engine.begin() as connection:
        for chunk in pd.read_csv(csv_path, chunksize=chunksize):
            chunk = prepare(chunk)
            connection.execute(statement, chunk.to_dict("records"))
            processed += len(chunk)

    return processed
