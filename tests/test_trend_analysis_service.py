import pytest
import pandas as pd
from datetime import date
from matplotlib.figure import Figure
from argus.domain.internal_models import (
    DataSource,
    Instrument,
    MarketDataRequest,
    MarketDataResponse,
)
from argus.services.trend_analysis_service import prepare_trend_analysis
from argus.services.market_data_service import get_market_data
from argus.storage.database import initialize_database

"""
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


@pytest.fixture
def sample_response(sample_source, sample_instrument):
    test_bar = {
        "timestamp": [date(2024, 1, 1), date(2024, 1, 2), date(2024, 1, 3)],
        "open": [None, None, None],
        "high": [None, None, None],
        "low": [None, None, None],
        "close": [1.10, 1.12, 1.11],
        "adjusted_close": [None, None, None],
        "volume": [None, None, None],
    }
    return MarketDataResponse(
        source=sample_source, instrument=sample_instrument, bars=pd.DataFrame(test_bar)
    )


def test_prepare_trend_analysis_success(
    sample_source, sample_instrument, sample_response, monkeypatch
):
    req = MarketDataRequest(
        source=sample_source,
        instrument=sample_instrument,
        timeframe="1d",
        start=date(2024, 1, 1),
        end=date(2024, 1, 4),
    )

    monkeypatch.setattr(
        "argus.services.trend_analysis_service.get_market_data",
        lambda db, r: sample_response,
    )

    res = prepare_trend_analysis("mock_db_path", req)
    assert isinstance(res, Figure)


def test_prepare_trend_analysis_failure(sample_source, sample_instrument, monkeypatch):
    req = MarketDataRequest(
        source=sample_source,
        instrument=sample_instrument,
        timeframe="1d",
        start=date(2024, 1, 1),
        end=date(2024, 1, 4),
    )

    error_response = MarketDataResponse(
        source=sample_source,
        instrument=sample_instrument,
        bars=pd.DataFrame(),
        message="Quote not found or no data available for symbol",
    )

    monkeypatch.setattr(
        "argus.services.trend_analysis_service.get_market_data",
        lambda db, r: error_response,
    )

    res = prepare_trend_analysis("mock_db_path", req)
    assert isinstance(res, str)
    assert res == "Quote not found or no data available for symbol"
"""
