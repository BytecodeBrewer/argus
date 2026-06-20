import pandas as pd
import pandas.testing as pdt
import numpy as np
from argus.services.timeseries_service import prepare_trend_analysis


def test_is_pct_change_added():
    test_curr = "EURUSD=X"
    test_start = ""
    test_end = ""
    test_interval = "1d"

    expect_result = {
        "date": ["2026-06-01", "2026-06-02", "2026-06-03"],
        "rate": [1.08, 1.1, 1.14],
        "daily_pct_change": [np.nan, 1.85185185185186, 3.6363636363636154],
        "roll_avg": [1.08, 1.09, 1.1066666666666667],
    }
    expect_dict = {
        "min_date": ["2026-06-01"],
        "min_rate": [1.08],
        "max_date": ["2026-06-03"],
        "max_rate": [1.14],
    }
    result = prepare_trend_analysis(test_curr, test_start,test_end,test_interval)
    if result is None:
        return None
    result_df, result_dict = result
    expect_df = pd.DataFrame(expect_result)

    pdt.assert_frame_equal(result_df, expect_df)
    assert result_dict == expect_dict
