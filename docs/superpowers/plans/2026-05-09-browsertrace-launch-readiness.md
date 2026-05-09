# BrowserTrace Launch Readiness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make BrowserTrace correct, demoable, and launch-ready as the primary `aaronlab` AI open-source project for a 1000-star growth push.

**Architecture:** Keep the existing small architecture: dependency-light SDK core, SQLite/filesystem storage, optional FastAPI/Jinja UI, and CLI commands. The plan avoids a rewrite and focuses on the first-user path: install, create a failed trace, view it locally, export it, and understand the project from the README.

**Tech Stack:** Python 3.11+, pytest, uv, SQLite, FastAPI, Jinja2, argparse, Markdown documentation.

---

## File Structure

- Modify `browsertrace/cli.py`: fix Python 3.11 f-string SyntaxError in HTML export.
- Modify `tests/test_cli.py`: add an explicit compile/import guard for the CLI module.
- Create `examples/no_api_failure_demo.py`: deterministic demo that creates a failed trace without Playwright, network, or API keys.
- Create `tests/test_examples.py`: test that the deterministic demo writes the expected failed run and failed step.
- Modify `README.md`: sharpen first screen, quickstart, deterministic demo instructions, and launch positioning.
- Modify `LAUNCH.md`: add a launch-readiness checklist and update the copy to point at the deterministic demo and final verification commands.

## Task 1: Fix Python 3.11 CLI Import

**Files:**
- Modify: `tests/test_cli.py`
- Modify: `browsertrace/cli.py`

- [ ] **Step 1: Add an explicit failing compile guard**

Add these imports near the top of `tests/test_cli.py`:

```python
import py_compile
from pathlib import Path
```

Add this test after `_seed(...)`:

```python
def test_cli_module_compiles_on_python311():
    """Guard against Python 3.11 f-string syntax regressions.

    The package supports Python 3.11, so CLI source must parse on 3.11 before
    any import-time tests can run.
    """
    root = Path(__file__).resolve().parents[1]
    py_compile.compile(str(root / "browsertrace" / "cli.py"), doraise=True)
```

- [ ] **Step 2: Run the new guard and verify it fails**

Run:

```bash
uv run --python 3.11 --extra dev pytest tests/test_cli.py::test_cli_module_compiles_on_python311 -q
```

Expected result before implementation:

```text
SyntaxError: f-string expression part cannot include a backslash
```

- [ ] **Step 3: Fix the export HTML f-string**

In `browsertrace/cli.py`, replace the export loop block around the fallback
image HTML with this version:

```python
    no_screenshot_html = (
        '<div style="color:#6b7280;text-align:center;padding:48px">'
        "no screenshot"
        "</div>"
    )

    for s in steps:
        is_err = (s["status"] or "ok") != "ok"
        klass = "step error" if is_err else "step"
        badge = "error" if is_err else "ok"
        img_html = ""
        if s["screenshot_path"] and Path(s["screenshot_path"]).exists():
            data = base64.b64encode(Path(s["screenshot_path"]).read_bytes()).decode()
            img_html = f"<img src='data:image/png;base64,{data}' alt='step {s['step_index']}'>"
        parts.append(
            f"<div class='{klass}'>"
            f"<div>{img_html or no_screenshot_html}</div>"
            f"<div>"
            f"<div style='font-size:11px;color:#6b7280;font-weight:600'>STEP {s['step_index']}</div>"
            f"<div style='font-size:15px'>{_html_escape(s['action'] or '')} <span class='badge {badge}'>{s['status'] or 'ok'}</span></div>"
            f"<div style='font-size:12px;color:#6b7280'><code>{_html_escape(s['url'] or '')}</code></div>"
        )
```

- [ ] **Step 4: Verify the targeted guard passes**

Run:

```bash
uv run --python 3.11 --extra dev pytest tests/test_cli.py::test_cli_module_compiles_on_python311 -q
```

Expected result:

```text
1 passed
```

- [ ] **Step 5: Verify all CLI tests pass**

Run:

```bash
uv run --python 3.11 --extra dev pytest tests/test_cli.py -q
```

Expected result:

```text
6 passed
```

- [ ] **Step 6: Commit the CLI fix**

Run:

```bash
git add browsertrace/cli.py tests/test_cli.py
rm -f uv.lock
git commit -m "fix: support CLI import on Python 3.11"
```

