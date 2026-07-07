from argus.domain.internal_models import MarketDataRequest, MarketDataResponse
from argus.clients.yfinance_client import get_timeseries
from argus.clients.exchangerate_client import get_rates
from argus.domain.validation import check_currency
from argus.storage.database import read_price_bars, insert_price_bar
import pandas as pd


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


def get_conv_rate(req: MarketDataRequest) -> float | None:
    """
    Gets the conversion rate between two currencies.

    Arg1: resp1: str - the first currency code
    Arg2: resp2: str - the second currency code

    Return: float or None - the conversion rate if found, otherwise None
    """

    data = get_rates(req)

    if data is None:
        return None

    return float(data["conversion_rate"])


def convert(amount: float, req: MarketDataRequest) -> float | None:
    """
    Converts an amount from one currency to another using the conversion rate.

    Arg1: amount: float - the amount to be converted
    Arg2: resp1: str - the first currency code
    Arg3: resp2: str - the second currency code

    Return: float or None - the converted amount if conversion rate is found, otherwise None
    """

    rate = get_conv_rate(req)
    if rate is not None:
        return amount * rate
    return None
