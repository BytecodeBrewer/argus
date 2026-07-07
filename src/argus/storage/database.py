import duckdb
from datetime import date
import pandas as pd
from argus.domain.internal_models import (
    DataSource,
    Instrument,
    MarketDataRequest,
    MarketDataResponse,
    PRICE_BAR_COLUMNS,
)


def initialize_database(database_path: str) -> None:
    """
    Initialize the DuckDB database schema.

    Creates the required sequences and tables for data sources,
    instruments, and price bars.

    Args:
        database_path (str): Path to the DuckDB database file.

    Returns:
        None
    """
    queries = [
        "CREATE SEQUENCE IF NOT EXISTS data_sources_id_seq;",
        "CREATE SEQUENCE IF NOT EXISTS instruments_id_seq;",
        "CREATE SEQUENCE IF NOT EXISTS price_bars_id_seq;",
        """
        CREATE TABLE IF NOT EXISTS data_sources (
            id INTEGER PRIMARY KEY DEFAULT nextval('data_sources_id_seq'),
            name TEXT NOT NULL UNIQUE,
            provider_kind TEXT NOT NULL,
            requires_api_key BOOLEAN NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS instruments (
            id INTEGER PRIMARY KEY DEFAULT nextval('instruments_id_seq'),
            symbol TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            asset_class TEXT NOT NULL,
            currency TEXT,
            exchange TEXT,
            base_currency TEXT,
            quote_currency TEXT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS price_bars (
            id INTEGER PRIMARY KEY DEFAULT nextval('price_bars_id_seq'),
            source_id INTEGER NOT NULL,
            instrument_id INTEGER NOT NULL,
            timestamp DATE NOT NULL,
            timeframe TEXT NOT NULL,
            close DOUBLE NOT NULL,
            open DOUBLE,
            high DOUBLE,
            low DOUBLE,
            adjusted_close DOUBLE,
            volume DOUBLE,
            FOREIGN KEY (source_id) REFERENCES data_sources (id),
            FOREIGN KEY (instrument_id) REFERENCES instruments (id),
            UNIQUE (source_id, instrument_id, timestamp, timeframe)
        );
        """,
    ]

    connection = duckdb.connect(database_path)
    try:
        for query in queries:
            connection.execute(query)
    finally:
        connection.close()


def get_or_create_source(connection, source: DataSource) -> int:
    """
    Get an existing data source ID or create a new data source.

    Searches for a data source by name. If it already exists, its ID is
    returned. Otherwise, the data source is inserted and the new ID is
    returned.

    Args:
        connection: Active DuckDB connection.
        source (DataSource): Data source model containing provider metadata.

    Returns:
        int: Database ID of the existing or newly created data source.

    Raises:
        ValueError: If the data source could not be inserted or found.
    """
    insert_query = """
    INSERT INTO data_sources (name, provider_kind, requires_api_key)
    VALUES (?,?,?)
    ON CONFLICT DO NOTHING;
    """
    search_query = """
    SELECT id FROM data_sources
    WHERE name=?
    """

    result = connection.execute(
        query=search_query,
        parameters=[source.name],
    ).fetchone()
    if result is not None:
        return result[0]

    connection.execute(
        query=insert_query,
        parameters=[source.name, source.provider_kind, source.requires_api_key],
    )

    result = connection.execute(
        query=search_query,
        parameters=[source.name],
    ).fetchone()

    if result is None:
        raise ValueError("Data source could not be inserted.")

    return result[0]