## Task 2: Add Deterministic No-API Failure Demo

**Files:**
- Create: `examples/no_api_failure_demo.py`
- Create: `tests/test_examples.py`

- [ ] **Step 1: Write the failing example test**

Create `tests/test_examples.py` with this content:

```python
"""Tests for launch demo scripts."""

from __future__ import annotations

import runpy
import sqlite3


def test_no_api_failure_demo_creates_failed_trace(tmp_path, monkeypatch):
    monkeypatch.setenv("BROWSERTRACE_HOME", str(tmp_path))

    runpy.run_path("examples/no_api_failure_demo.py", run_name="__main__")

    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        run = c.execute(
            "SELECT id, name, status, error FROM runs ORDER BY started_at DESC LIMIT 1"
        ).fetchone()
        steps = c.execute(
            "SELECT step_index, action, status, error, model_output "
            "FROM steps WHERE run_id=? ORDER BY step_index",
            (run[0],),
        ).fetchall()

    assert run[1] == "demo: checkout agent fails on disabled button"
    assert run[2] == "failed"
    assert "RuntimeError" in run[3]
    assert len(steps) == 4
    assert steps[3][1] == "click disabled checkout button"
    assert steps[3][2] == "error"
    assert "button was disabled" in steps[3][3]
    assert "button.checkout.primary" in steps[3][4]
```

- [ ] **Step 2: Run the example test and verify it fails because the demo does not exist**

Run:

```bash
uv run --python 3.11 --extra dev pytest tests/test_examples.py::test_no_api_failure_demo_creates_failed_trace -q
```

Expected result:

```text
FileNotFoundError: [Errno 2] No such file or directory: 'examples/no_api_failure_demo.py'
```

- [ ] **Step 3: Create the deterministic demo**

Create `examples/no_api_failure_demo.py` with this content:

```python
"""Deterministic BrowserTrace demo with no browser, network, or API key.

Run:
    python examples/no_api_failure_demo.py
    browsertrace

Then open http://127.0.0.1:3000 and click
"demo: checkout agent fails on disabled button".
"""

from __future__ import annotations

import base64

from browsertrace import Tracer


PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII="
)


def main() -> None:
    tracer = Tracer()

    try:
        with tracer.run("demo: checkout agent fails on disabled button") as run:
            run.step(
                action="open checkout page",
                url="https://shop.example.test/checkout",
                screenshot=PNG_1X1,
                model_input={
                    "task": "Complete checkout for the current cart.",
                    "observation": "Checkout page loaded.",
                },
                model_output={
                    "thought": "I need to inspect the checkout form before submitting.",
                    "next_action": "inspect form",
                },
            )
            run.step(
                action="inspect payment form",
                url="https://shop.example.test/checkout",
                screenshot=PNG_1X1,
                model_input={
                    "visible_fields": ["email", "card", "shipping"],
                    "button_text": "Place order",
                },
                model_output={
                    "thought": "All fields appear complete. I should click the primary checkout button.",
                    "selector": "button.checkout.primary",
                    "next_action": "click",
                },
            )
            run.step(
                action="model selects checkout button",
                url="https://shop.example.test/checkout",
                screenshot=PNG_1X1,
                model_input={
                    "dom_snippet": "<button class='checkout primary' disabled>Place order</button>",
                },
                model_output={
                    "thought": "The primary checkout button is the correct target.",
                    "selector": "button.checkout.primary",
                    "risk": "The model missed the disabled attribute.",
                },
            )
            failed_step = run.step(
                action="click disabled checkout button",
                url="https://shop.example.test/checkout",
                screenshot=PNG_1X1,
                model_input={"selector": "button.checkout.primary"},
                model_output={
                    "action": "click",
                    "selector": "button.checkout.primary",
                    "expected": "Order confirmation page",
                },
            )
            try:
                raise RuntimeError("button was disabled; click did not submit the form")
            except RuntimeError as exc:
                run.update_step(
                    failed_step,
                    status="error",
                    error=f"{type(exc).__name__}: {exc}",
                )
                raise
    except RuntimeError as exc:
        print(f"Run failed as expected: {type(exc).__name__}: {exc}")

    print("Done. Run `browsertrace` and open http://127.0.0.1:3000")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Verify the example test passes**

Run:

```bash
uv run --python 3.11 --extra dev pytest tests/test_examples.py -q
```

Expected result:

```text
1 passed
```

- [ ] **Step 5: Manually verify the demo creates traces in an isolated home**

Run:

```bash
rm -rf /tmp/browsertrace-demo
BROWSERTRACE_HOME=/tmp/browsertrace-demo uv run --python 3.11 python examples/no_api_failure_demo.py
BROWSERTRACE_HOME=/tmp/browsertrace-demo uv run --python 3.11 --extra dev python -m browsertrace.cli list
```

Expected output contains:

```text
demo: checkout agent fails on disabled button
```

- [ ] **Step 6: Commit the deterministic demo**

Run:

```bash
git add examples/no_api_failure_demo.py tests/test_examples.py
rm -f uv.lock
git commit -m "feat: add deterministic failure demo"
```

## Task 3: Polish README First-Run Path

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Replace the opening section through "See it in 60 seconds"**

Replace the top of `README.md`, from `# BrowserTrace` through the current
`See it in 60 seconds` section, with:

