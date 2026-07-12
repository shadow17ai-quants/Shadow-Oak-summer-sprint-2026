# Contributing to NifftyVault

Thank you for considering a contribution to NifftyVault! Please read this document to understand how you can help improve the project.

## How to Contribute

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/nifftyvault.git
   cd nifftyvault
   ```
3. **Create a branch** for your work:
   ```bash
   git checkout -b feature/your-feature-name
   ```
   Use `fix/`, `docs/`, `refactor/` prefixes as appropriate.
4. **Make your changes**, following the coding standards below.
5. **Run the test suite** to ensure nothing is broken:
   ```bash
   pytest
   ```
6. **Commit your changes** with a clear, descriptive message.
7. **Push to your fork** and open a Pull Request (PR) against the `main` branch.

## Coding Standards

- **Language**: Python 3.11+.
- **Formatting**: Use [Black](https://black.readthedocs.io/) with line length 88.
  ```bash
  black .
  ```
- **Linting**: Use [Ruff](https://docs.astral.sh/ruff/) for fast linting.
  ```bash
  ruff check .
  ```
- **Type Hints**: All public functions and methods must have type annotations.
- **Docstrings**: Follow the NumPy/SciPy docstring style.
  - Summary line, extended description, Parameters, Returns, Raises, See Also, Examples (if applicable).
- **Imports**: Standard library, third‑party, then local imports, each group separated by a blank line.
- **Naming**: `snake_case` for variables/functions, `UPPER_CASE` for constants, `PascalCase` for classes.
- **Constants**: Place in `src/nifftyvault/config.py` and annotate with `Final`.
- **Avoid**: Magic numbers, deep nesting (>4 levels), overly long functions (>50 lines).

## Testing

- Write unit tests for new functionality in the appropriate `tests/` file.
- Aim for high test coverage; new code must be covered by tests.
- Use `pytest` fixtures for reusable setup (see `tests/conftest.py` if present).

## Documentation

- Update the README if your changes affect user‑visible behavior.
- Add or modify docstrings for new public APIs.
- If you add a major feature, consider adding a section to the README or a separate documentation file.

## Pull Request Process

1. Ensure your branch is up to date with `main`:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```
2. Make sure all checks pass (CI will run automatically).
3. Request a review from at least one maintainer.
4. Address any feedback promptly.
5. Once approved, a maintainer will merge your PR.

## Reporting Issues

Please use the GitHub Issues tracker. Include:

* A clear, descriptive title.
* Steps to reproduce (if applicable).
* Expected vs. actual behavior.
* Relevant logs or screenshots.
* Environment details (Python version, OS, dependency versions).

## Code of Conduct

Please note that this project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold its standards.

Thank you again for contributing to NifftyVault!