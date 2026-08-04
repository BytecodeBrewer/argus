import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def create_lin_regression(df: pd.DataFrame) -> np.ndarray:
    raw_data = df.copy()

    X = np.array(raw_data)
    y = np.dot(X, np.array([1.21, 1.56])) + 2

    reg = LinearRegression().fit(X, y)
    result = reg.predict(np.array([[1.34, 1.45]]))
    return result
