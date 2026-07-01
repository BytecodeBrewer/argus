from argus.clients.yfinance_client import get_timeseries
import pandas as pd
import pandas.testing as pdt


def test_get_dataframe(monkeypatch):
    test_resp = pd.DataFrame(
        {
            "Close": [1.105583, 1.103875, 1.094176],
        },
        index=pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]),
    )
    test_resp.index.name = "Date"
    test_curr = "EURUSD=X"
    test_start = "2024-01-01"
    test_end = "2024-01-04"
    test_interval = "1d"

    def fake_yfinance_download(*args, **kwargs):
        return test_resp

    monkeypatch.setattr("yfinance.download", fake_yfinance_download)

    result = get_timeseries(test_curr, test_start, test_end, test_interval)
    expected = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]),
            "rate": [1.105583, 1.103875, 1.094176],
        }
    )
    assert result is not None
    pdt.assert_frame_equal(result, expected)


def test_get_none(monkeypatch):
    test_curr = "EURUSD=X"
    test_start = "2024-01-01"
    test_end = "2024-01-04"
    test_interval = "1d"

    def fake_yfinance_download(*args, **kwargs):
        return None

    monkeypatch.setattr("yfinance.download", fake_yfinance_download)

    result = get_timeseries(test_curr, test_start, test_end, test_interval)
    assert result is None


def test_get_empty_frame(monkeypatch):
    test_curr = "EURUSD=X"
    test_start = "2024-01-01"
    test_end = "2024-01-01"
    test_interval = "1d"

    def fake_yfinance_download(*args, **kwargs):
        return pd.DataFrame()

    monkeypatch.setattr("yfinance.download", fake_yfinance_download)

    result = get_timeseries(test_curr, test_start, test_end, test_interval)
    assert result is None


def test_error_raise(monkeypatch):
    test_curr = "EURUSD=X"
    # start date is inclusiv and end date is exclusiv - the range 2024-01-01-2024-01-01 is not possible
    test_start = "2024-01-04"
    test_end = "2024-01-02"
    test_interval = "1d"

    def fake_yfinance_download(
        tickers=test_curr, start=test_start, end=test_end, interval=test_interval
    ):
        raise Exception("fake yfinance error")

    monkeypatch.setattr("yfinance.download", fake_yfinance_download)

    result = get_timeseries(test_curr, test_start, test_end, test_interval)
    assert result is None
