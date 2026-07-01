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
    connection.close()
    table_names = {row[0] for row in tables}

    assert "data_sources" in table_names
    assert "instruments" in table_names
    assert "price_bars" in table_names


def test_data_is_inserted(tmp_path):
    source = DataSource(
        name="Yahoo", provider_kind="yfinance_api", requires_api_key=False
    )

    instrument = Instrument(
        symbol="EUR/USD",
        name="EUR - USD Rate",
        asset_class="fx",
        base_currency="EUR",
        quote_currency="USD",
    )

    pricebar = PriceBar(
        source=source,
        instrument=instrument,
        timestamp=date(2026, 1, 1),
        timeframe="1d",
        close=1.89,
    )

    db = tmp_path / "test.duckdb"
    initialize_database(db)
    insert_price_bar(db, pricebar)
    connection = duckdb.connect(db)

    instrument_count = connection.execute(
        "SELECT COUNT(*) FROM instruments;"
    ).fetchone()

    source_count = connection.execute("SELECT COUNT(*) FROM data_sources;").fetchone()

    price_bar_count = connection.execute("SELECT COUNT(*) FROM price_bars;").fetchone()

    assert instrument_count is not None
    assert source_count is not None
    assert price_bar_count is not None
    assert instrument_count[0] == 1
    assert source_count[0] == 1
    assert price_bar_count[0] == 1


def test_fx_has_correct_format(tmp_path):
    source = DataSource(
        name="Yahoo", provider_kind="yfinance_api", requires_api_key=False
    )

    instrument = Instrument(
        symbol="EUR/USD",
        name="EUR - USD Rate",
        asset_class="fx",
        base_currency="EUR",
        quote_currency="USD",
    )

    pricebar = PriceBar(
        source=source,
        instrument=instrument,
        timestamp=date(2026, 1, 1),
        timeframe="1d",
        close=1.89,
    )

    db = tmp_path / "test.duckdb"
    initialize_database(db)
    insert_price_bar(db, pricebar)
    connection = duckdb.connect(db)

    price_bar_fx = connection.execute("SELECT * FROM price_bars;").fetchone()
    connection.close()

    assert price_bar_fx is not None
    assert price_bar_fx[0] == 1
    assert price_bar_fx[1] == 1
    assert price_bar_fx[2] == 1
    assert price_bar_fx[3] == date(2026, 1, 1)
    assert price_bar_fx[4] == "1d"
    assert price_bar_fx[5] == 1.89
    assert price_bar_fx[6] is None
    assert price_bar_fx[7] is None
    assert price_bar_fx[8] is None
    assert price_bar_fx[9] is None
    assert price_bar_fx[10] is None


def test_duplicates_are_ignored(tmp_path):
    source = DataSource(
        name="Yahoo", provider_kind="yfinance_api", requires_api_key=False
    )

    instrument = Instrument(
        symbol="EUR/USD",
        name="EUR - USD Rate",
        asset_class="fx",
        base_currency="EUR",
        quote_currency="USD",
    )

    pricebar = PriceBar(
        source=source,
        instrument=instrument,
        timestamp=date(2026, 1, 1),
        timeframe="1d",
        close=1.89,
    )

    db = tmp_path / "test.duckdb"
    initialize_database(db)
    insert_price_bar(db, pricebar)
    insert_price_bar(db, pricebar)
    connection = duckdb.connect(db)
    count = connection.execute("SELECT COUNT(*) FROM price_bars;").fetchone()

    assert count is not None
    assert count[0] == 1


def test_read_price_bars_returns_matching_data(tmp_path):
    source = DataSource(
        name="Yahoo",
        provider_kind="yfinance_api",
        requires_api_key=False,
    )

    instrument = Instrument(
        symbol="EUR/USD",
        name="EUR - USD Rate",
        asset_class="fx",
        base_currency="EUR",
        quote_currency="USD",
    )

    pricebar = PriceBar(
        source=source,
        instrument=instrument,
        timestamp=date(2026, 1, 1),
        timeframe="1d",
        close=1.89,
    )

    db = tmp_path / "test.duckdb"
    initialize_database(db)
    insert_price_bar(db, pricebar)

    result = read_price_bars(
        db=db,
        source=source,
        instrument=instrument,
        start_date=date(2026, 1, 1),
        end_date=date(2026, 1, 31),
    )

    assert result.empty is False
    assert len(result) == 1
    assert result.iloc[0]["source_name"] == "Yahoo"
    assert result.iloc[0]["instrument_symbol"] == "EUR/USD"
    assert result.iloc[0]["timeframe"] == "1d"
    assert result.iloc[0]["close"] == 1.89


def test_read_price_bars_returns_empty_dataframe_for_missing_range(tmp_path):
    source = DataSource(
        name="Yahoo",
        provider_kind="yfinance_api",
        requires_api_key=False,
    )

    instrument = Instrument(
        symbol="EUR/USD",
        name="EUR - USD Rate",
        asset_class="fx",
        base_currency="EUR",
        quote_currency="USD",
    )

    pricebar = PriceBar(
        source=source,
        instrument=instrument,
        timestamp=date(2026, 1, 1),
        timeframe="1d",
        close=1.89,
    )

    db = tmp_path / "test.duckdb"
    initialize_database(db)
    insert_price_bar(db, pricebar)

    result = read_price_bars(
        db=db,
        source=source,
        instrument=instrument,
        start_date=date(2027, 1, 1),
        end_date=date(2027, 1, 31),
    )

    assert result.empty is True
