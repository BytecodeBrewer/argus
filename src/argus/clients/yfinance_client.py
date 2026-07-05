import yfinance as yf
import logging
from datetime import date
from argus.domain.internal_models import DataSource, Instrument, PriceBar


def get_timeseries(
    source: DataSource,
    instrument: Instrument,
    bar: PriceBar,
    start_date: date,
    end_date: date,
):
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
        pandas.DataFrame | None: A DataFrame containing the columns ``date`` and
        ``rate`` if data was successfully fetched. Returns ``None`` if the
        request fails, returns no data, or an exception occurs.
    """
    try:
        yf_logger = logging.getLogger("yfinance")
        yf_logger.disabled = True
        data = yf.download(
            tickers=instrument.base_currency,
            start=start_date,
            end=end_date,
            interval=bar.timeframe,
            multi_level_index=False,
            progress=False,
        )
        yf_logger.disabled = False
        if data is None:
            return None
        if data.empty:
            return None
        data = data.reset_index()
        data = data[["Date", "Close"]]
        data = data.rename(columns={"Date": "date", "Close": "rate"})
        return data
    except Exception:
        return None
