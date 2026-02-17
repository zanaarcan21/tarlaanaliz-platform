# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.

"""Pytest global configuration for CI/local parity."""

from __future__ import annotations

import importlib.util
from typing import Any


def pytest_addoption(parser: Any) -> None:
    """Register fallback options when optional plugins are missing."""
    parser.addini("asyncio_mode", "pytest-asyncio compatibility option")

    if importlib.util.find_spec("pytest_cov") is None:
        parser.addoption("--cov", action="store", default=None)
        parser.addoption("--cov-report", action="append", default=[])
