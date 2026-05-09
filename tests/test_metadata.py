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

    assert pyproject["project"]["version"] == "0.1.14"
    assert pyproject["project"]["version"] == browsertrace.__version__


def test_public_docs_do_not_reference_stale_v011_release():
    project_root = Path(__file__).resolve().parents[1]
    public_docs = [
        project_root / "README.md",
        project_root / "LAUNCH.md",
        *sorted((project_root / "docs").rglob("*.md")),
        *sorted((project_root / "docs").rglob("*.html")),
        project_root / "docs" / "llms.txt",
    ]

    stale_release = re.compile(r"v0\.1\.1(?!\d)")
    stale_mentions = [
        str(path.relative_to(project_root))
        for path in public_docs
        if stale_release.search(path.read_text())
    ]

    assert stale_mentions == []


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
    assert urls["Debugging Guide"] == "https://aaronlab.github.io/browsertrace/debug-browser-agent-failure.html"
    assert urls["Computer Use Guide"] == "https://aaronlab.github.io/browsertrace/computer-use-agent-debugging.html"
    assert urls["Browser Use Guide"] == "https://aaronlab.github.io/browsertrace/browser-use-debugging.html"
    assert urls["Changelog"] == "https://github.com/aaronlab/browsertrace/blob/main/CHANGELOG.md"
    assert urls["Roadmap"] == "https://github.com/aaronlab/browsertrace/blob/main/ROADMAP.md"
    assert urls["Discussions"] == "https://github.com/aaronlab/browsertrace/discussions/6"


def test_publish_workflow_is_ready_for_trusted_publishing():
    project_root = Path(__file__).resolve().parents[1]
    workflow = (project_root / ".github" / "workflows" / "publish.yml").read_text()

    assert "workflow_dispatch:" in workflow
    assert re.search(r"publish:\n(?: {4}.*\n)* {4}environment: pypi", workflow)
    assert re.search(
        r"publish:\n(?: {4}.*\n)* {4}permissions:\n"
        r"(?: {6}.*\n)* {6}contents: read\n"
        r"(?: {6}.*\n)* {6}id-token: write",
        workflow,
    )
    assert "pypa/gh-action-pypi-publish@release/v1" in workflow


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


def test_core_guides_have_tech_article_json_ld():
    project_root = Path(__file__).resolve().parents[1]
    guide_pages = [
        ("debug-browser-agent-failure.html", "How to debug an AI browser-agent failure"),
        ("browser-use-debugging.html", "Debug Browser Use failures with BrowserTrace"),
        ("stagehand-debugging.html", "Debug Stagehand runs with BrowserTrace"),
        ("skyvern-debugging.html", "Debug Skyvern task failures with BrowserTrace"),
        (
            "playwright-llm-debugging.html",
            "Debug Playwright + LLM browser-agent failures with BrowserTrace",
        ),
        (
            "computer-use-agent-debugging.html",
            "Debug custom computer-use agent failures with BrowserTrace",
        ),
    ]

    for filename, headline in guide_pages:
        page = (project_root / "docs" / filename).read_text()
        match = re.search(
            r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
            page,
            re.S,
        )

        assert match is not None, filename
        metadata = json.loads(match.group(1))
        assert metadata["@context"] == "https://schema.org", filename
        assert metadata["@type"] == "TechArticle", filename
        assert metadata["headline"] == headline, filename
        assert metadata["isPartOf"]["name"] == "BrowserTrace", filename
        assert metadata["codeRepository"] == "https://github.com/aaronlab/browsertrace", filename


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
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.14'
    )
    assert f'uvx --from "{github_spec}" browsertrace demo' in docs_text
    assert f'uvx --from "{github_spec}" browsertrace list' in docs_text
    assert "before PyPI publishing is enabled" in docs_text


def test_owner_launch_checklists_include_doctor_fallback_before_pypi():
    project_root = Path(__file__).resolve().parents[1]
    github_spec = (
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.14'
    )

    for relpath in [
        "LAUNCH.md",
        "docs/launch/owner-next-actions.md",
        "docs/launch/owner-next-actions.zh-CN.md",
    ]:
        text = (project_root / relpath).read_text()
        assert f'uvx --from "{github_spec}" browsertrace doctor' in text, relpath
        assert f'uvx --from "{github_spec}" browsertrace demo' in text, relpath
        assert "pypi" in text.lower(), relpath


def test_github_profile_draft_links_current_trial_and_contribution_paths():
    project_root = Path(__file__).resolve().parents[1]
    github_spec = (
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.14'
    )
    profile_draft = (
        project_root / "docs" / "launch" / "github-profile-readme.md"
    ).read_text()

    assert "https://github.com/aaronlab/browsertrace" in profile_draft
    assert "https://aaronlab.github.io/browsertrace/computer-use-agent-debugging.html" in profile_draft
    assert f'uvx --from "{github_spec}" browsertrace doctor' in profile_draft
    assert f'uvx --from "{github_spec}" browsertrace demo' in profile_draft
    assert "https://github.com/aaronlab/browsertrace/issues/3" in profile_draft
    assert "https://github.com/aaronlab/browsertrace/issues/90" in profile_draft