```markdown
# BrowserTrace

> Local flight recorder for AI browser agents.

![demo](docs/demo.gif)

**MIT · local-first · no signup · no cloud · Python 3.11+**

Your AI browser agent failed. Logs say what code ran, but not what the agent
actually saw, clicked, or decided.

BrowserTrace records each browser-agent step as a timeline: screenshot, URL,
action, model input, model output, status, and error. Open the local UI and jump
straight to the failure.

Built for Browser Use, Stagehand, Playwright + LLM scripts, and custom
computer-use agents.

## Install

```bash
# SDK only
pip install git+https://github.com/aaronlab/browsertrace

# SDK + local web UI
pip install "browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace"
```

## See a failure trace in 60 seconds

```bash
git clone https://github.com/aaronlab/browsertrace
cd browsertrace
pip install -e ".[ui]"
python examples/no_api_failure_demo.py
browsertrace
```

Open `http://127.0.0.1:3000`, click
`demo: checkout agent fails on disabled button`, and inspect the failed step.

For a real browser demo with screenshots from Wikipedia:

```bash
pip install playwright
playwright install chromium
python examples/multipage_failure.py
browsertrace
```
```

- [ ] **Step 2: Update the examples pointer under "Playwright"**

Replace:

```markdown
See `examples/playwright_example.py` and `examples/multipage_failure.py`.
```

With:

```markdown
See `examples/playwright_example.py`, `examples/failure_example.py`, and
`examples/multipage_failure.py`. If you want a no-browser deterministic demo,
run `examples/no_api_failure_demo.py`.
```

- [ ] **Step 3: Update the roadmap status lines**

Replace the roadmap block with:

```markdown
## Roadmap

- [x] **v0.1**: SDK + local UI + screenshots + model I/O + step status
- [x] **CLI export**: `browsertrace export <run_id>` static HTML bundle
- [x] **Search/filter**: Filter the run list by status and query text
- [x] **AI summaries**: Optional OpenAI-compatible root-cause endpoint
- [ ] **Multi-run comparison**: "Did this regression appear after my last commit?"
- [ ] **First-class Skyvern adapter**
- [ ] **Optional cloud share links**
```

- [ ] **Step 4: Verify README mentions the deterministic demo**

Run:

```bash
rg -n "no_api_failure_demo|Local flight recorder|See a failure trace in 60 seconds" README.md
```

Expected output contains all three patterns.

- [ ] **Step 5: Commit the README polish**

Run:

```bash
git add README.md
git commit -m "docs: sharpen BrowserTrace launch README"
```

## Task 4: Refresh Launch Checklist

**Files:**
- Modify: `LAUNCH.md`

- [ ] **Step 1: Add launch readiness checklist at the top**

Insert this section immediately after `# BrowserTrace launch`:

```markdown
## Launch readiness gates

- [ ] `uv run --python 3.11 --extra dev pytest -q` passes.
- [ ] `python examples/no_api_failure_demo.py` creates a failed run without API keys.
- [ ] `browsertrace list` shows the deterministic demo run.
- [ ] `browsertrace export <run_id> -o demo.html` creates a standalone HTML report.
- [ ] README first screen shows the value prop, GIF/screenshot, install, and 60-second demo.
- [ ] GitHub repo has description, topics, MIT license, and `v0.1.10` release.
- [ ] Demo GIF is under 60 seconds and shows the failed-step timeline.
- [ ] Show HN copy points to the repo and mentions no signup, no cloud, local-first.
```

