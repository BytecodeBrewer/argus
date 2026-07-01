from argus.domain.internal_models import DataSource, Instrument, PriceBar
from datetime import date


def test_data_source_can_be_created() -> None:
    source = DataSource(
        name="yfinance",
        provider_kind="fx_rates",
    )

    assert source.name == "yfinance"
    assert source.provider_kind == "fx_rates"
    assert source.requires_api_key is False


def test_instrument_can_be_created() -> None:
    instrument = Instrument(
        symbol="EUR/USD",
        name="Euro / US Dollar",
        asset_class="fx",
        base_currency="EUR",
        quote_currency="USD",
    )

    assert instrument.symbol == "EUR/USD"
    assert instrument.name == "Euro / US Dollar"
    assert instrument.asset_class == "fx"
    assert instrument.base_currency == "EUR"
    assert instrument.quote_currency == "USD"
    assert instrument.currency is None
    assert instrument.exchange is None


def test_rate_bar_can_be_created() -> None:
    source = DataSource(
        name="yfinance",
        provider_kind="fx_rates",
    )

    instrument_rate = Instrument(
        symbol="EUR/USD",
        name="Euro / US Dollar",
        asset_class="fx",
        base_currency="EUR",
        quote_currency="USD",
    )

    price_bar = PriceBar(
        source=source,
        instrument=instrument_rate,
        timestamp=date(2026, 1, 1),
        timeframe="1d",
        close=1.89,
    )

    assert price_bar.source == source
    assert price_bar.instrument == instrument_rate
    assert price_bar.timestamp == date(2026, 1, 1)
    assert price_bar.timeframe == "1d"
    assert price_bar.close == 1.89
    assert price_bar.open is None
    assert price_bar.high is None
    assert price_bar.low is None
    assert price_bar.adjusted_close is None
    assert price_bar.volume is None


def test_stock_ohlcv_bar_can_be_created() -> None:
    source = DataSource(
        name="yfinance",
        provider_kind="market_prices",
    )

    instrument = Instrument(
        symbol="AAPL",
        name="Apple Inc.",
        asset_class="stock",
        currency="USD",
        exchange="NASDAQ",
    )

    price_bar = PriceBar(
        source=source,
        instrument=instrument,
        timestamp=date(2026, 1, 1),
        timeframe="1d",
        open=187.15,
        high=188.44,
        low=183.89,
        close=185.64,
        adjusted_close=184.25,
        volume=50_200_000,
    )

    assert price_bar.instrument.symbol == "AAPL"
    assert price_bar.open == 187.15
    assert price_bar.high == 188.44
    assert price_bar.low == 183.89
    assert price_bar.close == 185.64
    assert price_bar.adjusted_close == 184.25
    assert price_bar.volume == 50_200_000