def test_readme_has_public_safe_export_sharing_example():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()

    assert "## Share A Public-Safe Trace" in readme
    assert "browsertrace demo" in readme
    assert "browsertrace list" in readme
    assert "browsertrace export <run_id> --public -o public.html" in readme
    assert "prompts/model I/O, screenshots, and URLs" in readme
    assert "hosted upload" in readme


def test_readme_has_browser_agent_feedback_checklist():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()

    assert "## Report A Browser-Agent Failure" in readme
    assert "Browser Use, Stagehand, Skyvern, Playwright + LLM, or custom computer-use" in readme
    assert "agent framework" in readme
    assert "failure symptom" in readme
    assert "browsertrace show <run_id>" in readme
    assert "public-safe export" in readme
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_launch_discussion_near_feedback():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()
    feedback_section = readme.split("## Report A Browser-Agent Failure", 1)[1].split(
        "## Why not just use ___?", 1
    )[0]

    assert "https://github.com/aaronlab/browsertrace/discussions/6" in feedback_section
    assert "browser-agent workflow feedback" in feedback_section
    assert "stars" not in feedback_section.lower()
    assert "upvotes" not in feedback_section.lower()
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_private_reports_near_feedback():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()
    feedback_section = readme.split("## Report A Browser-Agent Failure", 1)[1].split(
        "## Why not just use ___?", 1
    )[0]

    assert "[SECURITY.md](SECURITY.md)" in feedback_section
    assert "ordinary workflow feedback" in feedback_section
    assert "private or sensitive reports" in feedback_section
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_contributor_guide_near_contributing():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()
    contributing_section = readme.split("## Contributing", 1)[1].split(
        "## License", 1
    )[0]

    assert "[CONTRIBUTING.md](CONTRIBUTING.md)" in contributing_section
    assert "small, issue-based contribution path" in contributing_section
    assert "good first issue" in contributing_section
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_code_of_conduct_near_contributing():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()
    contributing_section = readme.split("## Contributing", 1)[1].split(
        "## License", 1
    )[0]

    assert "[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)" in contributing_section
    assert "concise contributor expectations" in contributing_section
    assert "welcoming baseline" in contributing_section
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_issue_template_chooser_near_contributing():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()
    contributing_section = readme.split("## Contributing", 1)[1].split(
        "## License", 1
    )[0]

    assert (
        "https://github.com/aaronlab/browsertrace/issues/new/choose"
        in contributing_section
    )
    assert "bug, feature, integration, or cloud/team template" in contributing_section
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_pull_request_template_near_contributing():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()
    contributing_section = readme.split("## Contributing", 1)[1].split(
        "## License", 1
    )[0]

    assert (
        "[pull request template](.github/PULL_REQUEST_TEMPLATE.md)"
        in contributing_section
    )
    assert "linked issue and test commands" in contributing_section
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_release_notes_near_install_tag():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()
    install_section = readme.split("## Install From The Release Tag", 1)[1].split(
        "For a walkthrough", 1
    )[0]

    assert (
        "https://github.com/aaronlab/browsertrace/releases/tag/v0.1.14"
        in install_section
    )
    assert "v0.1.14 release notes" in install_section
    assert "PyPI publishing is not enabled yet" in install_section
    assert "@v0.1.14" in install_section
    assert "hosted sharing" not in readme


def test_readme_links_pypi_tracking_issue_near_install_tag():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()
    install_section = readme.split("## Install From The Release Tag", 1)[1].split(
        "For a walkthrough", 1
    )[0]

    assert "https://github.com/aaronlab/browsertrace/issues/5" in install_section
    assert "PyPI tracking issue" in install_section
    assert "PyPI publishing is not enabled yet" in install_section
    assert "@v0.1.14" in install_section
    assert "hosted sharing" not in readme


def test_readme_mentions_python_version_near_install_tag():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()
    install_section = readme.split("## Install From The Release Tag", 1)[1].split(
        "For a walkthrough", 1
    )[0]

    assert "Requires Python 3.11+" in install_section
    assert "PyPI publishing is not enabled yet" in install_section
    assert "@v0.1.14" in install_section
    assert "hosted sharing" not in readme


def test_readme_links_first_run_troubleshooting_near_install_tag():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()
    install_section = readme.split("## Install From The Release Tag", 1)[1].split(
        "For a walkthrough", 1
    )[0]

    assert "examples/#first-run-troubleshooting-checklist" in install_section
    assert "first-run troubleshooting checklist" in install_section
    assert "@v0.1.14" in install_section
    assert "hosted sharing" not in readme


