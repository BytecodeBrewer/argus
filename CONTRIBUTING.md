# Contributing to ARGUS

Thank you for your interest in contributing to ARGUS.

ARGUS is a Python-based market analytics project focused on clean data workflows, reliable code, useful metrics and future AI-assisted monitoring.

This project is still growing, so contributions should help the project become more stable, understandable and useful step by step.

> [!IMPORTANT]
> ARGUS values reliability, clear communication and long-term skill building.  
> Contributions should improve the project without creating unnecessary complexity.

---

## Project Mindset

ARGUS is not only about adding features quickly.

The project is built around:

- clean Python code
- understandable architecture
- reliable tests
- useful documentation
- careful data handling
- practical analytics
- continuous learning

Good contributions should make the project easier to use, test, maintain or extend.

---

## What You Can Contribute

Helpful contributions include:

- bug fixes
- tests
- documentation improvements
- small refactorings
- validation improvements
- analytics metrics
- chart improvements
- data-source clients
- CI/CD improvements
- issue clarification
- architecture notes
- examples and usage instructions

> [!NOTE]
> Large features should usually start with an issue or short discussion before implementation.

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

## Development Setup

Clone the repository:

```bash
git clone https://github.com/BytecodeBrewer/argus.git
cd argus
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

Install the project with development dependencies:

```bash
pip install -e ".[dev]"
```

---

## Branch Workflow

Create a new branch for your work:

```bash
git checkout -b <issue-number-short-description>
```

Example:

```bash
git checkout -b 12-add-volatility-metric
```

Use focused branch names that describe the work.

---

## Commit Expectations

Commits should be small, understandable and related to the current task.

Good commit messages:

```text
Add rolling volatility metric
Fix currency validation edge case
Update README setup instructions
Add tests for trend metrics
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
> A good commit tells future readers what changed and why it belongs to the task.

---

## Testing

Before opening a pull request, run the test suite:

```bash
pytest
```

A pull request should not be opened as ready for review if tests are failing without explanation.

If a test fails and you do not know why, mention it clearly in the pull request.

> [!IMPORTANT]
> CI checks must pass before a pull request can be merged.

---

## Pull Request Expectations

A good pull request should include:

- a clear title
- a short explanation of what changed
- a link to the related issue if available
- notes about tests
- screenshots for UI changes if useful
- a short explanation of any trade-offs

Pull requests should be focused and reviewable.

Before opening a pull request, run:

```bash
pytest
ruff check .
ruff format --check .
```

---

## Reliability Expectations

Contributors are expected to work reliably.

This means:

- do not submit random or unfinished code without context
- do not ignore failing tests
- do not introduce secrets, API keys or local machine paths
- do not rewrite unrelated parts of the project without discussion
- communicate if you are unsure
- keep changes understandable for future contributors
- respect the existing architecture unless there is a clear reason to change it

Reliability does not mean knowing everything already.

It means being honest, careful and consistent.

---

## Learning Mindset

ARGUS welcomes contributors who want to improve their technical skills.

You do not need to be an expert to contribute.

Helpful behavior includes:

- asking clear questions
- explaining your reasoning
- being open to review feedback
- improving your code after feedback
- learning from tests, errors and architecture discussions
- documenting what you learned when it helps others

> [!NOTE]
> This project values skill growth.  
> A thoughtful small contribution is better than a large unclear one.

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

Never commit secrets.

Do not commit:

- API keys
- tokens
- passwords
- `.env` files
- local config files with private data

Use a local `.env` file for secrets.

```env
api_key=your_api_key_here
```

> [!WARNING]
> If you accidentally commit a secret, revoke it immediately and inform the maintainer.

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

Repository-level files such as `README.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` and `LICENSE` belong in the repository root.

Technical notes, research and deeper explanations belong in `docs/`.

---

## Communication

Please communicate respectfully and constructively.

When giving feedback:

- focus on the code or idea, not the person
- explain the reason behind suggestions
- be specific
- stay open to alternatives

When receiving feedback:

- assume good intent
- ask questions if something is unclear
- improve the contribution step by step

All contributors are expected to follow the project’s Code of Conduct.

---

## Maintainer Notes

The maintainer may ask for changes before merging a pull request.

A contribution may be declined if it:

- does not fit the current roadmap
- adds too much complexity too early
- breaks existing functionality
- lacks necessary tests
- duplicates existing work
- does not follow the project’s quality expectations

This helps keep ARGUS stable, learnable and maintainable.