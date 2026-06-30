import duckdb
from argus.domain.internal_models import DataSource, PriceBar, Instrument


def initialize_database(database_path: str) -> None:
    create_data_sources_sequence = """
    CREATE SEQUENCE IF NOT EXISTS data_sources_id_seq;
    """
    create_instruments_sequence = """
    CREATE SEQUENCE IF NOT EXISTS instruments_id_seq;
    """
    create_price_bars_sequence = """
    CREATE SEQUENCE IF NOT EXISTS price_bars_id_seq;
    """
    create_data_sources_table = """ 
    CREATE TABLE IF NOT EXISTS data_sources (
        id INTEGER PRIMARY KEY DEFAULT nextval('data_sources_id_seq'),
        name TEXT NOT NULL UNIQUE,
        provider_kind TEXT NOT NULL,
        requires_api_key BOOLEAN NOT NULL
    );
    """
    create_instruments_table = """
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
    """
    create_price_bars_table = """
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
        FOREIGN KEY (instrument_id) REFERENCES instruments (id)
    );
    """
    connection = duckdb.connect(database_path)

    connection.execute(query=create_data_sources_sequence)
    connection.execute(query=create_instruments_sequence)
    connection.execute(query=create_price_bars_sequence)

    connection.execute(query=create_data_sources_table)
    connection.execute(query=create_instruments_table)
    connection.execute(query=create_price_bars_table)

    connection.close()


def get_or_create_source(connection, source: DataSource) -> int:
    insert_query = """
    INSERT INTO data_sources (name, provider_kind, requires_api_key)
    VALUES (?,?,?);
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
    insert_query = """
    INSERT INTO instruments (
        symbol,
        name,
        asset_class,
        currency,
        exchange,
        base_currency,
        quote_currency)
    VALUES (?,?,?,?,?,?,?);
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


def insert_price_bar(db: str, price_bar: PriceBar) -> None:
    insert_query = """
        INSERT INTO price_bars (
            source_id,
            instrument_id,
            timestamp,
            timeframe,
            close,
            open,
            high,
            low,
            adjusted_close,
            volume
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
    connection = duckdb.connect(db)
    try:
        source_id = get_or_create_source(connection, price_bar.source)
        instrument_id = get_or_create_instrument(connection, price_bar.instrument)
        connection.execute(
            query=insert_query,
            parameters=[
                source_id,
                instrument_id,
                price_bar.timestamp,
                price_bar.timeframe,
                price_bar.close,
                price_bar.open,
                price_bar.high,
                price_bar.low,
                price_bar.adjusted_close,
                price_bar.volume,
            ],
        )
        connection.close()
    finally:
        connection.close()

def get_price_bar(db: str,source:DataSource,instrument:Instrument,start_time:str,end_time:str):
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
        WHERE data_sources.name = ? AND instruments.symbol = ? AND price_bars.timestamp BETWEEN ? AND ?
        JOIN data_sources ON price_bars.source_id = data_sources.id
        JOIN instruments ON price_bars.instrument_id = instruments.id
        """
    connection = duckdb.connect(db)
    result = connection.execute(search_query,parameters=[source.name,instrument.symbol,start_time,end_time])
    connection.close()
    return result
