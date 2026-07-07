from argus.clients.yfinance_client import get_timeseries
from argus.domain.internal_models import (
    DataSource,
    Instrument,
    MarketDataRequest,
    MarketDataResponse,
)
from datetime import date
import pandas as pd
import pandas.testing as pdt

"""
def test_get_dataframe(monkeypatch):
    test_resp = pd.DataFrame(
        {
            "Close": [1.105583, 1.103875, 1.094176],
        },
        index=pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]),
    )
    test_resp.index.name = "Date"
    source = DataSource(name="YFinance API", provider_kind="yfinance")
    instrument = Instrument(
        symbol="EUR - USD",
        name="EUR/USD",
        asset_class="fx",
        base_currency="EUR",
        quote_currency="USD",
    )
    req = MarketDataRequest(
        source=source,
        instrument=instrument,
        timeframe="1d",
        start=date(2024, 1, 1),
        end=date(2024, 1, 4),
    )

    def fake_yfinance_download(*args, **kwargs):
        return test_resp

    monkeypatch.setattr("yfinance.download", fake_yfinance_download)
    resp = get_timeseries(req)
    expected = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]),
            "rate": [1.105583, 1.103875, 1.094176],
        }
    )

    assert resp is not None
    pdt.assert_frame_equal(resp, expected)


def test_get_none(monkeypatch):
    source = DataSource(name="YFinance API", provider_kind="yfinance")
    instrument = Instrument(symbol="EUR - USD", name="EUR/USD", asset_class="fx")
    req = MarketDataRequest(
        source=source,
        instrument=instrument,
        timeframe="1d",
        start=date(2026, 1, 1),
        end=date(2026, 1, 4),
    )

    def fake_yfinance_download(*args, **kwargs):
        return None

    monkeypatch.setattr("yfinance.download", fake_yfinance_download)

    resp = get_timeseries(req)
    assert resp is None


def test_get_empty_frame(monkeypatch):
    source = DataSource(name="YFinance API", provider_kind="yfinance")
    instrument = Instrument(symbol="EUR - USD", name="EUR/USD", asset_class="fx")
    req = MarketDataRequest(
        source=source,
        instrument=instrument,
        timeframe="1d",
        start=date(2026, 1, 1),
        end=date(2026, 1, 1),
    )

    def fake_yfinance_download(*args, **kwargs):
        return pd.DataFrame()

    monkeypatch.setattr("yfinance.download", fake_yfinance_download)

    resp = get_timeseries(req)
    assert resp is None


def test_error_raise(monkeypatch):
    # start date is inclusiv and end date is exclusiv - the range 2024-01-01-2024-01-01 is not possible
    source = DataSource(name="YFinance API", provider_kind="yfinance")
    instrument = Instrument(symbol="EUR - USD", name="EUR/USD", asset_class="fx")
    req = MarketDataRequest(
        source=source,
        instrument=instrument,
        timeframe="1d",
        start=date(2026, 1, 1),
        end=date(2026, 1, 1),
    )

    def fake_yfinance_download():
        raise Exception("fake yfinance error")

    monkeypatch.setattr("yfinance.download", fake_yfinance_download)

    resp = get_timeseries(req)
    assert resp is None
"""
