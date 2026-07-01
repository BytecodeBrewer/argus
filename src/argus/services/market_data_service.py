import pandas as pd
from argus.clients.yfinance_client import get_timeseries
from argus.analytics.metrics.trend_metrics import (
    add_rolling_average,
    add_daily_percentage_change,
    get_min_max_rates,
)


def prepare_trend_analysis(
    curr_symbol: str, start: str, end: str, intervall: str
) -> tuple[pd.DataFrame, dict] | None:
    """
    Prepare time-series data for trend analysis.

    Fetches historical exchange-rate data for the given currency symbol and
    enriches it with daily percentage changes and a rolling average. It also
    calculates the minimum and maximum exchange rates for the resulting time
    series.

    Args:
        curr_symbol (str): Currency symbol used by Yahoo Finance, for example
            "EURUSD=X".
        start (str): Start date of the requested time range in YYYY-MM-DD format.
        end (str): End date of the requested time range in YYYY-MM-DD format.
        intervall (str): Data interval supported by Yahoo Finance, for example
            "1d", "1h", or "15m".

    Returns:
        tuple[pd.DataFrame, dict] | None: A tuple containing the prepared
        DataFrame and a dictionary with minimum and maximum rates. Returns
        ``None`` if no time-series data could be fetched.
    """

    df = get_timeseries(curr_symbol, start, end, intervall)
    if df is None:
        return None
    df = add_daily_percentage_change(df)
    df = add_rolling_average(df)
    min_max_rates = get_min_max_rates(df)
    return df, min_max_rates
