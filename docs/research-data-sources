# ARGUS Data Source Research

## Goal

Research and choose a real data source for ARGUS analytics.

ARGUS should evolve from a simple FX converter into a broader market analysis tool.

The first real data source should replace the mock time-series client and provide useful historical data for beginner-friendly analytics.

The selected source should be:

* free or usable without relevant cost
* easy to integrate in Python
* pandas-friendly
* useful for historical analysis
* suitable for future market analytics
* not limited to pure experimentation if the project becomes more serious later

---

## Why

ARGUS currently uses mock time-series data for early analytics development.

Sprint 2 needs a real data client so market metrics can be calculated from real data.

The existing ExchangeRate API client was useful for the first live currency conversion feature, but ARGUS now needs stronger historical data support.

The project should not become a pure FX trading tool.

FX data is a useful entry point because it is simpler than stock analysis:

* exchange-rate data is easier to model
* fewer external fundamentals are needed
* one clean time series is enough for first analytics
* beginner-friendly metrics can be implemented quickly

However, the long-term direction is broader market analysis:

* stocks
* ETFs
* indices
* currencies
* simple trading-oriented insights
* paper trading
* later possible commercial usage if data licensing allows it

---

## Compared Data Sources

| Source | Best Use Case | Free / Cost | API Key | Python / pandas Fit | Commercial Suitability | Fit for ARGUS |
|---|---|---:|---:|---|---|---|
| Frankfurter | Historical FX data | Free | No | Good | Better than unofficial sources, open-source/self-hostable | Very good first client |
| yfinance | Broad market data for research | Free | No | Excellent | Limited / check Yahoo terms | Very good later client |
| ExchangeRate API | Live currency conversion | Free tier / paid tiers | Yes / depends on endpoint | Okay | Depends on plan and terms | Legacy / live conversion only |
| FRED API | Macroeconomic context data | Free | Yes | Good | Possible, but series-specific rights must be checked | Good later macro context client |
| Alpha Vantage | Stocks, FX, crypto, indicators | Free tier + paid | Yes | Good | More API-like, paid plans available | Possible later |
| Twelve Data | Stocks, FX, ETFs, crypto, indices | Free tier + paid | Yes | Good | More suitable for serious API usage | Possible later |

---

## Current ExchangeRate API

### What it is

The current ExchangeRate API client is useful for live currency conversion.

It fits the original project stage:

* enter an amount
* select source currency
* select target currency
* receive converted result

### Strengths

* Already integrated
* Simple for live conversion
* Good for the original FX converter use case
* Easy to understand

### Limitations

* Not ideal as the main historical analytics source
* Historical data support is not the strongest free path for this project
* Less useful once ARGUS moves toward market analytics
* Adds less long-term value if Frankfurter covers FX better

### ARGUS Fit

The ExchangeRate API should not be the strategic core client anymore.

It can remain temporarily as:

* legacy live conversion client
* fallback client
* comparison point during migration

Long term, it can probably be removed if Frankfurter covers all required FX use cases.

---

## Frankfurter

### What it is

Frankfurter is a free and open-source exchange-rate API.

It provides current and historical exchange-rate data and does not require an API key.

### Strengths

* Free
* No API key required
* Simple REST API
* Historical FX data
* Time-series data
* JSON response format
* Easy to transform into pandas DataFrames
* Good fit for beginner-friendly analytics
* Can replace mock FX time-series data directly
* Can also replace parts of the current ExchangeRate API later

### Limitations

* Focused on exchange rates
* Not a broad market-data API
* Does not cover stocks, ETFs or company fundamentals
* Not enough for long-term stock or portfolio analysis alone

### ARGUS Fit

Frankfurter is the best first real data client for Sprint 2.

It solves the immediate problem:

* replace mock time-series data
* fetch real historical exchange-rate data
* calculate the first real analytics metrics
* keep the implementation beginner-friendly
* avoid unnecessary complexity from stock-market data too early

FX data is a useful entry point because it is simpler than stock analysis.

However, ARGUS should not stay limited to FX trading.

The long-term direction is broader market analysis for normal users:

* stocks
* ETFs
* indices
* currencies
* watchlists
* basic market insights
* paper trading
* later possible commercial usage if data licensing allows it

---

## yfinance

### What it is

yfinance is a Python library for downloading market data from Yahoo Finance.

It is useful for stocks, ETFs, indices and some FX symbols.

### Strengths

* Very easy to use in Python
* Excellent pandas compatibility
* Supports broader market data than Frankfurter
* Good for stocks, ETFs and indices
* Useful for future market analysis
* Useful for later signal generation and ML experiments

### Limitations

* Not an official Yahoo Finance API
* Intended mainly for research and educational use
* Commercial usage requires checking Yahoo terms
* Data availability depends on Yahoo symbols
* Less predictable than a dedicated paid market-data API
* Not ideal as the first serious commercial data backbone

### ARGUS Fit

yfinance is a very good later client.

It should be introduced when ARGUS moves from FX-based analytics toward broader market analysis.

It is especially useful for:

* stocks
* ETFs
* indices
* market comparisons
* watchlists
* signal experiments
* ML features
* paper trading prototypes

