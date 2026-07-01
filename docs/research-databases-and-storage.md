# ARGUS Storage Research

## Goal

Research what ARGUS should store and which database/storage approach fits the project.

ARGUS is moving from live API requests and in-memory analytics toward real data workflows.  
The first storage decision should support local market analytics, SQL practice and future dashboard features without adding unnecessary infrastructure too early.

---

## Storage Use Cases

ARGUS should eventually store different kinds of data, but not all of them need to be implemented at once.

Relevant storage use cases are:

* historical exchange rates
* cleaned historical market data
* source information
* instruments that ARGUS can analyze
* later watchlists
* later generated reports
* later macroeconomic data
* later paper-trading history

The first implementation should focus on historical market data and the basic entities needed to query it.

---

## Storage Candidates

ARGUS should compare storage options based on the current project phase.

The project currently needs local analytical storage, not a full server or cloud database.

### DuckDB

DuckDB is a local analytical database.

It is a strong fit for ARGUS because it supports SQL-based analytics without requiring a database server.

Useful for:

* historical market data
* local time-series analysis
* SQL practice
* Python-based analytics
* notebook-based exploration
* dashboard data preparation

Limitations:

* not a server database
* less suitable for multi-user product features later

---

### SQLite

SQLite is a simple local database.

It is strong for small app storage and simple persistence.

Useful for:

* settings
* small app-state data
* simple local tables
* later watchlists
* lightweight metadata

Limitations:

* less analytics-focused than DuckDB
* not ideal as the main storage layer for historical market data
* better for app-state than analytical time-series queries

---

### PostgreSQL

PostgreSQL is a server-based relational database.

It is a strong long-term option when ARGUS becomes more product-like.

Useful for:

* server-based storage
* user-facing features
* report history
* watchlists
* paper-trading history
* richer metadata
* cloud-ready architecture
* SQLGate usage later

Limitations:

* more setup than needed right now
* requires server or Docker setup
* adds infrastructure complexity too early

Fit for ARGUS:

PostgreSQL should be introduced later when ARGUS moves toward a server-based or cloud-ready architecture.

---

## Local, Server and Cloud Options

| Option | Meaning | Fit Now | Fit Later |
| --- | --- | ---: | ---: |
| Local storage | Database runs locally inside or next to the project | High | High |
| Server database | Database runs as a separate service, for example PostgreSQL | Medium | High |
| Cloud storage/database | Managed storage or database in the cloud | Low | High |

ARGUS should start with local storage.

Reason:

* simpler setup
* easier learning curve
* good fit for a Python analytics project
* no cloud or server infrastructure required yet
* enough for historical data, metrics and dashboard development

Server and cloud storage should come later when ARGUS has stronger product features such as reports, user state, paper-trading history or deployment needs.

---

## Recommended First Storage Approach

DuckDB should be the first storage technology for ARGUS.

Reason:

* ARGUS currently needs local analytical storage, not a full server database
* DuckDB fits historical time-series analysis well
* it supports SQL-based analytics without requiring a database server
* it works well with Python and notebook-based exploration
* it keeps the first storage implementation manageable
* it can later be replaced or complemented by PostgreSQL if ARGUS becomes more product-like

The first storage implementation should focus on:

* historical market data
* cleaned OHLCV-ready price data
* source information
* instruments that ARGUS can analyze

PostgreSQL and SQLGate become more relevant later.

For the first DuckDB phase, the goal is to build a clean local analytics workflow.

---

## Developer Interaction Workflow

ARGUS should use a practical developer workflow for DuckDB.

The goal is to make the database easy to inspect, explore and validate before logic is moved into production code.

### Notebook Exploration

Notebooks should be the main exploration layer.

They are useful for:

* opening the DuckDB database
* testing SQL queries
* validating imported data
* comparing SQL results with pandas calculations
* exploring metric logic
* documenting research assumptions

This workflow is especially useful before turning queries into reusable project code.

Notebook exploration should be preferred over a GUI database tool in the first phase.

### DuckDB CLI

The DuckDB CLI should be used for quick database inspection.

It is useful for:

* checking available tables
* running small SQL queries
* validating stored records
* debugging the local database file

The CLI is not the main research environment, but it is useful as a fast inspection tool.

A GUI tool such as DBeaver can be tested if needed, but it should stay optional.

---

## First Data Model Direction

The first data model should support FX data now and broader market data later.

ARGUS should not use a narrow `date | value` table as the main market-data model.

That would work for simple exchange rates, but it would become limiting once ARGUS adds stocks, ETFs, indices or broader market APIs.

