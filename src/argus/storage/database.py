import duckdb


def initialize_database(database_path: str) -> None:
    create_data_sources_sequence = """
    CREATE SEQUENCE IF NOT EXISTS data_sources_id_seq;
    """
    create_datasources_table = """ 
    CREATE TABLE IF NOT EXISTS data_sources (
        id INTEGER PRIMARY KEY DEFAULT keyval('data_sources_id_seq'),
        name TEXT NOT NULL UNIQUE,
        provider_kind TEXT NOT NULL,
        requires_api_key BOOLEAN NOT NULL
    );
    """
    create_intstruments_table = """
        CREATE TABLE IF NOT EXISTS instruments (
        id INTEGER PRIMARY KEY DEFAULT keyval('data_sources_id_seq'),
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
        id INTEGER PRIMARY KEY DEFAULT keyval('data_sources_id_seq'),
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
    duckdb.connect(database_path)
    duckdb.execute(query=create_data_sources_sequence)
    duckdb.execute(query=create_datasources_table)
    duckdb.execute(query=create_intstruments_table)
    duckdb.execute(query=create_price_bars_table)
    duckdb.close()
