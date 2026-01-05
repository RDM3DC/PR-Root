# Contributing

## Development setup
```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -U pip
python -m pip install -e .[dev]
pytest -q
ruff check .
```

## Guidelines
- Add tests for behavior changes.
- Keep math claims conservative: PR-Root is branch bookkeeping for standard complex functions.
- Prefer small, reviewable PRs.

## Reporting issues
Include:
- Python version
- Minimal reproduction snippet
- Expected vs actual behavior