def test_readme_explains_doctor_near_install_tag():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()
    install_section = readme.split("## Install From The Release Tag", 1)[1].split(
        "For a walkthrough", 1
    )[0]

    assert "`browsertrace doctor` is a safe local status check" in install_section
    assert "install and trace-store status" in install_section
    assert "@v0.1.14" in install_section
    assert "hosted sharing" not in readme


def test_readme_explains_list_near_install_tag():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()
    install_section = readme.split("## Install From The Release Tag", 1)[1].split(
        "For a walkthrough", 1
    )[0]

    assert "`browsertrace list` shows demo run IDs" in install_section
    assert "`browsertrace demo`" in install_section
    assert "@v0.1.14" in install_section
    assert "hosted sharing" not in readme


def test_readme_explains_show_near_install_tag():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()
    install_section = readme.split("## Install From The Release Tag", 1)[1].split(
        "For a walkthrough", 1
    )[0]

    assert "`browsertrace show <run_id>` inspects a listed run" in install_section
    assert "from the terminal" in install_section
    assert "@v0.1.14" in install_section
    assert "hosted sharing" not in readme


def test_readme_explains_public_safe_export_near_install_tag():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()
    install_section = readme.split("## Install From The Release Tag", 1)[1].split(
        "For a walkthrough", 1
    )[0]

    assert (
        "`browsertrace export <run_id> --public -o public.html` creates a "
        "public-safe HTML export"
    ) in install_section
    assert "from a listed run" in install_section
    assert "@v0.1.14" in install_section
    assert "hosted sharing" not in readme


def test_readme_explains_port_override_near_install_tag():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()
    install_section = readme.split("## Install From The Release Tag", 1)[1].split(
        "For a walkthrough", 1
    )[0]

    assert (
        "`BROWSERTRACE_PORT=3001 browsertrace` starts the local UI on another port"
        in install_section
    )
    assert "when 3000 is busy" in install_section
    assert "@v0.1.14" in install_section
    assert "hosted sharing" not in readme


def test_readme_explains_isolated_trace_storage_near_install_tag():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()
    install_section = readme.split("## Install From The Release Tag", 1)[1].split(
        "For a walkthrough", 1
    )[0]

    assert (
        "`BROWSERTRACE_HOME=/tmp/browsertrace-demo browsertrace demo` writes "
        "demo traces to an isolated trace store"
    ) in install_section
    assert "@v0.1.14" in install_section
    assert "hosted sharing" not in readme


def test_readme_explains_cli_help_near_install_tag():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()
    install_section = readme.split("## Install From The Release Tag", 1)[1].split(
        "For a walkthrough", 1
    )[0]

    assert "`browsertrace --help` lists local CLI commands and options" in install_section
    assert "@v0.1.14" in install_section
    assert "hosted sharing" not in readme


def test_readme_explains_export_help_near_install_tag():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()
    install_section = readme.split("## Install From The Release Tag", 1)[1].split(
        "For a walkthrough", 1
    )[0]

    assert (
        "`browsertrace export --help` lists export options before creating a "
        "public-safe HTML report"
    ) in install_section
    assert "@v0.1.14" in install_section
    assert "hosted sharing" not in readme


def test_readme_groups_install_tips_as_compact_list():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()
    install_section = readme.split("## Install From The Release Tag", 1)[1].split(
        "For a walkthrough", 1
    )[0]

    assert "Useful local checks:" in install_section
    for tip in [
        "- `browsertrace doctor` is a safe local status check",
        "- After `browsertrace demo`, `browsertrace list` shows demo run IDs",
        "- `browsertrace show <run_id>` inspects a listed run",
        "- `browsertrace export <run_id> --public -o public.html` creates a public-safe HTML export",
        "- `BROWSERTRACE_PORT=3001 browsertrace` starts the local UI on another port",
        "- `BROWSERTRACE_HOME=/tmp/browsertrace-demo browsertrace demo` writes demo traces to an isolated trace store",
        "- `browsertrace --help` lists local CLI commands and options",
        "- `browsertrace export --help` lists export options before creating a public-safe HTML report",
    ]:
        assert tip in install_section

    assert "@v0.1.14" in install_section
    assert "hosted sharing" not in readme


