import yfinance as yf
import pandas as pd
from argus.domain.internal_models import (
    MarketDataRequest,
    PRICE_BAR_COLUMNS,
    YFINANCE_PRICE_BAR_MAPPING,
)


def get_timeseries(request: MarketDataRequest) -> pd.DataFrame:
    start = str(request.start)
    end = str(request.end)
    timeframe = request.timeframe
    curr_pair = (
        f"{request.instrument.base_currency}{request.instrument.quote_currency}=X"
    )

    try:
        raw_resp = yf.download(
            tickers=curr_pair,
            start=start,
            end=end,
            interval=timeframe,
            multi_level_index=False,
            progress=False,
        )
    except Exception:
        raise ConnectionError("Network error or connection timeout")

    if raw_resp is None:
        raise ConnectionError("Yahoo Finance API returned an invalid response")

    if (
        raw_resp.empty
        or "Close" not in raw_resp.columns
        or raw_resp["Close"].dropna().empty
    ):
        raise ValueError("Quote not found or no data available for symbol")

    resp = normalize_yfinance_bars(raw_resp)
    return resp


def normalize_yfinance_bars(raw_df: pd.DataFrame) -> pd.DataFrame:
    df = raw_df.copy()
    df = df.reset_index()
    df = df.rename(columns=YFINANCE_PRICE_BAR_MAPPING)
    return df[list(PRICE_BAR_COLUMNS)]
