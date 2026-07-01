from dataclasses import dataclass
from datetime import date


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


@dataclass
class PriceBar:
    source: DataSource
    instrument: Instrument
    timestamp: date
    timeframe: str
    close: float
    open: float | None = None
    high: float | None = None
    low: float | None = None
    adjusted_close: float | None = None
    volume: float | None = None
