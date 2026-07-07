from dataclasses import dataclass
from datetime import date
import pandas as pd


@dataclass
class DataSource:
    name: str
    provider_kind: str
    requires_api_key: bool = False


@dataclass
class Instrument:
    symbol: str
    name: str
    asset_class: str
    currency: str | None = None
    exchange: str | None = None
    base_currency: str | None = None
    quote_currency: str | None = None


PRICE_BAR_COLUMNS = (
    "timestamp",
    "open",
    "high",
    "low",
    "close",
    "adjusted_close",
    "volume",
)

YFINANCE_PRICE_BAR_MAPPING = {
    "Date": "timestamp",
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Adj Close": "adjusted_close",
    "Volume": "volume",
}


@dataclass
class MarketDataRequest:
    source: DataSource
    instrument: Instrument
    timeframe: str
    start: date
    end: date


@dataclass
class MarketDataResponse:
    source: DataSource
    instrument: Instrument
    bars: pd.DataFrame
    message: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.bars, pd.DataFrame):
            raise TypeError("bars must be a pandas DataFrame")
        if self.message == "":
            missing_cols = [
                col for col in PRICE_BAR_COLUMNS if col not in self.bars.columns
            ]
            if missing_cols:
                raise ValueError(
                    f"Missing required columns in bars DataFrame: {missing_cols}"
                )
