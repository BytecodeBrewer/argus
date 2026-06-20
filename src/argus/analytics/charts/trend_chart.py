import matplotlib.pyplot as plt
import pandas as pd
from argus.services.timeseries_service import prepare_trend_analysis


def create_trendchart(curr: str, dates: pd.DataFrame):
    """
    Create a trend chart for exchange-rate analysis.

    Builds a Matplotlib figure showing the exchange rate, its rolling
    average, and the daily percentage change for a selected currency.
    The minimum and maximum exchange-rate values are highlighted in the
    chart.

    Args:
        curr (str): Currency code or currency pair identifier used for
            the trend analysis.
        dates (pd.DataFrame): DataFrame containing the date information
            used to prepare the time-series analysis.

    Returns:
        matplotlib.figure.Figure: Matplotlib figure containing the trend
        chart.

    Notes:
        The chart uses two y-axes:

            - The left y-axis displays the exchange rate and rolling average.
            - The right y-axis displays the daily percentage change.

        Minimum and maximum exchange-rate values are marked with scatter
        points and annotations.
    """
    df = pd.DataFrame()
    df, min_max_rates = prepare_trend_analysis(curr, dates)
    min_date = min_max_rates["min_date"][0]
    min_rate = min_max_rates["min_rate"][0]
    max_date = min_max_rates["max_date"][0]
    max_rate = min_max_rates["max_rate"][0]

    # Rate and Rolling Average needs seperat x-Achse von Daily Percentage Chnage erhalten
    fig, ax1 = plt.subplots(figsize=(5, 3.5), dpi=100)

    # Subplot 1
    ax1.plot(df["date"], df["rate"], color="black", label="Exchange Rate")
    ax1.plot(df["date"], df["roll_avg"], color="blue", label="Rolling Average")

    # Scatter and Annote Min/Max Rate
    ax1.scatter(min_date, min_rate, color="red")
    ax1.scatter(max_date, max_rate, color="green")
    ax1.annotate("Min", (min_date, min_rate))
    ax1.annotate("Max", (max_date, max_rate))

    # Rotate date values for better visibillity
    ax1.tick_params(axis="x", rotation=45)

    # Subplot 2
    ax2 = ax1.twinx()
    bar_colors = ["green" if x >= 0 else "red" for x in df["daily_pct_change"]]
    ax2.bar(
        df["date"],
        df["daily_pct_change"],
        color=bar_colors,
        alpha=0.4,
        label="Daily Change",
    )
    ax2.legend(loc="upper left")
    ax2.set_ylabel("Percentage Scale")

    # Adjust the layout
    fig.tight_layout()
    return fig
