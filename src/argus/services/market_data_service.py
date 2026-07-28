import pandas as pd

from argus.clients.yfinance_client import get_timeseries
from argus.domain.internal_models import MarketDataRequest, MarketDataResponse
from argus.storage.database import insert_price_bar, read_price_bars


def get_market_data(
    db: str,
    request: MarketDataRequest,
) -> MarketDataResponse:
    """
    Get a time series either from local stroage or client with first-storage-workflow

    Args:
        curr_symbol (str): Currency symbol used by Yahoo Finance, for example
            "EURUSD=X".
        start (str): Start date of the requested time range in YYYY-MM-DD format.
        end (str): End date of the requested time range in YYYY-MM-DD format.
        intervall (str): Data interval supported by Yahoo Finance, for example
            "1d", "1h", or "15m".

    Returns:
        pd.DataFrame | None: A
        DataFrame with dates and rates. Returns
        ``None`` if no time-series data could be fetched.
    """
    bars = read_price_bars(db, request)
    if not (bars.empty):
        db_response = MarketDataResponse(
            source=request.source, instrument=request.instrument, bars=bars, message=""
        )
        return db_response

    try:
        bars = get_timeseries(request)
        api_response = MarketDataResponse(
            source=request.source, instrument=request.instrument, bars=bars
        )
        insert_price_bar(db, api_response)
        return api_response
    except (ConnectionError, ValueError) as e:
        return MarketDataResponse(
            source=request.source,
            instrument=request.instrument,
            bars=pd.DataFrame(),
            message=str(e),
        )