def test_readme_links_browser_use_debugging_guide():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()

    assert "https://aaronlab.github.io/browsertrace/browser-use-debugging.html" in readme
    assert "Browser Use callback compatibility" in readme
    assert "register_new_step_callback" in readme
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_stagehand_debugging_guide():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()

    assert "https://aaronlab.github.io/browsertrace/stagehand-debugging.html" in readme
    assert "Stagehand `act` and `extract` debugging" in readme
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_skyvern_debugging_guide():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()

    assert "https://aaronlab.github.io/browsertrace/skyvern-debugging.html" in readme
    assert "Skyvern task and workflow debugging" in readme
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_playwright_llm_debugging_guide():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()

    assert "https://aaronlab.github.io/browsertrace/playwright-llm-debugging.html" in readme
    assert "prompt, DOM, selector, retry, and error fields" in readme
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_integrations_overview():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()

    assert "https://aaronlab.github.io/browsertrace/integrations.html" in readme
    assert "Browser Use, Stagehand, Skyvern, and Playwright guide paths" in readme
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_adapter_request_near_integrations():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()

    assert (
        "https://github.com/aaronlab/browsertrace/issues/new?template=integration_request.yml"
        in readme
    )
    assert "Browser Use, Stagehand, Skyvern, or Playwright adapter requests" in readme
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_comparison_guide_with_named_text():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()

    assert (
        "[browser-agent debugging comparison](https://aaronlab.github.io/browsertrace/compare-browser-agent-debugging.html)"
        in readme
    )
    assert "LLM tracing" in readme
    assert "hosted browser/runtime tools" in readme
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_llms_txt_for_ai_coding_agents():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()

    assert "docs/llms.txt" in readme
    assert "AI/coding agents" in readme
    assert "concise project context" in readme
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_examples_command_cheat_sheet():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()

    assert "examples/#browsertrace-command-cheat-sheet" in readme
    assert "command cheat sheet" in readme
    assert "browsertrace doctor" in readme
    assert "browsertrace demo" in readme
    assert "browsertrace list" in readme
    assert "browsertrace show" in readme
    assert "public-safe export" in readme
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_example_matrix():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()

    assert "examples/#example-matrix" in readme
    assert "no-service examples" in readme
    assert "commands" in readme
    assert "runnable demo" in readme
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_first_run_troubleshooting_checklist():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()

    assert "examples/#first-run-troubleshooting-checklist" in readme
    assert "first-run troubleshooting checklist" in readme
    assert "browsertrace doctor" in readme
    assert "browsertrace demo" in readme
    assert "browsertrace list" in readme
    assert "browsertrace show" in readme
    assert "public-safe export" in readme
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_doctor_output_example():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()

    assert "examples/#check-a-healthy-local-install" in readme
    assert "healthy `browsertrace doctor` output" in readme
    assert "Home:" in readme
    assert "Database:" in readme
    assert "Runs:" in readme
    assert "UI dependencies:" in readme
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_public_safe_attachment_note():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()

    assert "examples/#attach-a-public-safe-export-to-an-issue" in readme
    assert "public-safe export" in readme
    assert "omits prompt/model I/O, screenshots, and URLs" in readme
    assert "GitHub issue or PR comment" in readme
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_share_safe_export_recipe():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()

    assert "examples/#creating-a-share-safe-export" in readme
    assert "browsertrace export <run_id> --public -o public.html" in readme
    assert "omits prompt/model I/O, screenshots, and URLs" in readme
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_github_actions_public_export_artifact_recipe():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()

    assert "examples/#github-actions-artifact-for-public-safe-exports" in readme
    assert "GitHub Actions artifact" in readme
    assert "public.html" in readme
    assert "BrowserTrace does not upload traces by itself" in readme
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_gitlab_ci_public_export_artifact_recipe():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()

    assert "examples/#gitlab-ci-artifact-for-public-safe-exports" in readme
    assert "GitLab CI artifact" in readme
    assert "public.html" in readme
    assert "BrowserTrace does not upload traces by itself" in readme
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_isolated_trace_storage_testing_recipe():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()

    assert "examples/#testing-with-isolated-trace-storage" in readme
    assert "isolated trace storage" in readme
    assert "BROWSERTRACE_HOME" in readme
    assert "temp directory" in readme
    assert "pytest" in readme
    assert "no browser, network, or API key" in readme
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_trace_storage_location_recipe():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()

    assert "examples/#where-traces-are-stored" in readme
    assert "~/.browsertrace/" in readme
    assert "BROWSERTRACE_HOME" in readme
    assert "local traces" in readme
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_playwright_sync_snapshot_recipe():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()

    assert "examples/#playwright-sync-api-snapshot" in readme
    assert "snapshot_sync" in readme
    assert "sync Playwright" in readme
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_environment_variable_quick_reference():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()

    assert "examples/#environment-variable-quick-reference" in readme
    assert "environment variable quick reference" in readme
    assert "BROWSERTRACE_HOME" in readme
    assert "BROWSERTRACE_PORT" in readme
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_cli_help_discovery_recipe():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()

    assert "examples/#discover-cli-options" in readme
    assert "CLI help" in readme
    assert "browsertrace --help" in readme
    assert "browsertrace export --help" in readme
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_run_id_prefix_troubleshooting_recipe():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()

    assert "examples/#run-id-prefixes-for-export" in readme
    assert "run ID prefix" in readme
    assert "browsertrace export <run_id>" in readme
    assert "longer unique prefix" in readme
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_failed_run_terminal_inspection_recipe():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()

    assert "examples/#inspect-a-failed-run-in-the-terminal" in readme
    assert "failed step timeline" in readme
    assert "browsertrace show <run_id>" in readme
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_recent_runs_list_limit_recipe():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()

    assert "examples/#show-only-recent-runs" in readme
    assert "recent runs" in readme
    assert "browsertrace list --limit 5" in readme
    assert "inspect or export" in readme
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_demo_run_lookup_recipe():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()

    assert "examples/#finding-your-demo-run" in readme
    assert "browsertrace list" in readme
    assert "run IDs" in readme
    assert "timestamps" in readme
    assert "status" in readme
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_readme_links_port_already_in_use_recipe():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()

    assert "examples/#port-already-in-use" in readme
    assert "port already in use" in readme
    assert "local UI port" in readme
    assert "BROWSERTRACE_PORT" in readme
    assert "@v0.1.14" in readme
    assert "hosted sharing" not in readme


