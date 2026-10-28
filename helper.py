import pandas as pd
from sqlalchemy.dialects.mysql import insert


def utc_datetime(values):
    return pd.to_datetime(values, utc=True).dt.tz_localize(None)


def import_csv(
    engine,
    csv_path,
    table,
    prepare,
    chunksize=1000,
    progress_every=10000,
):
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

            if processed % progress_every == 0:
                print(
                    f"[{table.name}] Przetworzono: {processed}",
                    flush=True,
                )

    return processed
