from sqlalchemy import text

from connect_db import get_engine


QUERY = text("""
    WITH ordered_data AS (
        SELECT
            dtime_utc,
            LAG(dtime_utc) OVER (ORDER BY dtime_utc) AS previous_dtime_utc
        FROM pse_actual
    )
    SELECT
        previous_dtime_utc,
        dtime_utc,
        TIMESTAMPDIFF(
            MINUTE,
            previous_dtime_utc,
            dtime_utc
        ) AS gap_minutes
    FROM ordered_data
    WHERE TIMESTAMPDIFF(
        MINUTE,
        previous_dtime_utc,
        dtime_utcx1
    ) != 15
""")


engine = get_engine()

with engine.connect() as connection:
    gaps = connection.execute(QUERY).all()

engine.dispose()

print(f"Liczba luk: {len(gaps)}")
for gap in gaps:
    print(gap)