def test_examples_readme_includes_windows_public_safe_export_flow():
    project_root = Path(__file__).resolve().parents[1]
    examples_readme = (project_root / "examples" / "README.md").read_text()

    assert "## Public Export Flow" in examples_readme
    assert (
        "```powershell\n"
        "browsertrace demo\n"
        "browsertrace list\n"
        "browsertrace export <run_id> --public -o public.html\n"
        "```"
    ) in examples_readme
    assert "`--public` omits prompts/model I/O, screenshots, and URLs" in examples_readme
    assert "BrowserTrace does not upload" in examples_readme


def test_examples_readme_includes_export_run_id_prefix_troubleshooting():
    project_root = Path(__file__).resolve().parents[1]
    examples_readme = (project_root / "examples" / "README.md").read_text()

    assert "### Run ID Prefixes For Export" in examples_readme
    assert "browsertrace list" in examples_readme
    assert "browsertrace export <run_id> --public -o public.html" in examples_readme
    assert "unique prefix" in examples_readme
    assert "copy more characters" in examples_readme
    assert "hosted sharing" not in examples_readme


def test_examples_readme_includes_browsertrace_show_failed_run_recipe():
    project_root = Path(__file__).resolve().parents[1]
    examples_readme = (project_root / "examples" / "README.md").read_text()

    assert "### Inspect a failed run in the terminal" in examples_readme
    assert "browsertrace show <run_id>" in examples_readme
    assert "browsertrace list" in examples_readme
    assert "browsertrace export <run_id> --public -o public.html" in examples_readme
    assert "failed step" in examples_readme


def test_examples_readme_includes_list_limit_recent_runs_recipe():
    project_root = Path(__file__).resolve().parents[1]
    examples_readme = (project_root / "examples" / "README.md").read_text()

    assert "### Show only recent runs" in examples_readme
    assert "browsertrace list --limit 5" in examples_readme
    assert "most recent runs" in examples_readme
    assert "browsertrace show <run_id>" in examples_readme
    assert "browsertrace export <run_id> --public -o public.html" in examples_readme
    assert "hosted sharing" not in examples_readme


def test_examples_readme_includes_doctor_output_example():
    project_root = Path(__file__).resolve().parents[1]
    examples_readme = (project_root / "examples" / "README.md").read_text()

    assert "### Check a healthy local install" in examples_readme
    assert "browsertrace doctor" in examples_readme
    assert "BrowserTrace doctor" in examples_readme
    assert "Home:" in examples_readme
    assert "Database:" in examples_readme
    assert "Runs:" in examples_readme
    assert "UI dependencies:" in examples_readme
    assert "@v0.1.14" in examples_readme
    assert "hosted sharing" not in examples_readme


def test_examples_readme_includes_cli_help_discovery_recipe():
    project_root = Path(__file__).resolve().parents[1]
    examples_readme = (project_root / "examples" / "README.md").read_text()

    assert "### Discover CLI options" in examples_readme
    assert "browsertrace --help" in examples_readme
    assert "browsertrace export --help" in examples_readme
    assert "browsertrace export <run_id> --public -o public.html" in examples_readme
    assert "@v0.1.14" in examples_readme
    assert "hosted sharing" not in examples_readme


def test_examples_readme_includes_environment_variable_quick_reference():
    project_root = Path(__file__).resolve().parents[1]
    examples_readme = (project_root / "examples" / "README.md").read_text()

    assert "### Environment variable quick reference" in examples_readme
    assert "`BROWSERTRACE_HOME`" in examples_readme
    assert "`BROWSERTRACE_PORT`" in examples_readme
    assert "changes the trace store" in examples_readme
    assert "changes the local UI port" in examples_readme
    assert "@v0.1.14" in examples_readme
    assert "hosted sharing" not in examples_readme


