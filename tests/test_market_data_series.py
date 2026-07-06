import pandas as pd
import pandas.testing as pdt
import numpy as np
from datetime import date
from argus.services.market_data_service import get_market_data
from argus.storage.database import initialize_database
from argus.domain.internal_models import DataSource,Instrument,MarketDataSet


def test_get_a_full_timeseries(tmp_path):
    source = DataSource(name="YFinance API",provider_kind="yfinance")
    instrument = Instrument(symbol="EUR - USD",name="EUR/USD",asset_class="fx")
    market_data = MarketDataSet(
    source=source,
    instrument=instrument,
    timeframe="1d",
    start=date(2024, 1, 1),
    end=date(2024, 1, 4),
    bars=pd.DataFrame(),
)
    db = tmp_path / "test.duckdb"
    expect_result = {
        "date": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "rate": [1.1055831909179688, 1.1038745641708374, 1.0941756963729858],
        "daily_pct_change": [np.nan, -0.1545452898675692, -0.8786204622023064],
        "roll_avg": [1.1055831909179688, 1.104728877544403, 1.101211150487264],
    }
    expect_dict = {
        "min_date": ["2024-01-03 00:00:00"],
        "min_rate": [1.0941756963729858],
        "max_date": ["2024-01-01 00:00:00"],
        "max_rate": [1.1055831909179688],
    }
    initialize_database(db)
    result = get_market_data(db=db,market_data=market_data)

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
