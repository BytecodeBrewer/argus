import numpy as np
import pandas as pd
import pandas.testing as pdt

from argus.analytics.metrics.trend_metrics import (
    add_daily_percentage_change,
    add_rolling_average,
    get_min_max_rates,
)


def test_is_pct_change_added():
    test_timesseries = {
        "date": ["2026-05-01", "2026-05-02", "2026-05-03"],
        "rate": [1.00, 1.10, 1.21],
    }

    expect_result = {
        "date": ["2026-05-01", "2026-05-02", "2026-05-03"],
        "rate": [1.00, 1.10, 1.21],
        "daily_pct_change": [np.nan, 10.0, 10.0],
    }
    test_df = pd.DataFrame(test_timesseries)
    result_df = add_daily_percentage_change(test_df)
    expect_df = pd.DataFrame(expect_result)

    pdt.assert_frame_equal(result_df, expect_df)


def test_is_roll_avg_added():
    test_timesseries = {
        "date": ["2026-05-01", "2026-05-02", "2026-05-03"],
        "rate": [1.00, 1.10, 1.21],
    }

    expect_result = {
        "date": ["2026-05-01", "2026-05-02", "2026-05-03"],
        "rate": [1.00, 1.10, 1.21],
        "roll_avg": [1.00, 1.05, 1.1033333333333333333333333333333],
    }
    test_df = pd.DataFrame(test_timesseries)
    result_df = add_rolling_average(test_df)
    expect_df = pd.DataFrame(expect_result)

    pdt.assert_frame_equal(result_df, expect_df)


def test_get_min_max_():
    test_timesseries = {
        "date": ["2026-05-01", "2026-05-02", "2026-05-03"],
        "rate": [1.00, 1.10, 1.21],
    }

    min_max = {
        "min_date": ["2026-05-01"],
        "min_rate": [1.00],
        "max_date": ["2026-05-03"],
        "max_rate": [1.21],
    }
    test_df = pd.DataFrame(test_timesseries)
    result_dict = get_min_max_rates(test_df)

    assert result_dict == min_max