- [ ] **Step 2: Update the asset checklist**

Replace the current `配套素材清单` section with:

```markdown
## 配套素材清单

要发推之前必须准备：

- [ ] **demo GIF**：30-60 秒，展示
  - 运行 `python examples/no_api_failure_demo.py`
  - 运行 `browsertrace`
  - 打开 `localhost:3000`
  - 进入失败 run
  - 展开 failed step 的 model output

- [ ] **真实浏览器 GIF**：可选但推荐，展示
  - 运行 `python examples/multipage_failure.py`
  - Wikipedia 搜索 Tokyo
  - timeline 跳到失败 selector

- [ ] **README 第一屏**：必须有
  - hero GIF 或 screenshot
  - 本地优先、无注册、无云
  - 60 秒 demo
  - Browser Use / Stagehand / Playwright 关键词

- [ ] **GitHub repo 首页**：必须有
  - description
  - topics: `ai-agents`, `browser-automation`, `observability`, `debugging`, `llm`, `playwright`
  - MIT license
  - `v0.1.10` release
```

- [ ] **Step 3: Verify launch checklist mentions final commands**

Run:

```bash
rg -n "uv run --python 3.11|no_api_failure_demo|v0.1.10|Show HN" LAUNCH.md
```

Expected output contains all four patterns.

- [ ] **Step 4: Commit launch checklist refresh**

Run:

```bash
git add LAUNCH.md
git commit -m "docs: refresh BrowserTrace launch checklist"
```

## Task 5: Full Verification and Completion Audit

**Files:**
- No source files should be modified in this task unless verification exposes a bug.

- [ ] **Step 1: Run the full Python 3.11 test suite**

Run:

```bash
uv run --python 3.11 --extra dev pytest -q
```

Expected result:

```text
49 passed
```

If the exact count differs because a task added or removed tests, the result
must still show no failures, no errors, and no skipped launch-readiness tests.

- [ ] **Step 2: Verify package build metadata**

Run:

```bash
rm -rf dist
uv build
ls dist
rm -rf dist
```

Expected result contains:

```text
Successfully built dist/browsertrace-0.1.0
```

- [ ] **Step 3: Verify deterministic demo and CLI list**

Run:

```bash
rm -rf /tmp/browsertrace-demo
BROWSERTRACE_HOME=/tmp/browsertrace-demo uv run --python 3.11 python examples/no_api_failure_demo.py
BROWSERTRACE_HOME=/tmp/browsertrace-demo uv run --python 3.11 --extra dev python -m browsertrace.cli list
```

Expected output contains:

```text
demo: checkout agent fails on disabled button
```

- [ ] **Step 4: Verify HTML export**

Run:

```bash
RUN_ID="$(BROWSERTRACE_HOME=/tmp/browsertrace-demo uv run --python 3.11 --extra dev python -m browsertrace.cli list | awk 'NR==1 {print $1}')"
BROWSERTRACE_HOME=/tmp/browsertrace-demo uv run --python 3.11 --extra dev python -m browsertrace.cli export "$RUN_ID" -o /tmp/browsertrace-demo.html
test -s /tmp/browsertrace-demo.html
rg -n "checkout agent fails|data:image/png;base64|button.checkout.primary" /tmp/browsertrace-demo.html
```

Expected output includes all three searched strings.

- [ ] **Step 5: Confirm worktree cleanliness**

Run:

```bash
git status --short
```

Expected output is empty.

If `uv.lock` exists only because `uv run` generated it during verification,
remove it before re-running the cleanliness check:

```bash
rm -f uv.lock
git status --short
```

- [ ] **Step 6: Audit the active 1000-star objective**

Run:

```bash
gh repo view aaronlab/browsertrace --json name,owner,visibility,stargazerCount,repositoryTopics,licenseInfo
```

Expected audit interpretation:

- Repo owner is `aaronlab`.
- Repo visibility is public.
- Repo is AI-related by description/topics and project content.
- Star count is checked from GitHub now.
- If `stargazerCount` is 1000 or lower, the active thread goal is not complete.
- Do not call `update_goal` unless `stargazerCount` is greater than 1000.

- [ ] **Step 7: Commit verification notes only if a tracked verification artifact was intentionally created**

If no tracked files changed during verification, do not create a commit.
