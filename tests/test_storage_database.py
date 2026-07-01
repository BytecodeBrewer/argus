from datetime import date

import duckdb

from argus.domain.internal_models import DataSource, Instrument, PriceBar
from argus.storage.database import (
    initialize_database,
    insert_price_bar,
    read_price_bars,
)


def test_initialize_database_creates_required_tables(tmp_path):

    db = tmp_path / "test.duckdb"

    initialize_database(db)
    connection = duckdb.connect(db)

    tables = connection.execute("SHOW TABLES;").fetchall()
    table_names = {row[0] for row in tables}

    assert "data_sources" in table_names
    assert "instruments" in table_names
    assert "price_bars" in table_names
