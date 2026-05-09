"""Package metadata consistency tests."""

from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path

import browsertrace


def test_package_version_matches_module_version():
    project_root = Path(__file__).resolve().parents[1]
    pyproject = tomllib.loads((project_root / "pyproject.toml").read_text())

    assert pyproject["project"]["version"] == "0.1.10"
    assert pyproject["project"]["version"] == browsertrace.__version__


def test_pyproject_has_launch_discovery_metadata():
    project_root = Path(__file__).resolve().parents[1]
    pyproject = tomllib.loads((project_root / "pyproject.toml").read_text())
    project = pyproject["project"]

    keywords = set(project["keywords"])
    assert {
        "ai-agent-debugging",
        "browser-agent",
        "browser-agents",
        "computer-use",
        "llm-observability",
    } <= keywords

    classifiers = set(project["classifiers"])
    assert "Topic :: Scientific/Engineering :: Artificial Intelligence" in classifiers
    assert "Topic :: Software Development :: Testing" in classifiers

    urls = project["urls"]
    assert urls["Changelog"] == "https://github.com/aaronlab/browsertrace/blob/main/CHANGELOG.md"
    assert urls["Roadmap"] == "https://github.com/aaronlab/browsertrace/blob/main/ROADMAP.md"
    assert urls["Discussions"] == "https://github.com/aaronlab/browsertrace/discussions/6"


def test_homepage_has_software_source_code_json_ld():
    project_root = Path(__file__).resolve().parents[1]
    homepage = (project_root / "docs" / "index.html").read_text()

    match = re.search(
        r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
        homepage,
        re.S,
    )

    assert match is not None
    metadata = json.loads(match.group(1))
    assert metadata["@context"] == "https://schema.org"
    assert metadata["@type"] == "SoftwareSourceCode"
    assert metadata["name"] == "BrowserTrace"
    assert metadata["codeRepository"] == "https://github.com/aaronlab/browsertrace"
    assert metadata["programmingLanguage"] == "Python"
    assert metadata["license"] == "https://opensource.org/license/mit"
