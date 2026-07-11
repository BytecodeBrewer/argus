import pandas as pd
import pandas.testing as pdt
import numpy as np
import pytest
from argus.analytics.metrics.trend_metrics import (
    add_daily_percentage_change,
    add_rolling_average,
    get_min_max_rates,
    get_cumulative_return,
    get_strongest_weakest_days,
    add_rolling_volatility,
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


def test_get_cumulative_return():
    test_timesseries = {
        "date": ["2026-05-01", "2026-05-02", "2026-05-03"],
        "rate": [1.00, 1.10, 1.21],
    }
    test_df = pd.DataFrame(test_timesseries)
    resault = get_cumulative_return(test_df)
    assert resault == pytest.approx(21.0)

    # Egde case
    empty_df = pd.DataFrame(columns=["date", "rate"])
    result = get_cumulative_return(empty_df)
    assert result == 0.0


def test_get_strongest_weakest_days():
    test_timeseries = {
        "date": ["2026-05-01", "2026-05-02", "2026-05-03", "2026-05-04"],
        "rate": [1.00, 1.20, 1.14, 2.00],
    }
    test_df = pd.DataFrame(test_timeseries)

    result = get_strongest_weakest_days(test_df)

    assert result == {
        "strongest_day": {"date": "2026-05-04", "pct_change": 75.44},
        "weakest_day": {"date": "2026-05-03", "pct_change": -5.0},
    }

    # Edge case
    flat_timeseries = {
        "date": ["2026-05-01", "2026-05-02", "2026-05-03"],
        "rate": [1.15, 1.15, 1.15],
    }
    flat_df = pd.DataFrame(flat_timeseries)
    result = get_strongest_weakest_days(flat_df)
    assert result == {
        "strongest_day": {"date": "2026-05-02", "pct_change": 0.0},
        "weakest_day": {"date": "2026-05-02", "pct_change": 0.0},
    }


def test_is_rolling_volatility_added():
    test_timeseries = {
        "date": ["2026-05-01", "2026-05-02", "2026-05-03"],
        "rate": [1.00, 2.00, 1.00],
    }
    test_df = pd.DataFrame(test_timeseries)

    expect_result = {
        "date": ["2026-05-01", "2026-05-02", "2026-05-03"],
        "rate": [1.00, 2.00, 1.00],
        "rolling_volatility": [0.0, 0.0, 106.06601717798213],
    }
    expect_df = pd.DataFrame(expect_result)
    result_df = add_rolling_volatility(test_df, window=2)

    pdt.assert_frame_equal(result_df, expect_df)
