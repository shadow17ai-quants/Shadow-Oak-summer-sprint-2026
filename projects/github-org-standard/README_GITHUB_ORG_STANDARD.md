# GitHub Organization Standard — Repo Checklist/Script

This repository provides a lightweight standardization guide to keep README/LICENSE/CHANGELOG/CONTRIBUTING consistent across all projects (including **SovereignFinance**).

## Checklist (apply to every repo)

### 1) Root files
- [ ] `README.md`
  - [ ] One-line tagline
  - [ ] Short description (what/why)
  - [ ] Features list
  - [ ] Architecture overview (tree diagram)
  - [ ] Installation
  - [ ] Usage examples
  - [ ] Testing instructions
  - [ ] Contributing link
  - [ ] License section
- [ ] `LICENSE`
- [ ] `CONTRIBUTING.md`
- [ ] `CHANGELOG.md`
- [ ] `.pre-commit-config.yaml` (if using pre-commit)
- [ ] `pyproject.toml` with consistent tool sections (ruff/pytest/mypy)

### 2) Badges & metadata
- [ ] GitHub Actions badges in README
- [ ] Topics configured in GitHub: `python`, `cli` (or domain-specific), `analytics`, etc.

### 3) GitHub Actions
- [ ] Workflow for `tests` (pytest)
- [ ] Workflow for `lint` (ruff + optionally mypy)

### 4) Release discipline
- [ ] Changelog entries per release
- [ ] GitHub Releases created from tags

## Script: apply standard (repository-agnostic)

Create a `standardize_repo.py` script in each repo or run from any location.

```python
# (reference only) Use internal tooling from your workflow.
```

> In this workspace, manual standardization is sufficient because file content is generated consistently.

## Suggested README skeleton

- Title
- Version
- Shadow Oak Capitals attribution
- Overview
- Features
- Architecture Overview
- Folder Structure
- Installation
- Quick Start / Usage
- Testing
- Known Limitations
- Future Roadmap
- Contributing
- License

