"""
Shared test configuration for OakLedger.
"""

import sys
from pathlib import Path

# Add the src directory to the path so we can import oakledger
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