However, yfinance should not be the first mock-client replacement if the immediate Sprint 2 goal is clean historical FX analytics.

---

## FRED API

### What it is

FRED is the Federal Reserve Economic Data API from the Federal Reserve Bank of St. Louis.

It provides access to economic and macroeconomic time series such as:

* interest rates
* inflation indicators
* unemployment data
* GDP-related data
* yield curves
* recession indicators
* money supply
* economic sentiment and macro context data

FRED is not mainly a market-price API.

It should not replace Frankfurter or yfinance as the main historical price-data client.

Instead, FRED is useful as a macroeconomic context source for ARGUS.

### Strengths

* Very relevant for macroeconomic analysis
* Strong fit for market context
* Useful for explaining why markets may move
* Provides historical economic time series
* Good for dashboards, reports and later signal context
* Can support more serious market analysis than pure price charts

### Limitations

* Requires an API key
* Not a stock, ETF or FX price-data provider
* Some series may be owned by third parties
* Copyrighted series may require additional permission for non-personal or commercial use
* Commercial usage needs careful checking per data series
* Not ideal as the first replacement for the mock time-series client

### ARGUS Fit

FRED is a strong future addition for ARGUS.

It becomes valuable when ARGUS starts connecting market movements with economic conditions.

FRED can help ARGUS answer questions like:

* Are interest rates rising or falling?
* Is inflation cooling down?
* Is the yield curve inverted?
* Is the macro environment risky?
* Could market weakness be connected to macro conditions?

This makes FRED useful for analysis and reporting, but not as the first Sprint 2 data client.

---

## Alpha Vantage

### What it is

Alpha Vantage is a financial data API for stocks, FX, crypto, commodities, indicators and more.

### Strengths

* Official API-style access
* Supports many market data types
* Has documentation for many endpoints
* More suitable than yfinance if the project later needs a more formal API provider
* Could support more serious long-term data workflows

### Limitations

* Requires API key
* Free tier is limited
* Request limits can become annoying for analytics workflows
* More setup than Frankfurter or yfinance
* Some advanced or real-time features require paid plans

### ARGUS Fit

Alpha Vantage is not recommended as the first Sprint 2 client.

It is worth revisiting later if ARGUS needs:

* more formal market-data API access
* indicators
* broader asset coverage
* a clearer path toward commercial or semi-commercial use

---

## Twelve Data

### What it is

Twelve Data is a financial market data API covering stocks, forex, ETFs, indices, crypto and more.

### Strengths

* Broad market coverage
* API-first design
* Supports JSON and other formats
* Has SDK support
* Better long-term candidate than unofficial data sources
* More suitable for serious market-data workflows

### Limitations

* Requires API key
* Free tier limitations apply
* More platform dependency
* More setup than Frankfurter
* Probably too much for the first Sprint 2 step

### ARGUS Fit

Twelve Data is interesting for later.

It may become relevant when ARGUS moves toward:

* broader market analysis
* paper trading
* more reliable stock/ETF data
* possible commercial use
* serious dashboard or monitoring workflows

It should not be the first implementation choice because Frankfurter is simpler for the current phase.

---

## Commercial Usage Consideration

ARGUS should avoid locking itself into data sources that are only useful for experiments if the project may later become more serious.

Current interpretation:

| Source | Commercial Direction |
|---|---|
| Frankfurter | Best first choice; open-source/self-hostable, but source and data terms should still be checked before commercial use |
| yfinance | Great for learning and research, but not ideal for commercial use without checking Yahoo terms |
| ExchangeRate API | Commercial use depends on API plan and terms |
| FRED API | Useful for macro context, but series-specific rights must be checked |
| Alpha Vantage | More realistic commercial path through paid plans |
| Twelve Data | More realistic commercial path through paid plans |

---

## Final Portfolio Decision

Frankfurter should still be selected as the first real data source for Sprint 2.

Reason:

* It directly replaces the mock time-series client.
* It provides clean historical exchange-rate data.
* It keeps the first analytics implementation manageable.
* It is simple, free and beginner-friendly.

yfinance should be added later when ARGUS moves toward broader market analysis:

* stocks
* ETFs
* indices
* watchlists
* simple signals
* paper trading prototypes

FRED should be added as a macro context client, not as the first historical price-data client.

It becomes valuable when ARGUS starts connecting market movements with economic conditions.

Alpha Vantage or Twelve Data should be evaluated later if ARGUS needs a more serious or commercial-friendly market-data provider.

```text
Sprint 2:
Frankfurter
→ real historical FX data
→ replaces mock time-series data

Later:
yfinance
→ broader market data
→ stocks, ETFs, indices, paper trading prototypes

FRED
→ macroeconomic context
→ inflation, rates, unemployment, GDP, yield curve

Future:
Alpha Vantage or Twelve Data
→ more serious market-data provider
→ better candidate for commercial or production-like use
```

---

## Out of Scope for This Ticket

This research focuses on data sources for analytics.

The following topics should be handled in later research tickets:

| Topic | Reason |
|---|---|
| Alpaca | Broker, paper trading and execution API; relevant later, but not first data-source replacement |
| CCXT exchanges | Crypto exchange connector layer; useful later for crypto workflows |
| Broker integrations | Belong to paper trading / execution research |

