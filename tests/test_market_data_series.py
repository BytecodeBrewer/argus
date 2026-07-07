import pandas as pd
from datetime import date
from argus.services.market_data_service import get_market_data
from argus.storage.database import initialize_database
from argus.domain.internal_models import DataSource, Instrument, MarketDataRequest


def test_get_a_full_timeseries(tmp_path):
    source = DataSource(name="YFinance API", provider_kind="yfinance")
    instrument = Instrument(symbol="EUR - USD", name="EUR/USD", asset_class="fx")
    req = MarketDataRequest(
        source=source,
        instrument=instrument,
        timeframe="1d",
        start=date(2024, 1, 1),
        end=date(2024, 1, 4),
    )
    db = tmp_path / "test.duckdb"

    initialize_database(db)
    result = get_market_data(db, req)

    assert result is not None
    """
    result_df, result_dict = result
    result_df["date"] = result_df["date"].astype("str")
    result_dict["min_date"] = [str(result_dict["min_date"][0])]
    result_dict["max_date"] = [str(result_dict["max_date"][0])]
    expect_df = pd.DataFrame(expect_result)

    pdt.assert_frame_equal(result_df, expect_df)
    assert result_dict == expect_dict
    """
