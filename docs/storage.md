# ARGUS Storage Layer

ARGUS uses DuckDB as the local storage layer for normalized market data.

The storage layer stores ARGUS-internal market data structures and provides reusable historical data for analytics, charts, dashboards and reports.

The storage design follows the direction described in [`docs/research-databases-and-storage.md`](research-databases-and-storage.md).

## Storage Workflow

ARGUS uses a storage-first workflow for historical market data.

```text
User / GUI / Analytics request
        ↓
Market data service
        ↓
Check DuckDB storage
        ↓
If data exists:
    read stored data
    return it for analytics, charts or reports

If data is missing:
    fetch data from a client/API
    normalize the response into ARGUS-internal data
    return the normalized data
    save the normalized data in DuckDB
```

DuckDB is used to avoid unnecessary repeated API calls and to make historical market data reusable across analytics, dashboard and reporting workflows.

Fresh API data can be used immediately after normalization and is also persisted so future requests can use the local storage layer first.

## Schema Overview

The first storage schema is based on three related entities:

```text
data_sources
instruments
price_bars
```

### `data_sources`

Stores where market data came from.

Examples:

```text
yfinance
ExchangeRate API
Frankfurter
FRED
```

Each source describes a provider or API that can deliver market, FX or macro data.

### `instruments`

Stores what ARGUS can analyze.

Examples:

```text
EUR/USD
AAPL
SPY
BTC-USD
```

An instrument represents the internal ARGUS identity of an asset, currency pair, ETF, index or other market object.

Provider-specific symbols should be normalized before storage. For example:

```text
yfinance provider symbol: EURUSD=X
ARGUS instrument symbol: EUR/USD
```

### `price_bars`

Stores historical time-series values in an OHLCV-ready structure.

A price bar belongs to:

```text
one data source
one instrument
one timestamp
one timeframe
```

FX rates are stored as `close` values.

For simple FX data, the remaining OHLCV fields can stay empty. For broader market data, the same structure can store open, high, low, close, adjusted close and volume values.

The combination of source, instrument, timestamp and timeframe identifies a unique stored price bar.

## Internal Models and Storage

ARGUS uses internal domain models before data is stored:

```text
DataSource
Instrument
PriceBar
```

These models describe the meaning of the data inside ARGUS.

The storage layer translates these internal models into DuckDB tables:

```text
DataSource  -> data_sources
Instrument  -> instruments
PriceBar    -> price_bars
```

In Python, a `PriceBar` references a `DataSource` and an `Instrument`.

In DuckDB, this relationship is stored through IDs:

```text
price_bars.source_id     -> data_sources.id
price_bars.instrument_id -> instruments.id
```

This keeps the database normalized while still allowing ARGUS to work with meaningful internal models in Python.

## Reading Stored Data

Stored price bars can be read by:

```text
source
instrument
start date
end date
```

The storage layer joins `price_bars`, `data_sources` and `instruments` so that stored IDs become readable market data again.

Read operations return tabular data that can be used by:

```text
analytics
charts
dashboards
reports
```

This allows ARGUS to process stored historical data without depending on raw API response structures.
