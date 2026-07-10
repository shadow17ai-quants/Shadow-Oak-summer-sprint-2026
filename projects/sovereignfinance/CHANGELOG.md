# Changelog

All notable changes to SovereignFinance will be documented in this file.

## [Unreleased]
### Added
- Comprehensive README with project overview, architecture, usage, and roadmap.
- CONTRIBUTING.md guideline for contributors.
- MIT LICENSE file.
- Standardized project structure with `src/` layout.
- Pre‑commit hooks configuration (to be added).
- GitHub Actions CI workflow (to be added).

### Changed
- Refactored `validate_transaction_data` to remove stray parameter, fixing description loss.
- Changed call to `db.add_transaction` to use keyword arguments for clearer API.

### Fixed
- Test `test_cli_add_income_flow` now passes; description is correctly passed through the call chain.
- Various minor typos in docstrings and comments.

## [0.1.0] - 2026-07-10
### Added
- Initial release of SovereignFinance personal finance tracker.
- Command‑line interface (CLI) for adding income/expenses, viewing transactions, generating PDF reports.
- Interactive Streamlit dashboard with charts and CRUD operations.
- SQLite database schema and DAO layer.
- Input validation module with comprehensive checks.
- Basic test suite covering CLI, config, database, dashboard, and validation.
- Requirements file (`requirements.txt`) with core dependencies.
- Seed data script for quick demonstration.