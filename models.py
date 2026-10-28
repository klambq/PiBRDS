from sqlalchemy import (
    Column,
    Date,
    Index,
    MetaData,
    Numeric,
    String,
    Table,
    UniqueConstraint,
)
from sqlalchemy.dialects.mysql import BIGINT, DATETIME


metadata = MetaData()


pse_actual = Table(
    "pse_actual",
    metadata,
    Column(
        "id",
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    ),
    Column("business_date", Date, nullable=False),
    Column("dtime", String(20), nullable=False),
    Column("dtime_utc", DATETIME(), nullable=False),
    Column("period", String(15), nullable=False),
    Column("period_utc", String(13), nullable=False),
    Column("demand", Numeric(10, 3), nullable=False),
    Column("swm_p", Numeric(10, 3), nullable=False),
    Column("swm_np", Numeric(10, 3), nullable=False),
    Column("jg", Numeric(10, 3), nullable=False),
    Column("jgw1", Numeric(10, 3), nullable=False),
    Column("jgm1", Numeric(10, 3), nullable=False),
    Column("jnwrb", Numeric(10, 3), nullable=False),
    Column("jgm", Numeric(10, 3), nullable=False),
    Column("wi", Numeric(10, 3), nullable=False),
    Column("pv", Numeric(10, 3), nullable=False),
    UniqueConstraint("dtime_utc", name="uq_pse_actual_dtime_utc"),
)


pse_forecast_pkd = Table(
    "pse_forecast_pkd",
    metadata,
    Column(
        "id",
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    ),
    Column("dtime", String(20), nullable=False),
    Column("gen_fv", Numeric(10, 1), nullable=False),
    Column("gen_wi", Numeric(10, 1), nullable=False),
    Column("period", String(15), nullable=False),
    Column("dtime_utc", DATETIME(), nullable=False),
    Column("period_utc", String(13), nullable=False),
    Column("business_date", Date, nullable=False),
    Column("publication_ts", DATETIME(fsp=6), nullable=False),
    Column("publication_ts_utc", DATETIME(fsp=6), nullable=False),
    UniqueConstraint(
        "dtime_utc",
        "publication_ts_utc",
        name="uq_pse_forecast_pkd",
    ),
    Index("idx_pse_forecast_pkd_business_date", "business_date"),
    Index(
        "idx_pse_forecast_pkd_publication_ts_utc",
        "publication_ts_utc",
    ),
)
