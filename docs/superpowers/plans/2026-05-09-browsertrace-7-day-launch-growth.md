# BrowserTrace 7-Day Launch Growth Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prepare and run a legitimate 7-day launch system for `aaronlab/browsertrace` so the project can grow toward 1000+ GitHub stars.

**Architecture:** Keep growth assets inside the repository so they can be reviewed, reused, and updated as feedback arrives. The plan separates demo reliability, launch copy, visual assets, community outreach, and audit loops so each piece can ship independently.

**Tech Stack:** Python 3.11, pytest, Playwright for demo capture, GitHub CLI, Markdown launch docs.

---

## File Structure

- Modify `scripts/record_demo.py`: remove the stale hardcoded run ID and resolve the latest failed run from the local BrowserTrace API.
- Use existing `tests/test_record_demo_script.py`: cover environment override and API lookup behavior for the recorder.
- Rewrite `LAUNCH.md`: make it the owner-facing control room with current gates, posting schedule, launch checklist, and exact publish steps.
- Create `docs/launch/channel-copy.md`: channel-specific copy for X, LinkedIn, Hacker News, Product Hunt, Reddit, WeChat, Jike, and Xiaohongshu.
- Create `docs/launch/response-templates.md`: concise replies for likely launch comments and objections.
- Create `docs/launch/outreach-targets.md`: targeted communities and the one relevant ask for each.
- Create `docs/launch/tutorial-post.md`: long-form post draft explaining how to debug a browser-agent failure with BrowserTrace.
- Create `docs/social-preview.svg`: editable source artwork for a GitHub/Product Hunt social preview card.
- Generate `docs/social-preview.png` if a local converter is available; otherwise leave SVG source and record the conversion gap in `LAUNCH.md`.

---

### Task 1: Make Demo Recorder Reusable

**Files:**
- Modify: `scripts/record_demo.py`
- Test: `tests/test_record_demo_script.py`

- [ ] **Step 1: Run the targeted recorder tests and confirm the current failure**

Run:

```bash
uv run --python 3.11 --extra dev pytest tests/test_record_demo_script.py -q
```

Expected: failure because `scripts.record_demo.resolve_demo_run_id` is not defined.

- [ ] **Step 2: Update imports and constants**

In `scripts/record_demo.py`, replace the import block and remove `TOKYO_RUN_ID`:

```python
import asyncio
import json
import os
import shutil
import time
import urllib.request
from pathlib import Path

from playwright.async_api import async_playwright

BASE = "http://127.0.0.1:3000"
FRAMES = Path("/tmp/bt-frames")
FPS = 15
WIDTH, HEIGHT = 1280, 800
```

- [ ] **Step 3: Add dynamic run resolution**

Add this function above `main()`:

```python
def resolve_demo_run_id(base: str = BASE) -> str:
    override = os.environ.get("BROWSERTRACE_DEMO_RUN_ID")
    if override:
        return override

    url = f"{base}/api/runs?status=failed&limit=1"
    with urllib.request.urlopen(url) as resp:
        payload = json.loads(resp.read().decode("utf-8"))

    runs = payload.get("runs") or []
    if not runs:
        raise RuntimeError(
            "No failed BrowserTrace runs found. Run "
            "`python examples/no_api_failure_demo.py` or set "
            "BROWSERTRACE_DEMO_RUN_ID."
        )
    return runs[0]["id"]
```

- [ ] **Step 4: Use the resolved run ID in `main()`**

Inside `main()`, before navigating to the run detail page, add:

```python
        run_id = resolve_demo_run_id(BASE)
```

Then replace:

```python
        await page.goto(f"{BASE}/run/{TOKYO_RUN_ID}")
```

with:

```python
        await page.goto(f"{BASE}/run/{run_id}")
```

- [ ] **Step 5: Update the docstring**

Replace Tokyo-specific wording with:

