import yfinance as yf
import pandas as pd
from argus.domain.internal_models import (
    MarketDataRequest,
    PRICE_BAR_COLUMNS,
    YFINANCE_PRICE_BAR_MAPPING,
)


def get_timeseries(request: MarketDataRequest) -> pd.DataFrame:
    """
    Fetch historical exchange-rate time series data from Yahoo Finance.

    Args:
        curr_symbol (str): Currency symbol used by Yahoo Finance, for example
            "EURUSD=X".
        start (str): Start date of the requested time range in YYYY-MM-DD format.
        end (str): End date of the requested time range in YYYY-MM-DD format.
        interval (str): Data interval supported by Yahoo Finance, for example
            "1d", "1h", or "15m".

    Returns:
        pandas.DataFrame | empty pandas.DataFrame: A DataFrame containing pricebars columns if data was successfully fetched.
        Returns empty pandas.DataFrame if the request fails and an exception occurs (with an error message).
    """
    try:
        start = str(request.start)
        end = str(request.end)
        timeframe = request.timeframe
        curr_pair = (
            f"{request.instrument.base_currency}{request.instrument.quote_currency}=X"
        )
        raw_resp = yf.download(
            tickers=curr_pair,
            start=start,
            end=end,
            interval=timeframe,
            multi_level_index=False,
            progress=False,
        )
        if raw_resp is None:
            raise ConnectionError("Couldn't fetch data")
        if raw_resp.empty:
            raise ValueError("No data")
        resp = normalize_yfinance_bars(raw_resp)
        return resp
    except Exception:
        return pd.DataFrame()


def normalize_yfinance_bars(raw_df: pd.DataFrame) -> pd.DataFrame:
    df = raw_df.copy()
    df = df.reset_index()
    df = df.rename(columns=YFINANCE_PRICE_BAR_MAPPING)
    return df[list(PRICE_BAR_COLUMNS)]
