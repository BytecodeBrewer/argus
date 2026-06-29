import duckdb

def initialize_database(database_path: str) -> None:
    create_datasources_table = """ 
    CREATE TABLE IF NOT EXISTS data_sources (
        id INTEGER PRIMARY_KEY,
        name TEXT,
        provider_kind TEXT,
        requires_api_key: BOOLEAN DEFAULTS:False
    )
    """
    create_intstrument_table = """
        CREATE TABLE IF NOT EXISTS instrument (
        id INTEGER PRIMARY_KEY,
        name TEXT,
        asset_class TEXT,
        currency TEXT or NONE DEFAULTS: NONE,
        exchange TEXT or NONE DEFAULTS: NONE,
        base_currency TEXT or NONE DEFAULTS: NONE,
        quote_currency TEXT or NONE DEFAULTS: NONE
    )
    """
    create_price_bar_table = """
        CREATE TABLE IF NOT EXISTS price_bar (
        id INTEGER PRIMARY_KEY,
        source_id FOREIGN_KEY,
        instrument_id FOREIGN_KEY,
        timestamp: date,
        timeframe TEXT,
        close FLOAT,
        open: FLOAT or NONE DEFAULTS: NONE,
        high: FLOAT or NONE DEFAULTS: NONE,
        low: FLOAT or NONE DEFAULTS: NONE,
        adjusted_close FLOAT or NONE DEFAULTS: NONE,
        volume: FLOAT or NONE DEFAULTS: NONE
    )
    """
    duckdb.connect(database_path)
    duckdb.execute(query=create_datasources_table)
    duckdb.execute(query=create_intstrument_table)
    duckdb.execute(query=create_price_bar_table)
    duckdb.close()
