import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def create_lin_regression(df: pd.DataFrame) -> np.ndarray:
    raw_data = df.copy()
    conv_data = convert_date_to_acc(raw_data)
    x = conv_data[["days_since_start"]]
    y = conv_data[["close"]]

    model = LinearRegression()
    model.fit(x,y)
    result = model.predict(x)
    return result

def convert_date_to_acc(df: pd.DataFrame):
    result = df.copy()
    result = result.drop(columns=["date"])
    result["days_since_start"] = range(len(result))
    return result
