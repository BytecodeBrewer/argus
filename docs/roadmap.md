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

### Sprint 2 — Reporting & Market Analytics Foundation

**Status:** In progress

Move ARGUS from a simple FX-focused prototype toward a first usable market analytics and reporting tool.

**Scope:**

- Add stronger market analytics metrics:

  - cumulative return
  - strongest / weakest day
  - rolling volatility
  - basic performance analytics
  - basic risk analytics
- Add or improve real market data support:

  - yfinance for broader market data
  - existing FX conversion remains available where useful
- Improve pandas-based analysis workflows
- Introduce local storage for historical market data
- Add report generation and export
- Add a first simple prediction feature
- Introduce NiceGUI as the next GUI direction
- Extend the current dashboard with real market analytics
- Add tests for metric calculations, data transformations and storage behavior
- Improve CI/CD with first deployment or release automation steps

**Outcome:**

ARGUS becomes a basic market analytics and reporting tool.
Users can fetch market data, store it locally, calculate metrics, generate a first report and view results through a first modern dashboard.

---

### Sprint 3 — Advanced Local Analytics & Product Quality

**Status:** Planned

Expand the local ARGUS application into a stronger analytics product with better data handling, UI structure, predictions and quality checks.

**Scope:**

- Extend the local storage layer
- Add a first local ETL workflow
- Improve the NiceGUI dashboard structure and usability
- Explore how NiceGUI can later interact with a more modern frontend stack such as Django, React or Node.js-based services
- Keep Tkinter as legacy/prototype unless it is no longer useful
- Add more metrics, instruments and prediction features
- Improve report templates and report structure
- Introduce first LLM-based summaries for generated reports
- Add first performance tests
- Introduce Snyk or another dependency/security scanning workflow
- Improve code quality, test coverage and maintainability

**Outcome:**

ARGUS becomes a more scalable local analytics application.
It can process more instruments, produce better reports, provide first automated summaries and offer more reliable insight into market data.

---

### Sprint 4 — Extended Analysis & Cloud-Ready Foundation

**Status:** Planned

Prepare ARGUS for deeper analysis, cloud interaction and future portfolio-assistant workflows while keeping the local product usable and transparent.

**Scope:**

- Add Docker Compose for a more complete local development setup
- Introduce a first Azure connection, focused on simple storage or artifact exchange
- Improve the LLM workflow
- Introduce a first RAG-ready structure for reports, notes, documentation and stored analysis artifacts
- Add data quality checks
- Improve caching and efficient storage of market data
- Add more export options for users
- Add more metrics and better metadata visualization
- Improve transparency around data sources, generated reports and analysis assumptions
- Prepare clear interfaces for future cloud and assistant workflows

**Outcome:**

ARGUS becomes ready to interact with a future cloud layer.
The application can produce clearer, more transparent market analysis and prepares the foundation for retrieval-based workflows, stronger automation and future ARGUS Core integration.

---

### Sprint 5 — Cloud Interaction & Agentic Monitoring Foundation

**Status:** Planned

Start the first cloud-connected ARGUS workflows and introduce the foundation for monitoring, agentic checks and strategy-support features.

**Scope:**

- Add first cloud workflows that extend local analysis
- Connect local ARGUS workflows with the first cloud-side services
- Extend RAG over stored market notes, reports, documentation and analysis artifacts
- Add agentic checks for:

  - data quality
  - anomalies
  - recurring market scans
  - report consistency
- Add first human-in-the-loop review workflows for signals or strategy ideas
- Add automated monitoring workflows
- Prepare the first foundations for:

  - paper trading
  - backtesting
  - controlled strategy evaluation
  - future portfolio-assistant workflows

**Outcome:**

ARGUS and the first cloud-side services begin to interact.
ARGUS becomes useful not only as an analytics and reporting tool, but also as the first foundation for monitoring, strategy evaluation and controlled market-research workflows.
