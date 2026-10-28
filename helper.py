import csv
from datetime import datetime, timezone


def parse_utc_datetime(value):
    parsed = datetime.fromisoformat(value)

    if parsed.tzinfo is None:
        return parsed

    return parsed.astimezone(timezone.utc).replace(tzinfo=None)


def import_csv_in_batches(
    engine,
    csv_path,
    parse_row,
    statement,
    batch_size=1000,
):
    if not csv_path.is_file():
        raise FileNotFoundError(f"Nie znaleziono pliku: {csv_path}")

    processed = 0
    batch = []

    with csv_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        with engine.begin() as connection:
            for row in reader:
                batch.append(parse_row(row))

                if len(batch) == batch_size:
                    connection.execute(statement, batch)
                    processed += len(batch)
                    print(f"Przetworzono: {processed}")
                    batch.clear()

            if batch:
                connection.execute(statement, batch)
                processed += len(batch)

    return processed
