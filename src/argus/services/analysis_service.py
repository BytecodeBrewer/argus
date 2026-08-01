from matplotlib.figure import Figure
import pandas as pd
from argus.analytics.charts.trend_chart import create_trendchart
from argus.analytics.predictions.models import create_lin_regression
from argus.analytics.metrics.trend_metrics import (
    add_daily_percentage_change,
    add_rolling_average,
    get_min_max_rates,
)
from argus.domain.internal_models import MarketDataRequest
from argus.services.market_data_service import get_market_data


def prepare_trend_analysis(db: str, request: MarketDataRequest) -> Figure | str:
    """
    Prepare time-series data and generate a trend analysis chart.

    Enriches the historical exchange-rate DataFrame with daily percentage changes
    and a rolling average, calculates the minimum and maximum rates, and uses
    the result to build a trend visualization chart.

    Args:
        df (pd.DataFrame): A DataFrame containing market data time-series.

    Returns:
        plotly.graph_objects.Figure: A figure object representing the
        generated trend chart.
    """
    response = get_market_data(db, request)

    if response.message:
        return response.message

    df = response.bars.copy()
    df = add_daily_percentage_change(df)
    df = add_rolling_average(df)
    min_max_rates = get_min_max_rates(df)
    fig = create_trendchart(df, min_max_rates)
    return fig

def add_prediction(db: str, request: MarketDataRequest) -> pd.DataFrame:
    response = get_market_data(db, request)
    predict_data = create_lin_regression(response.bars)
    return predict_data