from sqlalchemy import text

from connect_db import get_engine


QUERY = text("""
    SELECT *
    FROM (
        SELECT
            dtime_utc,
            TIMESTAMPDIFF(
                MINUTE,
                LAG(dtime_utc) OVER (ORDER BY dtime_utc),
                dtime_utc
            ) AS diff
        FROM pse_actual
    ) AS data
    WHERE diff != 15
""")


engine = get_engine()

with engine.connect() as connection:
    gaps = connection.execute(QUERY).all()

engine.dispose()

print(f"Liczba luk: {len(gaps)}")
for gap in gaps:
    print(gap)