def test_examples_readme_includes_public_safe_attachment_note():
    project_root = Path(__file__).resolve().parents[1]
    examples_readme = (project_root / "examples" / "README.md").read_text()

    assert "### Attach a public-safe export to an issue" in examples_readme
    assert "public.html" in examples_readme
    assert "GitHub issue or PR comment" in examples_readme
    assert "browsertrace export <run_id> --public -o public.html" in examples_readme
    assert "prompt/model I/O, screenshots, and URLs" in examples_readme
    assert "@v0.1.14" in examples_readme
    assert "hosted sharing" not in examples_readme


def test_examples_readme_includes_first_run_troubleshooting_checklist():
    project_root = Path(__file__).resolve().parents[1]
    examples_readme = (project_root / "examples" / "README.md").read_text()

    assert "### First-run troubleshooting checklist" in examples_readme
    assert "browsertrace doctor" in examples_readme
    assert "browsertrace demo" in examples_readme
    assert "browsertrace list" in examples_readme
    assert "browsertrace show <run_id>" in examples_readme
    assert "browsertrace export <run_id> --public -o public.html" in examples_readme
    assert "@v0.1.14" in examples_readme
    assert "hosted sharing" not in examples_readme


def test_examples_readme_includes_command_cheat_sheet():
    project_root = Path(__file__).resolve().parents[1]
    examples_readme = (project_root / "examples" / "README.md").read_text()

    assert "### BrowserTrace command cheat sheet" in examples_readme
    assert "| Command | Use when |" in examples_readme
    assert "`browsertrace doctor`" in examples_readme
    assert "`browsertrace demo`" in examples_readme
    assert "`browsertrace list`" in examples_readme
    assert "`browsertrace show <run_id>`" in examples_readme
    assert "`browsertrace export <run_id> --public -o public.html`" in examples_readme
    assert "@v0.1.14" in examples_readme
    assert "hosted sharing" not in examples_readme


def test_examples_readme_includes_pytest_isolated_storage_recipe():
    project_root = Path(__file__).resolve().parents[1]
    examples_readme = (project_root / "examples" / "README.md").read_text()

    assert "### Testing with isolated trace storage" in examples_readme
    assert "def test_browsertrace_trace_uses_temp_store" in examples_readme
    assert 'monkeypatch.setenv("BROWSERTRACE_HOME", str(tmp_path))' in examples_readme
    assert "Tracer()" in examples_readme
    assert "no browser, network, or API key" in " ".join(examples_readme.split())


def test_examples_readme_includes_github_actions_public_export_artifact_recipe():
    project_root = Path(__file__).resolve().parents[1]
    examples_readme = (project_root / "examples" / "README.md").read_text()

    assert "### GitHub Actions artifact for public-safe exports" in examples_readme
    assert "actions/upload-artifact@v4" in examples_readme
    assert (
        "RUN_ID=$(browsertrace demo | awk -F': ' '/Run ID:/ {print $2}')"
        in examples_readme
    )
    assert 'browsertrace export "$RUN_ID" --public -o public.html' in examples_readme
    assert "BrowserTrace does not upload traces by itself" in examples_readme
    assert (
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.14'
        in examples_readme
    )


def test_examples_readme_includes_gitlab_ci_public_export_artifact_recipe():
    project_root = Path(__file__).resolve().parents[1]
    examples_readme = (project_root / "examples" / "README.md").read_text()

    assert "### GitLab CI artifact for public-safe exports" in examples_readme
    assert "browsertrace-public-export:" in examples_readme
    assert (
        "RUN_ID=$(browsertrace demo | awk -F': ' '/Run ID:/ {print $2}')"
        in examples_readme
    )
    assert 'browsertrace export "$RUN_ID" --public -o public.html' in examples_readme
    assert "artifacts:" in examples_readme
    assert "public.html" in examples_readme
    assert "BrowserTrace does not upload traces by itself" in examples_readme


def test_examples_readme_includes_playwright_sync_snapshot_recipe():
    project_root = Path(__file__).resolve().parents[1]
    examples_readme = (project_root / "examples" / "README.md").read_text()

    assert "### Playwright sync API snapshot" in examples_readme
    assert "from playwright.sync_api import sync_playwright" in examples_readme
    assert "run.snapshot_sync(page, action=\"opened example.com\")" in examples_readme
    assert "sync Playwright" in examples_readme


