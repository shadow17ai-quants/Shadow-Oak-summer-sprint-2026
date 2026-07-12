"""Repo README standardization helper.

This script is intentionally lightweight: it validates that a README contains
core sections and prints actionable findings.

Usage:
  python standardize_readme_checklist.py path/to/README.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED_HEADINGS = [
    r"^##\s+Overview\s*$",
    r"^##\s+Installation\s*$",
    r"^##\s+Usage\s*$",
    r"^##\s+Testing\s*$",
    r"^##\s+Contributing\s*$",
    r"^##\s+License\s*$",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_readme(readme_text: str) -> list[str]:
    problems: list[str] = []

    for pattern in REQUIRED_HEADINGS:
        if not re.search(pattern, readme_text, flags=re.MULTILINE):
            heading = pattern.strip("^")
            problems.append(f"Missing required heading matching pattern: {heading}")

    # optional but recommended markers
    if "Architecture Overview" not in readme_text and "Architecture" not in readme_text:
        problems.append("Consider adding an 'Architecture Overview' section")

    if "Badges" not in readme_text:
        problems.append("Consider adding GitHub Actions/license/type badges")

    return problems


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python standardize_readme_checklist.py path/to/README.md")
        return 2

    readme_path = Path(sys.argv[1])
    if not readme_path.exists():
        print(f"File not found: {readme_path}")
        return 2

    text = read_text(readme_path)
    problems = check_readme(text)

    if not problems:
        print("README looks compliant with the standard checklist.")
        return 0

    print("README checklist issues:")
    for p in problems:
        print(f"- {p}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
