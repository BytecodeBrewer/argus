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
- Extend the current dashboard
- Add or evaluate new data clients:
  - yfinance for broader market data
- Improve pandas-based analysis workflows
- Add a local storage for historical market data
- Add report generation and export
- add first prediction feature
- Introduce NiceGUI as a new GUI
- Add tests for metric calculations and data transformations
- Add CD Pipeline

Outcome:
ARGUS becomes a basic market analytics tool

### Sprint 3 — Storage, Web-Ready UI & Data Architecture

**Status:** Planned

Prepare ARGUS for persistent data workflows and a stronger product interface.

Scope:

- Extend local storage layer
- First local ETL Pipeline
- Extend NiceGUI and plan how to combine with modern frotend techstack like django and node.js
- Keep Tkinter as legacy/prototype unless still useful
- More metrics, more instruments and more (and better) prediction features
- Introduce first LLM summary for reports
- Introduce Snyk and Performance Test to cover perfomance and security of argus
- Improve Code Quality

Outcome:
ARGUS is a scalable analytics application that allows to get more insight from market data

### Sprint 4 — Introduction for extended Analysis

**Status:** Planned

Turn ARGUS into a stronger end-to-end data engineering project which is cloud ready.

Scope:

- Docker Compose
- Intorduce Azure (a simple connection - storage only)
- Better LLM Workflow (introduce RAG)
- Data quality checks
- Caching and efficient storing of market data
- More export possibilities for users
- More metrics and better meta data visualization

Outcome:

ARGUS is ready to interact with the cloud layer and future cloud app. It's able to give the user an transparent and clear analysis of requested market section.

### Sprint 5 — AI-Assisted Research & Agentic Monitoring

**Status:** Future vision

Scope:

- First Cloud workflows to extend the analysis
- RAG over stored market notes, reports or documentation
- Agentic checks for data quality, anomalies and recurring market scans
- Human-in-the-loop signal review
- Automated monitoring workflows

Outcome:

ARGUS and the cloud app interact with each other. ARGUS become the first time an useful monitoring and alysis tool.
It's the beginn of ARGUS to help the user to find, implement and deploy strategies. Through that ARGUS will
be first time able to give signals and allow paper trading, back tests and controlled trading with agents. 
