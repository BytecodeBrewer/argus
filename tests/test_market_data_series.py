import pytest
import pandas as pd
from datetime import date
from unittest.mock import Mock
from argus.domain.internal_models import (
    DataSource,
    Instrument,
    MarketDataRequest,
    MarketDataResponse,
)
from argus.services.market_data_service import get_market_data


@pytest.fixture
def sample_source():
    return DataSource(name="Yahoo", provider_kind="yfinance_api")


@pytest.fixture
def sample_instrument():
    return Instrument(symbol="AAPL", name="Apple Inc.", asset_class="stock")


@pytest.fixture
def sample_response(sample_source, sample_instrument):
    test_bar = {
        "timestamp": date(2026, 1, 1),
        "open": None,
        "high": None,
        "low": None,
        "close": 1.89,
        "adjusted_close": None,
        "volume": None,
    }
    return MarketDataResponse(
        source=sample_source,
        instrument=sample_instrument,
        bars=pd.DataFrame(test_bar, index=[0]),
    )


def test_get_market_data_storage_hit(
    monkeypatch, sample_source, sample_instrument, sample_response
):
    req = MarketDataRequest(
        source=sample_source,
        instrument=sample_instrument,
        timeframe="1d",
        start=date(2026, 1, 1),
        end=date(2026, 1, 1),
    )

    monkeypatch.setattr(
        "argus.services.market_data_service.read_price_bars",
        lambda db, r: sample_response.bars,
    )

    mock_get_timeseries = Mock()
    monkeypatch.setattr(
        "argus.services.market_data_service.get_timeseries", mock_get_timeseries
    )

    res = get_market_data("mock_db_path", req)

    assert res is not None
    assert not res.bars.empty
    mock_get_timeseries.assert_not_called()


def test_get_market_data_storage_miss(
    monkeypatch, sample_source, sample_instrument, sample_response
):
    req = MarketDataRequest(
        source=sample_source,
        instrument=sample_instrument,
        timeframe="1d",
        start=date(2026, 1, 1),
        end=date(2026, 1, 1),
    )

    monkeypatch.setattr(
        "argus.services.market_data_service.read_price_bars",
        lambda db, r: pd.DataFrame(),
    )
    monkeypatch.setattr(
        "argus.services.market_data_service.get_timeseries",
        lambda r: sample_response.bars,
    )

    mock_insert = Mock()
    monkeypatch.setattr(
        "argus.services.market_data_service.insert_price_bar", mock_insert
    )

    res = get_market_data("mock_db_path", req)

    assert res is not None
    mock_insert.assert_called_once()


def test_get_market_data_handles_client_exceptions(
    monkeypatch, sample_source, sample_instrument
):
    req = MarketDataRequest(
        source=sample_source,
        instrument=sample_instrument,
        timeframe="1d",
        start=date(2026, 1, 1),
        end=date(2026, 1, 1),
    )

    monkeypatch.setattr(
        "argus.services.market_data_service.read_price_bars",
        lambda db, r: pd.DataFrame(),
    )

    def mock_value_error(request):
        raise ValueError("Quote not found or no data available for symbol")

    monkeypatch.setattr(
        "argus.services.market_data_service.get_timeseries", mock_value_error
    )

    res_val = get_market_data("mock_db_path", req)
    assert res_val.bars.empty
    assert res_val.message == "Quote not found or no data available for symbol"

    # Fall 2: ConnectionError testen (z.B. Internet weg)
    def mock_connection_error(request):
        raise ConnectionError("Network error or connection timeout")

    monkeypatch.setattr(
        "argus.services.market_data_service.get_timeseries", mock_connection_error
    )

    res_conn = get_market_data("mock_db_path", req)
    assert res_conn.bars.empty
    assert res_conn.message == "Network error or connection timeout"
