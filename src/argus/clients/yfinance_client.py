import yfinance as yf
import logging


def get_timeseries(curr_symbol, start, end, interval):
    try:
        yf_logger = logging.getLogger("yfinance")
        yf_logger.disabled = True
        data = yf.download(
            tickers=curr_symbol,
            start=start,
            end=end,
            interval=interval,
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

    
get_timeseries("EURUSD=X","2024-01-01","2024-01-02","1m")