def test_owner_profile_actions_include_browsertrace_pin_step():
    project_root = Path(__file__).resolve().parents[1]
    owner_docs = {
        "LAUNCH.md": "Pin BrowserTrace",
        "docs/launch/owner-next-actions.md": "Pin BrowserTrace",
        "docs/launch/owner-next-actions.zh-CN.md": "置顶 BrowserTrace",
        "docs/launch/owner-publish-queue.md": "Pin BrowserTrace",
    }

    for relpath, phrase in owner_docs.items():
        text = (project_root / relpath).read_text()
        assert phrase in text, relpath
        assert "aaronlab/browsertrace" in text, relpath
        assert "https://github.com/aaronlab/browsertrace/issues/24" in text, relpath


def test_first_run_docs_include_doctor_command():
    project_root = Path(__file__).resolve().parents[1]
    docs_text = "\n".join(
        [
            (project_root / "README.md").read_text(),
            (project_root / "docs" / "llms.txt").read_text(),
        ]
    )

    assert "browsertrace doctor" in docs_text
    assert "Print local install and trace-store status" in docs_text


def test_llms_txt_points_to_current_contribution_path():
    project_root = Path(__file__).resolve().parents[1]
    llms = (project_root / "docs" / "llms.txt").read_text()

    assert "Good first issue: https://github.com/aaronlab/browsertrace/issues/90" in llms
    assert (
        "Integration request: https://github.com/aaronlab/browsertrace/issues/new?template=integration_request.yml"
        in llms
    )


def test_llms_txt_includes_troubleshooting_prompt_snippet():
    project_root = Path(__file__).resolve().parents[1]
    llms = (project_root / "docs" / "llms.txt").read_text()

    assert "## Troubleshooting Prompt" in llms
    assert "browsertrace doctor" in llms
    assert "browsertrace demo" in llms
    assert "browsertrace list" in llms
    assert "browsertrace show <run_id>" in llms
    assert "browsertrace export <run_id> --public -o public.html" in llms
    assert "Good first issue: https://github.com/aaronlab/browsertrace/issues/90" in llms
    assert "@v0.1.14" in llms
    assert "hosted sharing" not in llms


def test_press_kit_includes_current_trial_and_contribution_paths():
    project_root = Path(__file__).resolve().parents[1]
    press_kit = (project_root / "docs" / "launch" / "press-kit.md").read_text()
    github_spec = (
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.14'
    )

    assert f'uvx --from "{github_spec}" browsertrace doctor' in press_kit
    assert f'uvx --from "{github_spec}" browsertrace demo' in press_kit
    assert "Good first issue: https://github.com/aaronlab/browsertrace/issues/90" in press_kit


def test_core_guides_advertise_llms_txt():
    project_root = Path(__file__).resolve().parents[1]

    for filename in [
        "debug-browser-agent-failure.html",
        "browser-use-debugging.html",
        "stagehand-debugging.html",
        "skyvern-debugging.html",
        "playwright-llm-debugging.html",
        "computer-use-agent-debugging.html",
    ]:
        page = (project_root / "docs" / filename).read_text()
        assert (
            '<link rel="alternate" type="text/plain" title="llms.txt" href="./llms.txt">'
            in page
        ), filename


def test_browser_use_guide_has_troubleshooting_section():
    project_root = Path(__file__).resolve().parents[1]
    page = (project_root / "docs" / "browser-use-debugging.html").read_text()

    assert "Troubleshooting Browser Use traces" in page
    assert "Could not attach to this Agent" in page
    assert "register_new_step_callback" in page
    assert "No screenshots appear" in page
    assert "browsertrace export &lt;run_id&gt; --public -o public.html" in page


def test_browser_use_guide_documents_callback_compatibility():
    project_root = Path(__file__).resolve().parents[1]
    page = (project_root / "docs" / "browser-use-debugging.html").read_text()

    assert "Callback compatibility" in page
    assert "on_step_start" in page
    assert "on_step_end" in page
    assert "register_new_step_callback" in page
    assert "run-hook-only" in page


def test_sitemap_exposes_llms_txt_and_core_discovery_pages():
    project_root = Path(__file__).resolve().parents[1]
    sitemap = (project_root / "docs" / "sitemap.xml").read_text()

    for path in [
        "",
        "llms.txt",
        "debug-browser-agent-failure.html",
        "browser-use-debugging.html",
        "stagehand-debugging.html",
        "skyvern-debugging.html",
        "playwright-llm-debugging.html",
        "computer-use-agent-debugging.html",
        "integrations.html",
        "launch/",
    ]:
        assert f"https://aaronlab.github.io/browsertrace/{path}" in sitemap, path


def test_launch_copy_includes_uvx_github_trial_before_pypi():
    project_root = Path(__file__).resolve().parents[1]
    github_spec = (
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.14'
    )

    for relpath in [
        "docs/launch/channel-copy.md",
        "docs/launch/day-1-publish-packet.md",
        "docs/launch/day-2-show-hn-packet.md",
    ]:
        text = (project_root / relpath).read_text()
        assert f'uvx --from "{github_spec}" browsertrace doctor' in text, relpath
        assert f'uvx --from "{github_spec}" browsertrace demo' in text, relpath
        assert "before pypi publishing is enabled" in text.lower(), relpath


