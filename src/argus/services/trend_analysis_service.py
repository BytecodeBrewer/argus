import pandas as pd
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
    fig = create_trendchart(df, min_max_rates)
    return fig
