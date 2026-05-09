"""Package metadata consistency tests."""

from __future__ import annotations

import tomllib
from pathlib import Path

import browsertrace


def test_package_version_matches_module_version():
    project_root = Path(__file__).resolve().parents[1]
    pyproject = tomllib.loads((project_root / "pyproject.toml").read_text())

    assert pyproject["project"]["version"] == "0.1.3"
    assert pyproject["project"]["version"] == browsertrace.__version__
