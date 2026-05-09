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

    assert pyproject["project"]["version"] == "0.1.13"
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
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.13'
    )
    assert f'uvx --from "{github_spec}" browsertrace demo' in docs_text
    assert f'uvx --from "{github_spec}" browsertrace list' in docs_text
    assert "before PyPI publishing is enabled" in docs_text


def test_owner_launch_checklists_include_doctor_fallback_before_pypi():
    project_root = Path(__file__).resolve().parents[1]
    github_spec = (
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.13'
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
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.13'
    )
    profile_draft = (
        project_root / "docs" / "launch" / "github-profile-readme.md"
    ).read_text()

    assert "https://github.com/aaronlab/browsertrace" in profile_draft
    assert "https://aaronlab.github.io/browsertrace/computer-use-agent-debugging.html" in profile_draft
    assert f'uvx --from "{github_spec}" browsertrace doctor' in profile_draft
    assert f'uvx --from "{github_spec}" browsertrace demo' in profile_draft
    assert "https://github.com/aaronlab/browsertrace/issues/3" in profile_draft
    assert "https://github.com/aaronlab/browsertrace/issues/28" in profile_draft


def test_readme_has_public_safe_export_sharing_example():
    project_root = Path(__file__).resolve().parents[1]
    readme = (project_root / "README.md").read_text()

    assert "## Share A Public-Safe Trace" in readme
    assert "browsertrace demo" in readme
    assert "browsertrace list" in readme
    assert "browsertrace export <run_id> --public -o public.html" in readme
    assert "prompts/model I/O, screenshots, and URLs" in readme
    assert "hosted upload" in readme


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

    assert "Good first issue: https://github.com/aaronlab/browsertrace/issues/28" in llms
    assert (
        "Integration request: https://github.com/aaronlab/browsertrace/issues/new?template=integration_request.yml"
        in llms
    )


def test_press_kit_includes_current_trial_and_contribution_paths():
    project_root = Path(__file__).resolve().parents[1]
    press_kit = (project_root / "docs" / "launch" / "press-kit.md").read_text()
    github_spec = (
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.13'
    )

    assert f'uvx --from "{github_spec}" browsertrace doctor' in press_kit
    assert f'uvx --from "{github_spec}" browsertrace demo' in press_kit
    assert "Good first issue: https://github.com/aaronlab/browsertrace/issues/28" in press_kit


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
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.13'
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
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.13'
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
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.13'
    )
    sheet = (project_root / "docs" / "launch" / "directory-submission-sheet.md").read_text()

    assert "before pypi publishing is enabled" in sheet.lower()
    assert f'uvx --from "{github_spec}" browsertrace doctor' in sheet
    assert f'uvx --from "{github_spec}" browsertrace demo' in sheet


def test_product_hunt_packet_includes_current_trial_and_contribution_paths():
    project_root = Path(__file__).resolve().parents[1]
    github_spec = (
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.13'
    )
    packet = (project_root / "docs" / "launch" / "day-4-product-hunt-packet.md").read_text()

    assert f'uvx --from "{github_spec}" browsertrace doctor' in packet
    assert f'uvx --from "{github_spec}" browsertrace demo' in packet
    assert "https://github.com/aaronlab/browsertrace/issues/28" in packet


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
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.13'
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
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.13'
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
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.13'
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
        'browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.13'
    )
    launch = (project_root / "LAUNCH.md").read_text()

    assert "2026-05-09T18:24:18+00:00" in launch
    assert "after Browser Use model input context update for issue #11" in launch
    assert f'uvx --from "{github_spec}" browsertrace doctor' in launch
    assert f'uvx --from "{github_spec}" browsertrace demo' in launch
