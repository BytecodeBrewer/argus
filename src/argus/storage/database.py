import duckdb
from argus.domain.internal_models import DataSource, PriceBar, Instrument


def initialize_database(database_path: str) -> None:
    create_data_sources_sequence = """
    CREATE SEQUENCE IF NOT EXISTS data_sources_id_seq;
    """
    create_instruments_sequence = """
    CREATE SEQUENCE IF NOT EXISTS instruemnts_id_seq;
    """
    create_price_bars_sequence = """
    CREATE SEQUENCE IF NOT EXISTS price_bars_id_seq;
    """
    create_datasources_table = """ 
    CREATE TABLE IF NOT EXISTS data_sources (
        id INTEGER PRIMARY KEY DEFAULT nextval('data_sources_id_seq'),
        name TEXT NOT NULL UNIQUE,
        provider_kind TEXT NOT NULL,
        requires_api_key BOOLEAN NOT NULL
    );
    """
    create_intstruments_table = """
        CREATE TABLE IF NOT EXISTS instruments (
        id INTEGER PRIMARY KEY DEFAULT nextval('instruemnts_id_seq'),
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

    connection.execute(query=create_datasources_table)
    connection.execute(query=create_intstruments_table)
    connection.execute(query=create_price_bars_table)

    connection.close()


def insert_data_source(database_path, source: DataSource) -> None:
    insert_query = """
    INSERT INTO data_sources (name, provider_kind, requires_api_key)
    VALUES (?,?,?);
    """
    connection = duckdb.connect(database_path)
    connection.execute(
        query=insert_query,
        parameters=[source.name, source.provider_kind, source.requires_api_key],
    )
    connection.close()


def insert_instruemnt(database_path, instrument: Instrument) -> None:
    insert_query = """
    INSERT INTO instruments (symbol,name,asset_class)
    VALUES (?,?,?);
    """

    connection = duckdb.connect(database_path)
    connection.execute(
        query=insert_query,
        parameters=[instrument.symbol, instrument.name, instrument.asset_class],
    )
    connection.close()