```python
"""Record a demo GIF of BrowserTrace by driving a real browser with Playwright.

Captures frames at ~15fps while:
  1. Showing the runs index
  2. Opening the latest failed run, or BROWSERTRACE_DEMO_RUN_ID if set
  3. Slowly scrolling the timeline top -> bottom

Output: /tmp/bt-frames/*.png  ->  combined later with gifski.
"""
```

- [ ] **Step 6: Verify and commit**

Run:

```bash
uv run --python 3.11 --extra dev pytest tests/test_record_demo_script.py -q
uv run --python 3.11 --extra dev pytest -q
git add scripts/record_demo.py tests/test_record_demo_script.py
git commit -m "fix: make demo recorder select failed run dynamically"
```

Expected: targeted tests pass and full suite passes.

---

### Task 2: Build the Launch Control Room

**Files:**
- Modify: `LAUNCH.md`
- Create: `docs/launch/channel-copy.md`
- Create: `docs/launch/response-templates.md`
- Create: `docs/launch/outreach-targets.md`
- Create: `docs/launch/tutorial-post.md`

- [ ] **Step 1: Rewrite `LAUNCH.md` structure**

Replace the current draft-style document with these sections:

```markdown
# BrowserTrace Launch Control Room

## Current State

## Day 0 Asset Checklist

## 7-Day Posting Calendar

## Owner-Only Actions

## Daily Metrics

## Launch Gates

## Links
```

The document must include the canonical repo URL `https://github.com/aaronlab/browsertrace`, the current release `v0.1.10`, and the current star count audit command:

```bash
gh repo view aaronlab/browsertrace --json stargazerCount,url,homepageUrl,owner
```

- [ ] **Step 2: Create channel copy**

Create `docs/launch/channel-copy.md` with exact ready-to-post drafts for:

- X short story post.
- LinkedIn technical post.
- Hacker News title and body.
- Product Hunt tagline, description, maker comment, and first comment.
- Reddit value-first post.
- WeChat group message.
- Jike post.
- Xiaohongshu post.

All drafts must ask for feedback, not upvotes or stars.

- [ ] **Step 3: Create response templates**

Create `docs/launch/response-templates.md` with responses for:

- "How is this different from Langfuse/LangSmith?"
- "How is this different from Browserbase recordings?"
- "Does data leave my machine?"
- "Does it work with Browser Use?"
- "Does it work with Stagehand?"
- "Can I share traces with a teammate?"
- "Why no PyPI install yet?"
- "I found a bug."
- "This is too early."

- [ ] **Step 4: Create outreach target list**

Create `docs/launch/outreach-targets.md` with columns:

```markdown
| Channel | Audience | Suggested timing | Post type | Owner action | Notes |
```

Include Hacker News, Product Hunt, X, LinkedIn, Browser Use community,
Stagehand community, Playwright community, Skyvern users, Reddit, WeChat, Jike,
and Xiaohongshu.

- [ ] **Step 5: Create tutorial post draft**

Create `docs/launch/tutorial-post.md` with a complete long-form draft titled:

```markdown
# How to Debug an AI Browser Agent Failure with Screenshots and Model I/O
```

It must include a failure story, install commands, demo commands, what to inspect
in the timeline, and a final link to `https://github.com/aaronlab/browsertrace`.

- [ ] **Step 6: Verify and commit**

Run:

```bash
rg -n "aaronlab/browsertrace|v0.1.10|Show HN|Product Hunt|Owner-Only|Daily Metrics" LAUNCH.md docs/launch
rg -n "upvote|stars please|vote for us" LAUNCH.md docs/launch
git add LAUNCH.md docs/launch
git commit -m "docs: add BrowserTrace launch control room"
```

Expected: first command finds the launch assets; second command returns no direct vote-solicitation copy except explanatory anti-spam text if present.

---

### Task 3: Add Social Preview Artwork

**Files:**
- Create: `docs/social-preview.svg`
- Optional generated: `docs/social-preview.png`
- Modify: `LAUNCH.md`

