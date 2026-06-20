import pandas as pd
from argus.clients.mock_client import get_mock_timeseries
from argus.analytics.metrics.trend_metrics import (
    add_rolling_average,
    add_daily_percentage_change,
    get_min_max_rates,
)


def prepare_trend_analysis(
    mock_curr: str, df: pd.DataFrame
) -> tuple[pd.DataFrame, dict]:
    """
    Prepares the data for trend analysis by adding conversion rates, daily percentage change, and rolling average.

    Arg1: mock_curr: str - the currency code for which the trend analysis is to
    be performed
    Arg2: df: pd.DataFrame - the DataFrame containing the dates for which the
    conversion rates are to be added

    Return: tuple[pd.DataFrame, dict] - a tuple containing the updated DataFrame with conversion rates,
    daily percentage change, and rolling average, and a dictionary with the minimum and maximum rates
    """
    df["rate"] = 0.0
    # For each date one API call to get the rate
    for i in range(len(df)):
        date = str(df.loc[i, "date"])
        df.loc[i, "rate"] = get_mock_timeseries(mock_curr, date)
    df = add_daily_percentage_change(df)
    df = add_rolling_average(df)
    min_max_rates = get_min_max_rates(df)
    return df, min_max_rates