The first model should focus on three related entities:

```text
data_sources
instruments
price_bars
```

> [!NOTE]
> The fields below describe the future database-oriented structure.
> Technical fields such as `id`, `instrument_id`, `source_id`, `created_at` and `updated_at` are expected to appear in the database layer.
> Internal Python models may reference related objects directly, for example `source` and `instrument`, before database IDs exist.

### data_sources

Stores where data came from.

Recommended first database fields:

```text
id
name
provider_kind
requires_api_key
created_at
updated_at
```

Example internal/source records:

| name             | provider_kind | requires_api_key |
| ---------------- | ------------- | ---------------: |
| ExchangeRate API | fx_rates      |             true |
| yfinance         | market_prices |            false |
| FRED             | macro_data    |             true |

### instruments

Stores what ARGUS can analyze.

Examples:

* EUR/USD
* AAPL
* SPY
* S&P 500
* BTC-USD

Recommended first database fields:

```text
id
symbol
name
asset_class
currency
exchange
base_currency
quote_currency
created_at
updated_at
```

Example instrument records:

| symbol  | name             | asset_class | currency | exchange  | base_currency | quote_currency |
| ------- | ---------------- | ----------- | -------- | --------- | ------------- | -------------- |
| EUR/USD | Euro / US Dollar | fx          | null     | null      | EUR           | USD            |
| AAPL    | Apple Inc.       | stock       | USD      | NASDAQ    | null          | null           |
| SPY     | SPDR S&P 500 ETF | etf         | USD      | NYSE Arca | null          | null           |

### price_bars

Stores historical market data in an OHLCV-ready structure.

Recommended first database fields:

```text
id
instrument_id
source_id
timestamp
timeframe
open
high
low
close
adjusted_close
volume
created_at
updated_at
```

FX-style exchange-rate data can be represented as a price bar by storing the rate in `close`.

The other OHLCV fields can stay empty until ARGUS uses data sources that provide them.

Example price bar records shown with joined source and instrument information for readability:

| source   | instrument | timestamp  | timeframe |   open |   high |    low |  close | adjusted_close |   volume |
| -------- | ---------- | ---------- | --------- | -----: | -----: | -----: | -----: | -------------: | -------: |
| yfinance | EUR/USD    | 2024-01-02 | 1d        |   null |   null |   null |  1.095 |           null |     null |
| yfinance | AAPL       | 2024-01-02 | 1d        | 187.15 | 188.44 | 183.89 | 185.64 |         184.25 | 50200000 |

---

## Recommended First Implementation Step

The first storage implementation should not be tied to one specific data provider.

ARGUS currently works with an existing ExchangeRate API client and evaluates broader market data through yfinance.  
Frankfurter may be added later as a stronger FX-oriented historical data source.

The storage layer should therefore focus on a normalized internal market-data format instead of depending on one API response structure.

Recommended first step:

```text
active data client
→ normalize into instruments and price_bars
→ store in DuckDB
→ query with SQL
→ use results for analytics and charts
```

---

## Future Direction

Later sprints can expand the storage layer step by step.

Possible later additions:

| Future Area | Possible Additions |
| --- | --- |
| Better source mapping | source-specific symbols, provider metadata |
| Watchlists | user-selected instruments |
| Reports | generated report metadata and history |
| Macro data | FRED indicators and observations |
| Paper trading | simulated orders, positions and portfolio history |
| Server architecture | PostgreSQL |
| SQL tooling | SQLGate with PostgreSQL |
| Cloud direction | managed PostgreSQL or cloud storage |

SQLGate should be kept for a later PostgreSQL phase.

It becomes useful when ARGUS moves toward:

* server-based storage
* stronger database management
* richer metadata
* more stable application state
* user-facing features
* report history
* cloud-ready architecture

Additional metadata such as documentation links, terms links or provider governance fields can also become useful later.

For the first DuckDB phase, these details should stay in research documentation instead of the database schema.

---

## Final Recommendation

ARGUS should start with DuckDB as the first local analytics storage layer.

DuckDB fits the current phase best because ARGUS needs local analytical SQL workflows, not a full server database yet.

The first implementation should store historical market data in an OHLCV-ready structure.

The recommended first data model is:

```text
data_sources
instruments
price_bars
```

Notebook exploration should be the main developer workflow before SQL logic is moved into application code.

The DuckDB CLI can be used for quick inspection.

PostgreSQL and SQLGate should be introduced later when ARGUS moves toward a more product-like or cloud-based architecture.
