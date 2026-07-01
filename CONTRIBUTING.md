# Contributing to ARGUS

Thank you for your interest in contributing to ARGUS.

ARGUS is a Python-based market analytics project focused on clean data workflows, reliable code, useful metrics and future AI-assisted monitoring.

The project is still growing, so contributions should be small, focused and easy to review. You do not need to be an expert to contribute, but your changes should be understandable, reliable and related to the current project direction.

Good starting points are issues labeled `good first issue`. These issues are usually smaller, easier to review and better suited for getting familiar with the project.

Helpful contributions include:

- bug fixes
- tests
- documentation improvements
- small refactorings
- analytics metrics
- data-source clients
- UI or chart improvements
- CI/CD and tooling improvements
- architecture or research notes

> [!IMPORTANT]
> Please keep changes focused and avoid adding unnecessary complexity.

---

## Before You Start

Before working on a contribution:

1. Check existing issues and pull requests.
2. Make sure your idea fits the current roadmap.
3. Keep the scope small and focused.
4. Ask if the direction is unclear.

Avoid opening large pull requests that mix unrelated changes.

Good examples:

- one PR for a new metric
- one PR for a bug fix
- one PR for documentation cleanup
- one PR for CI improvements

Bad examples:

- one PR that changes the UI, rewrites services, updates docs and adds a new data client at the same time

---

## Contribution Expectations

Contributors are expected to keep changes focused, understandable and related to the issue or task.

Please:

- explain your changes clearly
- be open to review feedback
- improve your contribution step by step after feedback
- avoid unrelated rewrites
- respect the existing architecture unless there is a clear reason to change it
- do not add scripts that automatically run `git add`, `git commit`, `git push` or create pull requests unless this was discussed first

A contribution may be declined or delayed if it:

- does not fit the current roadmap
- adds too much complexity too early
- breaks existing functionality
- lacks necessary checks or documentation
- duplicates existing work
- bypasses the repository workflow

---

## Branch Workflow

For issue-based work, create your branch from the related GitHub issue when possible.

GitHub may suggest a branch name based on the issue title. You can shorten it if the generated name is too long.

Good branch names are focused and describe the task:

```text
43-research-forecasting-approach
33-add-yfinance-client
40-improve-test-coverage
```

If you create the branch manually, use:

```bash
git checkout -b <issue-number-short-description>
```

Example:

```bash
git checkout -b 43-research-forecasting-approach
```

---

## Commit Expectations

Commits should be small, understandable and related to the current task.

ARGUS uses a conventional commit style with an issue reference:

```text
type(#issue): short description
```

Good commit messages:

```text
docs(#43): research first forecasting approach
feat(#33): add yfinance historical data client
test(#40): add tests for conversion service
fix(#33): handle empty historical data response
refactor(#34): split metric helpers
ci(#10): update commit message workflow
```

Avoid unclear messages:

```text
fix
stuff
changes
update
final
```

> [!TIP]
> A good commit tells future readers what changed and which issue it belongs to.

---

## Checks

Before opening a pull request, run the project checks:

```bash
pytest
ruff check .
ruff format --check .
```

These checks verify that tests pass, code style is valid and formatting is consistent.

A pull request should not be marked as ready for review if checks are failing without explanation.

If a check fails and you are unsure why, mention it clearly in the pull request.

> [!IMPORTANT]
> CI checks must pass before a pull request can be merged.

---

## Pull Request Expectations

Pull requests should target `develop` unless the maintainer explicitly says otherwise.

Do not open feature, research or documentation pull requests directly against `main`.
The `main` branch is reserved for stable/release-ready changes.

Please use the pull request template and fill it out clearly.

The template helps reviewers understand:

- what changed
- which issue is related
- whether tests were run
- whether documentation or screenshots are needed
- if there are any notes or trade-offs

Do not bypass the pull request template or replace it with an unrelated auto-generated description.  
It makes reviewing harder and may delay the merge.

---

## Code Style

Keep code simple and readable.

General guidelines:

- prefer clear names over clever shortcuts
- keep functions focused
- separate data loading, transformation and presentation logic
- avoid unnecessary global state
- avoid hidden side effects
- add tests for important behavior
- document assumptions when they matter

For analytics code:

- keep metric functions reusable
- avoid coupling metrics directly to UI code
- avoid coupling metrics directly to one specific API client
- prefer clear pandas transformations

---

## Secrets and API Keys

Never commit secrets, API keys, tokens, passwords, `.env` files or local config files with private data.

Use a local `.env` file for secrets:

```env
EXCHANGE_RATE_API_KEY=your_api_key_here
```

---

## Documentation

Documentation changes are welcome.

Useful documentation includes:

- setup instructions
- roadmap notes
- architecture explanations
- metric definitions
- data-source assumptions
- troubleshooting notes

Technical notes, research and deeper explanations belong in `docs/`.