def get_or_create_instrument(connection, instrument: Instrument) -> int:
    """
    Get an existing instrument ID or create a new instrument.

    Searches for an instrument by symbol. If it already exists, its ID is
    returned. Otherwise, the instrument is inserted and the new ID is
    returned.

    Args:
        connection: Active DuckDB connection.
        instrument (Instrument): Instrument model containing symbol and
            asset metadata.

    Returns:
        int: Database ID of the existing or newly created instrument.

    Raises:
        ValueError: If the instrument could not be inserted or found.
    """
    insert_query = """
    INSERT INTO instruments (
        symbol,
        name,
        asset_class,
        currency,
        exchange,
        base_currency,
        quote_currency)
    VALUES (?,?,?,?,?,?,?)
    ON CONFLICT DO NOTHING;
    """
    search_query = """
    SELECT id FROM instruments
    WHERE symbol=?
    """

    result = connection.execute(
        query=search_query,
        parameters=[instrument.symbol],
    ).fetchone()
    if result is not None:
        return result[0]

    connection.execute(
        query=insert_query,
        parameters=[
            instrument.symbol,
            instrument.name,
            instrument.asset_class,
            instrument.currency,
            instrument.exchange,
            instrument.base_currency,
            instrument.quote_currency,
        ],
    )
    result = connection.execute(
        query=search_query,
        parameters=[instrument.symbol],
    ).fetchone()

    if result is None:
        raise ValueError("Instrument could not be inserted.")

    return result[0]


def insert_price_bar(db: str, marketdata: MarketDataResponse) -> None:
    """
    Insert a price bar into the database.

    Ensures that the related data source and instrument exist, then inserts
    the price bar into the ``price_bars`` table. Duplicate price bars are
    ignored through the table's unique constraint.

    Args:
        db (str): Path to the DuckDB database file.
        price_bar (PriceBar): Price bar model containing source,
            instrument, timestamp, timeframe, and market values.

    Returns:
        None
    """
    insert_query = """
        INSERT INTO price_bars (
            source_id,
            instrument_id,
            timestamp,
            close,
            open,
            high,
            low,
            adjusted_close,
            volume
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT DO NOTHING;
        """
    connection = duckdb.connect(db)
    try:
        source_id = get_or_create_source(connection, marketdata.source)
        instrument_id = get_or_create_instrument(connection, marketdata.instrument)
        if marketdata.bars is None:
            return None
        for _, row in marketdata.bars.iterrows():
            connection.execute(
                query=insert_query,
                parameters=[
                    source_id,
                    instrument_id,
                    MarketDataResponse.bars["time"],
                    MarketDataResponse.bars["close"],
                    MarketDataResponse.bars["open"],
                    MarketDataResponse.bars["high"],
                    MarketDataResponse.bars["low"],
                    MarketDataResponse.bars["adjusted_close"],
                    MarketDataResponse.bars["volume"],
                ],
            )
    finally:
        connection.close()


def read_price_bars(db: str, request: MarketDataRequest) -> pd.DataFrame:
    """
    Read price bars for a source, instrument, and date range.

    Queries stored price bars joined with their data source and instrument
    metadata. Results are ordered by timestamp and returned as a pandas
    DataFrame.

    Args:
        db (str): Path to the DuckDB database file.
        source (DataSource): Data source used to filter the stored price bars.
        instrument (Instrument): Instrument used to filter the stored price bars.
        start_date (date): Inclusive start date of the requested time range.
        end_date (date): Inclusive end date of the requested time range.

    Returns:
        pd.DataFrame: DataFrame containing matching price bars and metadata.
    """

    search_query = """
    SELECT
        data_sources.name AS source_name,
        instruments.symbol AS instrument_symbol,
        price_bars.timestamp,
        price_bars.timeframe,
        price_bars.open,
        price_bars.high,
        price_bars.low,
        price_bars.close,
        price_bars.adjusted_close,
        price_bars.volume
    FROM price_bars
    JOIN data_sources ON price_bars.source_id = data_sources.id
    JOIN instruments ON price_bars.instrument_id = instruments.id
    WHERE data_sources.name = ?
      AND instruments.symbol = ?
      AND price_bars.timestamp BETWEEN ? AND ?
    ORDER BY price_bars.timestamp;
    """

    connection = duckdb.connect(db)
    try:
        result = connection.execute(
            query=search_query,
            parameters=[
                request.source.name,
                request.instrument.symbol,
                request.start,
                request.end,
            ],
        ).df()
    finally:
        connection.close()
    return result
