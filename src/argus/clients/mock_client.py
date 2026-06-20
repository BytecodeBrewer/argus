import numpy as np

mock_resp_data = {
    "date": [
        "2026-06-01",
        "2026-06-02",
        "2026-06-03",
        "2026-06-04",
        "2026-06-05",
        "2026-06-06",
        "2026-06-07",
        "2026-06-08",
        "2026-06-09",
        "2026-06-10",
        "2026-06-11",
        "2026-06-12",
        "2026-06-13",
        "2026-06-14",
        "2026-06-15",
    ],
    "rate": [
        1.08,
        1.10,
        1.14,
        1.12,
        1.10,
        1.07,
        1.08,
        1.08,
        1.08,
        1.10,
        1.12,
        1.12,
        1.15,
        1.12,
        1.13,
    ],
}


def get_mock_timeseries(curr: str, date: str) -> int | float:
    if curr == "USD":
        index = mock_resp_data["date"].index(date)
        rate = mock_resp_data["rate"][index]
        return rate
    else:
        return np.nan
