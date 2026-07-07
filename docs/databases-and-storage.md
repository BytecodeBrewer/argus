# ARGUS Storage Research

## Intro

It was previously a research what ARGUS should store and which database/storage approach fits the project.
Now it's a simple documentation about how the storage and domain logic looks like and should develop in the next sprints.

ARGUS is moving from live API requests and in-memory analytics toward real data workflows.  
The first storage decision should support local market analytics, SQL practice and future dashboard features without adding unnecessary infrastructure too early.

---

## First Storage Approach

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

---

## First Data Model Direction

The first data model should support FX data now and broader market data later.

ARGUS should not use a narrow `date | value` table as the main market-data model.

That would work for simple exchange rates, but it would become limiting once ARGUS adds stocks, ETFs, indices or broader market APIs.

The first model focuses on two primary metadata entities, supported by standard operational schemas and communication interfaces:

```text
DataSource
Instrument
```

### DataSource

Stores where data came from.

Current operational fields:

```text
name
provider_kind
requires_api_key (defaults to False)
```

### Instrument

Stores what ARGUS can analyze.
Current operational fields:

```text
symbol
name
asset_class
currency (optional)
exchange (optional)
base_currency (optional)
quote_currency (optional)
```

### Internal Operational Models

To support decoupled runtime communication and execution pipelines, ARGUS utilizes specialized Python dataclasses. These structures orchestrate active data flows between data-fetching clients and services.

**MarketDataRequest**
Encapsulates parameters passed to fetching engines and downstream query handlers.

* `source`: The targeted `DataSource` instance
* `instrument`: The targeted `Instrument` instance
* `timeframe`: Granularity of requested bars (like `"1d"`, `"1h"`).
* `start`: Temporal lower bound (`datetime.date`)
* `end`: Temporal upper bound (`datetime.date`)

**MarketDataResponse**
Encapsulates runtime data payloads, structural enforcement, and pipeline feedback.

* `source`: The originating `DataSource` instance
* `instrument`: The corresponding `Instrument` instance
* `bars`: A `pandas.DataFrame` holding the time-series payload
* `message`: Pipeline feedback or error context (defaults to `""`)

### The Price Bar Schema (Data Uniformity)

Crucially, **Price Bars are not treated as a standalone domain metadata model or database entity.** Instead, the Price Bar specification acts purely as an internal **uniformity schema** to normalize incoming time-series data across disparate third-party APIs.

All responses must be mapped into this standard schema layout within the `bars` DataFrame.

#### Provider Mapping Layer

Third-party structures are converted to this unified standard upon ingest. For example, `yfinance` fields map to the uniform schema via `YFINANCE_PRICE_BAR_MAPPING`:

* `Date` $\rightarrow$ `timestamp`
* `Open` $\rightarrow$ `open`
* `High` $\rightarrow$ `high`
* `Low` $\rightarrow$ `low`
* `Close` $\rightarrow$ `close`
* `Adj Close` $\rightarrow$ `adjusted_close`
* `Volume` $\rightarrow$ `volume`

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
