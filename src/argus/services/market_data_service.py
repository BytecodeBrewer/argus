import pandas as pd
from datetime import date
from argus.domain.internal_models import DataSource, PriceBar, Instrument
from argus.clients.yfinance_client import get_timeseries
from argus.storage.database import read_price_bars
from argus.analytics.metrics.trend_metrics import (
    add_rolling_average,
    add_daily_percentage_change,
    get_min_max_rates,
)
from argus.analytics.charts.trend_chart import create_trendchart


def prepare_trend_analysis(df: pd.DataFrame):
    """
    Prepare time-series data for trend analysis.

    Fetches historical exchange-rate data for the given currency symbol and
    enriches it with daily percentage changes and a rolling average. It also
    calculates the minimum and maximum exchange rates for the resulting time
    series.

    Args:
        df (pd.Dataframe): A timeserie with market data

    Returns:
        tuple[pd.DataFrame, dict] | None: A tuple containing the prepared
        DataFrame and a dictionary with minimum and maximum rates. Returns
        ``None`` if no time-series data could be fetched.
    """

    df = add_daily_percentage_change(df)
    df = add_rolling_average(df)
    min_max_rates = get_min_max_rates(df)
    if df is None:
        return None
    fig = create_trendchart(df, min_max_rates)
    return fig


def get_market_data(
    db: str,
    source: DataSource,
    instrument: Instrument,
    bar: PriceBar,
    start_date: date,
    end_date: date,
) -> pd.DataFrame | None:
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
    df, isNotEmpty = read_price_bars(
        db=db,
        source=source,
        instrument=instrument,
        start_date=start_date,
        end_date=end_date,
    )
    if isNotEmpty:
        return df
    else:
        df = get_timeseries(
            source=source,
            instrument=instrument,
            bar=bar,
            start_date=start_date,
            end_date=end_date,
        )
    if df is None:
        return None
    return df