- [ ] **Step 1: Create SVG source**

Create a 1280 x 640 SVG with:

- Title: `BrowserTrace`
- Subtitle: `Local flight recorder for AI browser agents`
- Three feature pills: `Screenshots`, `Model I/O`, `Failure timeline`
- Footer: `github.com/aaronlab/browsertrace`

Use a restrained dark background, bright timeline accents, and no external
fonts or images.

- [ ] **Step 2: Try PNG generation**

Run one of these if available:

```bash
rsvg-convert docs/social-preview.svg -o docs/social-preview.png
```

or:

```bash
magick docs/social-preview.svg docs/social-preview.png
```

or use Playwright to screenshot the SVG in a browser if neither converter is
available.

- [ ] **Step 3: Verify image size**

Run:

```bash
ls -lh docs/social-preview.*
```

Expected: SVG exists. If PNG exists, it is under 1 MB.

- [ ] **Step 4: Update `LAUNCH.md` with owner upload step**

Add this owner-only action:

```markdown
- Upload `docs/social-preview.png` as the GitHub repository social preview in
  Settings -> Social preview. If PNG generation is unavailable, use
  `docs/social-preview.svg` as source for a manual export first.
```

- [ ] **Step 5: Commit**

Run:

```bash
git add docs/social-preview.svg docs/social-preview.png LAUNCH.md
git commit -m "docs: add BrowserTrace social preview asset"
```

If `docs/social-preview.png` does not exist, omit it from `git add` and include
the conversion gap in the commit body.

---

### Task 4: Run Launch Readiness Audit

**Files:**
- Modify: `LAUNCH.md` if audit results reveal stale information.

- [ ] **Step 1: Verify tests**

Run:

```bash
uv run --python 3.11 --extra dev pytest -q
```

Expected: full test suite passes.

- [ ] **Step 2: Verify repo metadata**

Run:

```bash
gh repo view aaronlab/browsertrace --json name,owner,visibility,stargazerCount,repositoryTopics,licenseInfo,description,url,homepageUrl
```

Expected: owner is `aaronlab`, visibility is `PUBLIC`, license is MIT, URL and
homepage are canonical, and the star count is current.

- [ ] **Step 3: Verify CI**

Run:

```bash
gh run list --limit 3 --json databaseId,workflowName,status,conclusion,headSha,url
```

Expected: latest run on `main` is completed successfully or still in progress
for the latest pushed commit.

- [ ] **Step 4: Verify release**

Run:

```bash
gh release view v0.1.10 --json tagName,name,isDraft,isPrerelease,assets,url
```

Expected: `v0.1.10` exists and includes wheel, sdist, and demo HTML assets.

- [ ] **Step 5: Commit audit updates if needed**

If `LAUNCH.md` needed corrections, run:

```bash
git add LAUNCH.md
git commit -m "docs: update BrowserTrace launch audit"
```

---

### Task 5: Push and Monitor

**Files:**
- No planned file edits unless CI or audits reveal a problem.

- [ ] **Step 1: Push all commits**

Run:

```bash
git status --short --branch
git push origin main
```

Expected: only unrelated untracked or user-owned files remain, and `main` pushes.

- [ ] **Step 2: Monitor CI**

Run:

```bash
gh run list --limit 5 --json databaseId,workflowName,status,conclusion,headSha,url
```

If the latest run is in progress, wait until it completes.

- [ ] **Step 3: Audit star count**

Run:

```bash
gh repo view aaronlab/browsertrace --json stargazerCount,url
```

Expected: current star count is recorded. Do not mark the active goal complete
unless `stargazerCount > 1000`.

- [ ] **Step 4: Present owner publishing queue**

Report the exact files and actions the owner should publish from:

- `docs/launch/channel-copy.md`
- `docs/launch/outreach-targets.md`
- `docs/launch/response-templates.md`
- `LAUNCH.md`

The report must clearly separate actions Codex completed from actions requiring
the owner to log in and click publish.
