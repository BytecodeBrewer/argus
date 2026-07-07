from argus.clients.yfinance_client import get_timeseries
from argus.domain.internal_models import DataSource, Instrument, MarketDataRequest
from datetime import date
import pytest
import pandas as pd
import pandas.testing as pdt


@pytest.fixture
def sample_source():
    return DataSource(
        name="Yahoo", provider_kind="yfinance_api", requires_api_key=False
    )


@pytest.fixture
def sample_instrument():
    return Instrument(
        symbol="EUR/USD",
        name="EUR - USD Rate",
        asset_class="fx",
        base_currency="EUR",
        quote_currency="USD",
    )


def test_get_dataframe(monkeypatch, sample_source, sample_instrument):
    test_resp = pd.DataFrame(
        {
            "Open": [None, None, None],
            "High": [None, None, None],
            "Low": [None, None, None],
            "Close": [1.105583, 1.103875, 1.094176],
            "Adj Close": [None, None, None],
            "Volume": [None, None, None],
        },
        index=pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]),
    )
    test_resp.index.name = "Date"
    req = MarketDataRequest(
        source=sample_source,
        instrument=sample_instrument,
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
            "timestamp": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]),
            "open": [None, None, None],
            "high": [None, None, None],
            "low": [None, None, None],
            "close": [1.105583, 1.103875, 1.094176],
            "adjusted_close": [None, None, None],
            "volume": [None, None, None],
        }
    )

    assert resp is not None
    pdt.assert_frame_equal(resp, expected)


def test_client_network_error(monkeypatch, sample_source, sample_instrument):
    req = MarketDataRequest(
        source=sample_source,
        instrument=sample_instrument,
        timeframe="1d",
        start=date(2024, 1, 1),
        end=date(2024, 1, 4),
    )

    def mock_crash(*args, **kwargs):
        raise Exception()

    monkeypatch.setattr("yfinance.download", mock_crash)

    with pytest.raises(ConnectionError, match="Network error or connection timeout"):
        get_timeseries(req)


def test_client_invalid_response(monkeypatch, sample_source, sample_instrument):
    req = MarketDataRequest(
        source=sample_source,
        instrument=sample_instrument,
        timeframe="1d",
        start=date(2024, 1, 1),
        end=date(2024, 1, 4),
    )

    monkeypatch.setattr("yfinance.download", lambda *args, **kwargs: None)

    with pytest.raises(
        ConnectionError, match="Yahoo Finance API returned an invalid response"
    ):
        get_timeseries(req)


def test_client_quote_not_found(monkeypatch, sample_source, sample_instrument):
    req = MarketDataRequest(
        source=sample_source,
        instrument=sample_instrument,
        timeframe="1d",
        start=date(2024, 1, 1),
        end=date(2024, 1, 4),
    )

    monkeypatch.setattr("yfinance.download", lambda *args, **kwargs: pd.DataFrame())

    with pytest.raises(
        ValueError, match="Quote not found or no data available for symbol"
    ):
        get_timeseries(req)
