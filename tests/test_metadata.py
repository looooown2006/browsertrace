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


def test_windows_powershell_first_run_docs_cover_env_vars():
    project_root = Path(__file__).resolve().parents[1]
    docs_text = "\n".join(
        [
            (project_root / "README.md").read_text(),
            (project_root / "examples" / "README.md").read_text(),
        ]
    )

    assert 'powershell' in docs_text.lower()
    assert '$env:BROWSERTRACE_HOME = "$env:TEMP\\browsertrace-demo"' in docs_text
    assert '$env:BROWSERTRACE_PORT = "4000"' in docs_text
    assert "BROWSERTRACE_HOME=/tmp/browsertrace-demo" in docs_text
    assert "BROWSERTRACE_PORT=4000 browsertrace" in docs_text


def test_docs_include_uvx_github_quickstart_before_pypi():
    project_root = Path(__file__).resolve().parents[1]
    docs_text = "\n".join(
        [
            (project_root / "README.md").read_text(),
            (project_root / "docs" / "llms.txt").read_text(),
        ]
    )

    github_spec = (
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.10'
    )
    assert f'uvx --from "{github_spec}" browsertrace demo' in docs_text
    assert f'uvx --from "{github_spec}" browsertrace list' in docs_text
    assert "before PyPI publishing is enabled" in docs_text


def test_launch_copy_includes_uvx_github_trial_before_pypi():
    project_root = Path(__file__).resolve().parents[1]
    github_spec = (
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.10'
    )

    for relpath in [
        "docs/launch/channel-copy.md",
        "docs/launch/day-1-publish-packet.md",
        "docs/launch/day-2-show-hn-packet.md",
    ]:
        text = (project_root / relpath).read_text()
        assert f'uvx --from "{github_spec}" browsertrace demo' in text, relpath
        assert "before pypi publishing is enabled" in text.lower(), relpath


def test_longform_launch_posts_include_uvx_github_trial_before_pypi():
    project_root = Path(__file__).resolve().parents[1]
    github_spec = (
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.10'
    )

    for relpath in [
        "docs/launch/tutorial-post.md",
        "docs/launch/chinese-tutorial-post.md",
        "docs/launch/response-templates.md",
    ]:
        text = (project_root / relpath).read_text()
        assert f'uvx --from "{github_spec}" browsertrace demo' in text, relpath
        assert "pypi" in text.lower(), relpath


def test_directory_submission_sheet_includes_uvx_trial_before_pypi():
    project_root = Path(__file__).resolve().parents[1]
    github_spec = (
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.10'
    )
    sheet = (project_root / "docs" / "launch" / "directory-submission-sheet.md").read_text()

    assert "before pypi publishing is enabled" in sheet.lower()
    assert f'uvx --from "{github_spec}" browsertrace demo' in sheet


def test_awesome_list_submission_notes_include_trial_and_demo_links():
    project_root = Path(__file__).resolve().parents[1]
    github_spec = (
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.10'
    )
    notes = (
        project_root / "docs" / "launch" / "github-awesome-list-submissions.md"
    ).read_text()

    assert "https://aaronlab.github.io/browsertrace/" in notes
    assert "browsertrace-demo-public.html" in notes
    assert f'uvx --from "{github_spec}" browsertrace demo' in notes


def test_owner_next_actions_include_uvx_fallback_before_pypi():
    project_root = Path(__file__).resolve().parents[1]
    github_spec = (
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.10'
    )

    for relpath in [
        "docs/launch/owner-next-actions.md",
        "docs/launch/owner-next-actions.zh-CN.md",
    ]:
        text = (project_root / relpath).read_text()
        assert f'uvx --from "{github_spec}" browsertrace demo' in text, relpath
        assert "pypi" in text.lower(), relpath
