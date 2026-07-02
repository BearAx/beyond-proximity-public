#!/usr/bin/env python3
"""Compatibility entry point for the canonical headless experiment runner."""
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.run_experiment import main  # noqa: E402


if __name__ == "__main__":
    main()
