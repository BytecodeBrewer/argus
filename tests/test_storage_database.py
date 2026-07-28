from datetime import date

import duckdb
import pandas as pd
import pytest

from argus.domain.internal_models import (
    DataSource,
    Instrument,
    MarketDataRequest,
    MarketDataResponse,
)
from argus.storage.database import (
    initialize_database,
    insert_price_bar,
    read_price_bars,
)


@pytest.fixture
def sample_source():
    return DataSource(
        name="Yahoo", provider_kind="yfinance_api", requires_api_key=False
    )


@pytest.fixture
def sample_instrument():
    return Instrument(
        symbol="EUR/USD",
        name="EUR - USD Rate",
        asset_class="fx",
        base_currency="EUR",
        quote_currency="USD",
    )


@pytest.fixture
def sample_response(sample_source, sample_instrument):
    test_bar = {
        "timestamp": date(2026, 1, 1),
        "open": None,
        "high": None,
        "low": None,
        "close": 1.89,
        "adjusted_close": None,
        "volume": None,
    }
    return MarketDataResponse(
        source=sample_source,
        instrument=sample_instrument,
        bars=pd.DataFrame(test_bar, index=[0]),
    )


@pytest.fixture
def db_path(tmp_path):
    db = tmp_path / "test.duckdb"
    initialize_database(db)
    return db


def test_initialize_database_creates_required_tables(db_path):
    connection = duckdb.connect(str(db_path))
    tables = connection.execute("SHOW TABLES;").fetchall()
    connection.close()
    table_names = {row[0] for row in tables}

    assert "data_sources" in table_names
    assert "instruments" in table_names
    assert "price_bars" in table_names


def test_data_is_inserted(db_path, sample_response) -> None:
    insert_price_bar(db_path, sample_response)

    connection = duckdb.connect(str(db_path))

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


def test_fx_has_correct_format(db_path, sample_response) -> None:
    insert_price_bar(db_path, sample_response)

    connection = duckdb.connect(str(db_path))
    try:
        price_bar_fx = connection.execute("SELECT * FROM price_bars;").fetchone()
    finally:
        connection.close()

    assert price_bar_fx is not None
    assert price_bar_fx[0] == 1
    assert price_bar_fx[1] == 1
    assert price_bar_fx[2] == 1
    assert price_bar_fx[3] == date(2026, 1, 1)
    assert price_bar_fx[4] == 1.89
    assert price_bar_fx[5] is None
    assert price_bar_fx[6] is None
    assert price_bar_fx[7] is None
    assert price_bar_fx[8] is None
    assert price_bar_fx[9] is None


def test_duplicates_are_ignored(db_path, sample_response) -> None:
    insert_price_bar(db_path, sample_response)
    insert_price_bar(db_path, sample_response)  # Erneuter Insert des Duplikats

    connection = duckdb.connect(str(db_path))
    try:
        count = connection.execute("SELECT COUNT(*) FROM price_bars;").fetchone()
    finally:
        connection.close()

    assert count is not None
    assert count[0] == 1


def test_read_price_bars_returns_matching_data(
    db_path, sample_source, sample_instrument, sample_response
) -> None:
    req = MarketDataRequest(
        source=sample_source,
        instrument=sample_instrument,
        timeframe="1d",
        start=date(2026, 1, 1),
        end=date(2026, 1, 1),
    )
    insert_price_bar(db_path, sample_response)

    result = read_price_bars(db_path, req)

    assert len(result) == 1
    assert result.iloc[0]["close"] == 1.89


def test_read_price_bars_returns_empty_dataframe_for_missing_range(
    db_path, sample_source, sample_instrument
) -> None:
    req = MarketDataRequest(
        source=sample_source,
        instrument=sample_instrument,
        timeframe="1d",
        start=date(2026, 1, 1),
        end=date(2026, 1, 1),
    )

    result = read_price_bars(db_path, req)

    assert result.empty is True
