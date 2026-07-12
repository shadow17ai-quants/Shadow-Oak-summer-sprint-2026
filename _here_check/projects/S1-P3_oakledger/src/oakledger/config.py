"""
Configuration module for OakLedger.
Centralized configuration management.
"""

from pathlib import Path

# Base directories
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent  # oakledger project folder
DATA_DIR: Path = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

# Database configuration
DB_PATH: Path = PROJECT_ROOT / "trades.db"

# Optionally expose as string for backward compatibility
DB_PATH_STR: str = str(DB_PATH)
