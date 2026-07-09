import pandas as pd


def add_daily_percentage_change(df: pd.DataFrame) -> pd.DataFrame:
    """
        Add the daily percentage change of the exchange rate.

    Calculates the percentage change between each rate value and the
    previous rate value. The result is added as a new column named
    ``daily_pct_change``.

    Args:
        df (pd.DataFrame): DataFrame containing at least a ``rate`` column.

    Returns:
        pd.DataFrame: A copy of the input DataFrame with an added
        ``daily_pct_change`` column.

    Notes:
        The first row will contain ``NaN`` because there is no previous
        rate value to compare against.
    """
    result = df.copy()
    result["daily_pct_change"] = result["rate"].pct_change() * 100
    return result


def add_rolling_average(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a rolling average of the exchange rate.

    Calculates a rolling mean over the ``rate`` column using a fixed
    window size of 3 rows. The result is added as a new column named
    ``roll_avg``.

    Args:
        df (pd.DataFrame): DataFrame containing at least a ``rate`` column.

    Returns:
        pd.DataFrame: A copy of the input DataFrame with an added
        ``roll_avg`` column.
    """
    result = df.copy()
    result["roll_avg"] = result["rate"].rolling(window=3, min_periods=1).mean()
    return result


def get_min_max_rates(df: pd.DataFrame) -> dict:
    """
    Get the minimum and maximum exchange-rate values.

    Finds the rows with the lowest and highest values in the ``rate``
    column and returns their dates and rates in a dictionary.

    Args:
        df (pd.DataFrame): DataFrame containing at least ``date`` and
            ``rate`` columns.

    Returns:
        dict: Dictionary containing the minimum and maximum rate data with
        the following keys:

            - ``min_date``: Date of the lowest exchange rate.
            - ``min_rate``: Lowest exchange-rate value.
            - ``max_date``: Date of the highest exchange rate.
            - ``max_rate``: Highest exchange-rate value.
    """
    min_max = {"min_date": [], "min_rate": [], "max_date": [], "max_rate": []}
    min_id = df["rate"].idxmin()
    max_id = df["rate"].idxmax()
    min_max["min_date"].append(df.loc[min_id, "date"])
    min_max["min_rate"].append(df.loc[min_id, "rate"])
    min_max["max_date"].append(df.loc[max_id, "date"])
    min_max["max_rate"].append(df.loc[max_id, "rate"])
    return min_max


def get_cumulative_return(df:pd.DataFrame,start_date:str,end_date:str)->float:
    
    if df.empty:
        return 0.0
    start_row=df.loc[df["date"]==start_date]
    end_row=df.loc[df["date"]==end_date]
    
    if start_row.empty or end_row.empty:
        return 0.0

    start_rate=float(start_row["rate"].iloc[0])
    end_rate=float(end_row["rate"].iloc[0])

    if start_rate == 0.0:
        return 0.0

    return (end_rate - start_rate)/start_rate*100

def get_strongest_weakest_days(df: pd.DataFrame, start_date: str, end_date: str) -> dict:
    period_df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
    
    if period_df.empty or len(period_df) < 2:
        return {
            "strongest_day": {"date": None, "pct_change": 0.0},
            "weakest_day": {"date": None, "pct_change": 0.0}
        }
    
    pct_series = pd.Series(period_df["rate"]).pct_change() * 100
    valid_pct = pct_series.dropna()
    
    if valid_pct.empty:
        return {
            "strongest_day": {"date": None, "pct_change": 0.0},
            "weakest_day": {"date": None, "pct_change": 0.0}
        }
        
    max_idx = valid_pct.idxmax()
    min_idx = valid_pct.idxmin()
    
    return {
        "strongest_day": {
            "date": period_df.loc[max_idx, "date"],
            "pct_change": round(float(pct_series.loc[max_idx]), 2)
        },
        "weakest_day": {
            "date": period_df.loc[min_idx, "date"],
            "pct_change": round(float(pct_series.loc[min_idx]), 2)
        }
    }


