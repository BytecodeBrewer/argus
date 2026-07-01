# Roadmap

Each roadmap phase is treated as a separate development sprint.  
The roadmap is intentionally iterative: each sprint should leave the project in a usable and testable state.

## Sprint 1 — Product Foundation & First Public Release

**Status:** Completed

Build a small but usable Python application with a clear structure, tests, documentation and first release readiness.

Scope:

- Modular Python package structure
- REST API client for live exchange rates
- Calculator and currency conversion logic
- Input validation and error handling
- Tkinter GUI prototype
- Legacy CLI/debug interface
- First pandas/matplotlib analytics prototype with mock time-series data
- Basic test suite
- README update
- First release instructions
- API key setup instructions
- Collaboration documentation through `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` and `LICENSE`

Outcome:
Sprint 1 established the local ARGUS foundation with package structure, GUI prototype, analytics prototype, tests, documentation, CI, Dependabot and governance files.

### Sprint 2 — Market Analytics & Data Source Expansion

**Status:** In progress

Move from simple FX conversion toward broader market analytics.

Scope:

- Add stronger market metrics:
  - cumulative return
  - strongest / weakest day
  - rolling volatility
  - performance analytics
  - risk analytics
- Extend the current dashboard without adding unnecessary chart noise
- Add or evaluate new data clients:
  - Frankfurter for historical FX data
  - yfinance for broader market data
- Replace or reduce dependency on the current ExchangeRate API where needed
- Improve pandas-based analysis workflows
- Add tests for metric calculations and data transformations
- Document metric definitions, assumptions and chart behavior

Outcome:
ARGUS becomes a basic market analytics tool, not only a converter.

### Sprint 3 — Storage, Web-Ready UI & Data Architecture

**Status:** Planned

Prepare ARGUS for persistent data workflows and a stronger product interface.

Scope:

- Add local storage layer:
  - PostgreSQL, DuckDB, SQLite or Parquet depending on use case
- Store historical market data
- Separate ingestion, transformation, analytics and presentation layers more clearly
- Start NiceGUI as the main web-ready UI direction
- Keep Tkinter as legacy/prototype unless still useful
- Keep CLI as internal/debug interface only
- Add clearer architecture documentation
- Prepare the project for larger data workflows and external contributors

Outcome:
ARGUS has a clearer data architecture and starts moving from local prototype toward a scalable analytics application.

### Sprint 4 — Cloud, Pipelines & Portfolio-Grade Data Engineering

**Status:** Future

Turn ARGUS into a stronger end-to-end data engineering project.

Scope:

- Docker / Docker Compose
- Scheduled data ingestion
- Cloud storage or cloud database
- CI/CD improvements
- Data quality checks
- Basic pipeline orchestration
- Reporting layer
- Architecture diagram
- Deployment documentation

Target workflow:

```text
API → Ingestion → Storage → Transformation → Analysis → Visualization → CI/CD
```

### Sprint 5 — AI-Assisted Research & Agentic Monitoring

**Status:** Future vision

Add AI support only after the data, storage, service and reporting layers are stable.

Scope:

- LLM-assisted report summaries
- Explanation of unusual movements
- RAG over stored market notes, reports or documentation
- Agentic checks for data quality, anomalies and recurring market scans
- Human-in-the-loop signal review
- Automated monitoring workflows

Outcome:

ARGUS starts behaving like its name: a system that continuously watches market data, evaluates it and helps generate useful signals.