def test_longform_launch_posts_include_uvx_github_trial_before_pypi():
    project_root = Path(__file__).resolve().parents[1]
    github_spec = (
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.14'
    )

    for relpath in [
        "docs/launch/tutorial-post.md",
        "docs/launch/chinese-tutorial-post.md",
        "docs/launch/response-templates.md",
    ]:
        text = (project_root / relpath).read_text()
        assert f'uvx --from "{github_spec}" browsertrace doctor' in text, relpath
        assert f'uvx --from "{github_spec}" browsertrace demo' in text, relpath
        assert "pypi" in text.lower(), relpath


def test_directory_submission_sheet_includes_uvx_trial_before_pypi():
    project_root = Path(__file__).resolve().parents[1]
    github_spec = (
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.14'
    )
    sheet = (project_root / "docs" / "launch" / "directory-submission-sheet.md").read_text()

    assert "before pypi publishing is enabled" in sheet.lower()
    assert f'uvx --from "{github_spec}" browsertrace doctor' in sheet
    assert f'uvx --from "{github_spec}" browsertrace demo' in sheet


def test_product_hunt_packet_includes_current_trial_and_contribution_paths():
    project_root = Path(__file__).resolve().parents[1]
    github_spec = (
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.14'
    )
    packet = (project_root / "docs" / "launch" / "day-4-product-hunt-packet.md").read_text()

    assert f'uvx --from "{github_spec}" browsertrace doctor' in packet
    assert f'uvx --from "{github_spec}" browsertrace demo' in packet
    assert "https://github.com/aaronlab/browsertrace/issues/90" in packet


def test_pull_request_template_prompts_for_real_contributor_details():
    project_root = Path(__file__).resolve().parents[1]
    template = (project_root / ".github" / "PULL_REQUEST_TEMPLATE.md").read_text()

    assert "<summary>" not in template
    assert "Replace every placeholder before requesting review." in template
    assert "Fixes #123 or Refs #123" in template
    assert "I ran `uv run --python 3.11 --extra dev pytest -q`" in template


def test_security_policy_has_private_report_path_without_email_placeholder():
    project_root = Path(__file__).resolve().parents[1]
    policy = (project_root / "SECURITY.md").read_text()
    normalized = " ".join(policy.split())

    assert "private GitHub vulnerability report" in normalized
    assert "open a minimal public issue without exploit details" in normalized
    assert "emailing the maintainer" not in policy
    assert "browsertrace export <run_id> --public -o public.html" in policy


def test_awesome_list_submission_notes_include_trial_and_demo_links():
    project_root = Path(__file__).resolve().parents[1]
    github_spec = (
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.14'
    )
    notes = (
        project_root / "docs" / "launch" / "github-awesome-list-submissions.md"
    ).read_text()

    assert "https://aaronlab.github.io/browsertrace/" in notes
    assert "browsertrace-demo-public.html" in notes
    assert f'uvx --from "{github_spec}" browsertrace doctor' in notes
    assert f'uvx --from "{github_spec}" browsertrace demo' in notes


def test_targeted_outreach_copy_includes_uvx_trial_before_pypi():
    project_root = Path(__file__).resolve().parents[1]
    github_spec = (
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.14'
    )

    for relpath in [
        "docs/launch/day-3-targeted-communities-packet.md",
        "docs/launch/outreach-targets.md",
    ]:
        text = (project_root / relpath).read_text()
        assert f'uvx --from "{github_spec}" browsertrace doctor' in text, relpath
        assert f'uvx --from "{github_spec}" browsertrace demo' in text, relpath
        assert "before pypi publishing is enabled" in text.lower(), relpath


def test_owner_next_actions_include_uvx_fallback_before_pypi():
    project_root = Path(__file__).resolve().parents[1]
    github_spec = (
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.14'
    )

    for relpath in [
        "docs/launch/owner-next-actions.md",
        "docs/launch/owner-next-actions.zh-CN.md",
    ]:
        text = (project_root / relpath).read_text()
        assert f'uvx --from "{github_spec}" browsertrace demo' in text, relpath
        assert "pypi" in text.lower(), relpath


def test_launch_control_room_has_current_audit_and_uvx_fallback():
    project_root = Path(__file__).resolve().parents[1]
    github_spec = (
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.14'
    )
    launch = (project_root / "LAUNCH.md").read_text()

    assert "2026-05-09T23:41:26+00:00" in launch
    assert "after issue #89 closed and good-first issue #90 rotation" in launch
    assert f'uvx --from "{github_spec}" browsertrace doctor' in launch
    assert f'uvx --from "{github_spec}" browsertrace demo' in launch
