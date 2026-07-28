from datetime import date

import pandas as pd
import pytest

from argus.domain.internal_models import DataSource, Instrument, MarketDataResponse


@pytest.fixture
def valid_source():
    return DataSource(name="Yahoo", provider_kind="yfinance_api")


@pytest.fixture
def valid_instrument():
    return Instrument(symbol="AAPL", name="Apple Inc.", asset_class="stock")


def test_market_data_response_accepts_valid_dataframe(
    valid_source, valid_instrument
) -> None:
    valid_bar = {
        "timestamp": [date(2026, 1, 1)],
        "open": [150.0],
        "high": [155.0],
        "low": [149.0],
        "close": [153.5],
        "adjusted_close": [153.5],
        "volume": [1000000.0],
    }
    df = pd.DataFrame(valid_bar)

    resp = MarketDataResponse(
        source=valid_source, instrument=valid_instrument, bars=df, message=""
    )
    assert resp.bars.equals(df)


def test_market_data_response_raises_error_on_missing_columns(
    valid_source, valid_instrument
) -> None:
    incomplete_bar = {
        "timestamp": [date(2026, 1, 1)],
        "close": [153.5],
    }
    df = pd.DataFrame(incomplete_bar)

    with pytest.raises(ValueError) as exc_info:
        MarketDataResponse(
            source=valid_source, instrument=valid_instrument, bars=df, message=""
        )

    assert "Missing required columns" in str(exc_info.value)


def test_market_data_response_raises_error_if_not_a_dataframe(
    valid_source, valid_instrument
) -> None:
    invalid_input = "I'm just a string :D"

    with pytest.raises(TypeError) as exc_info:
        MarketDataResponse(
            source=valid_source,
            instrument=valid_instrument,
            bars=invalid_input,  # type: ignore
        )

    assert "must be a pandas DataFrame" in str(exc_info.value)
