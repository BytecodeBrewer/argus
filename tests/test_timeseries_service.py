import pandas as pd
import pandas.testing as pdt
import numpy as np
from argus.services.timeseries_service import prepare_trend_analysis


def test_is_pct_change_added():
    test_curr = "USD"
    test_dates = {
        "date": ["2026-06-01", "2026-06-02", "2026-06-03"],
    }
    test_dates = pd.DataFrame(test_dates)

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
    result_df, result_dict = prepare_trend_analysis(test_curr, test_dates)
    expect_df = pd.DataFrame(expect_result)

    pdt.assert_frame_equal(result_df, expect_df)
    assert result_dict == expect_dict
