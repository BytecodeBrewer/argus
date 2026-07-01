# Research: First Forecasting Approach for Market Time Series

## 1. Realistic First Prediction Task for ARGUS

A realistic first prediction task for ARGUS is **next-day exchange-rate movement** or **trend direction**. Predicting the exact next value (point forecast) is generally much harder and often less useful for trading/signal workflows than predicting the direction of the movement (up/down). A directional classification task serves as a simple, actionable signal for basic workflows.

## 2. Baseline Methods to Implement First

Before jumping into complex models, the following baselines should be implemented to evaluate the added value of any machine learning model:

- **Naive last-value forecast**: The prediction for the next period is exactly the value from the current period. This is surprisingly hard to beat in random walk-like financial time series.
- **Moving average forecast**: A simple rolling average to predict the next value or determine trend direction.
- **Simple linear regression**: To capture basic linear trends over a given historical window.

## 3. Libraries: NumPy, pandas, or scikit-learn?

The first implementation should use **pandas** and **scikit-learn**:

- **pandas**: Excellent for time-series manipulation, rolling windows, lagging features, and handling missing data.
- **scikit-learn**: Offers robust implementations of simple models (e.g., Linear Regression, Logistic Regression for direction) and provides standardized metrics and cross-validation tools designed for time series (e.g., `TimeSeriesSplit`).

## 4. Evaluation Metrics

For the initial approaches, we should focus on:

- **Directional accuracy**: The percentage of times the model correctly predicts the direction of the price movement (up vs down). This is often more relevant than magnitude errors.
- **MAE (Mean Absolute Error)**: If point forecasting is used, MAE is more robust to outliers than RMSE and provides a linear penalty for errors.
- **RMSE (Root Mean Squared Error)**: Useful to penalize larger errors more heavily, but should be secondary to directional accuracy for basic signal generation.

## 5. Why is LSTM not the first implementation step?

LSTMs are highly complex, require a large amount of well-structured data to train effectively without overfitting, and are notoriously difficult to tune. For financial time series, which suffer from low signal-to-noise ratios, an LSTM is likely to overfit the training data or collapse to predicting the last known value. Starting with an LSTM obscures whether the underlying data has any predictive power and sets a high barrier for debugging and infrastructure.

## 6. Prerequisites for an LSTM Ticket

Before considering LSTMs or other deep learning approaches, the following must be established:

- A reliable data ingestion and preprocessing pipeline.
- Established baseline performance metrics (e.g., a naive model and a linear regression model) to compare against.
- Sufficient historical data size.
- A robust backtesting and cross-validation framework to ensure the LSTM isn't just memorizing data or overfitting.
- Hardware/infrastructure to support longer training times and hyperparameter tuning.

## 7. Recommended First Implementation Approach

**Recommendation**: Start with **directional trend prediction** (predicting whether the next value is higher or lower than the current value) using a simple **Logistic Regression** model via **scikit-learn**.

- Use **pandas** to create basic lagged features (e.g., previous returns, moving averages).
- Evaluate using **directional accuracy**.
- Compare performance strictly against a **naive momentum** (predicting the trend continues) or **majority-class** baseline.
