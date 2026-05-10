# BrowserTrace GitHub Awesome List Submissions

Curated GitHub lists can bring qualified developer discovery, but only when the
project is a real fit. Submit one focused PR per list, follow each maintainer's
format, and do not ask for stars.

Tracking issue: https://github.com/aaronlab/browsertrace/issues/18

## Reviewer Links And Trial Path

Use these links only when a maintainer asks for more context. Keep the PR itself
small and formatted to the target list.

- Live demo: https://aaronlab.github.io/browsertrace/
- Public-safe demo export: https://github.com/aaronlab/browsertrace/releases/download/v0.1.14/browsertrace-demo-public.html
- Release: https://github.com/aaronlab/browsertrace/releases/tag/v0.1.14

Before PyPI publishing is enabled, the lightest local trial is:

```bash
uvx --from "browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.14" browsertrace doctor
uvx --from "browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.14" browsertrace demo
uvx --from "browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.14" browsertrace
```

## Contribution Reply

If a maintainer or list reader asks how to make a small docs fix, point to the
current good first issue:
https://github.com/aaronlab/browsertrace/issues/219

Then share the First PR Recipe:
https://github.com/aaronlab/browsertrace/blob/main/CONTRIBUTING.md#first-pr-recipe keeps the first contribution small and reviewable.

## Troubleshooting Reply

For awesome-list reviewer follow-up, local first-run issues, CI failures, or AI/coding-agent troubleshooting replies, ask for debugging/workflow details plus JSON CLI diagnostics when safe to share:

```bash
browsertrace doctor --json
browsertrace list --status failed --json
browsertrace show <run_id> --json
```

## Recommended Order

| Priority | Target | Fit | Section | Owner action |
|---:|---|---|---|---|
| 1 | `angrykoala/awesome-browser-automation` | Strong | `Tools` -> `AI` | Submitted: https://github.com/angrykoala/awesome-browser-automation/pull/112 |
| 2 | `mxschmitt/awesome-playwright` | Medium | `Utils` | Submitted: https://github.com/mxschmitt/awesome-playwright/pull/136 |
| 3 | `Jenqyang/Awesome-AI-Agents` | Medium | `Applications` -> `Tools` | Submitted: https://github.com/Jenqyang/Awesome-AI-Agents/pull/220 |
| 4 | `wjhou/awesome-computer-use-agents` | Strong | `frameworks/README.md` -> `Web/Browser Frameworks` | Submitted: https://github.com/wjhou/awesome-computer-use-agents/pull/2 |
| 5 | `cdxeve/awesome-computer-use-agents` | Strong | `GUI-Based Agents` -> `Web Agents` | Submitted: https://github.com/cdxeve/awesome-computer-use-agents/pull/2 |
| Skip | `e2b-dev/awesome-ai-agents` | Weak | n/a | Main list is for agents, not tools |

## 1. Awesome Browser Automation

Target:

```text
https://github.com/angrykoala/awesome-browser-automation
```

Status: submitted as https://github.com/angrykoala/awesome-browser-automation/pull/112.

Contribution rules observed:

- Use `[tool|resource](link) - Description.`
- One pull request per suggestion.
- Additions should be alphabetical in the relevant category.
- AI-focused browser automation tools belong under `Tools` -> `AI`.
- Description should be short, descriptive, capitalized, and end with a period.

Suggested entry:

```markdown
* [BrowserTrace](https://github.com/aaronlab/browsertrace) - Local flight recorder for AI browser agents with step timelines, screenshots, model I/O, errors, and public-safe HTML exports.
```

Suggested PR title:

```text
Add BrowserTrace to AI browser automation tools
```

Suggested PR body:

```text
Adds BrowserTrace under the AI section.

BrowserTrace is a local debugging tool for AI browser-agent runs. It records
failed Browser Use, Stagehand, Skyvern, Playwright + LLM, and custom
computer-use runs as step timelines with screenshots, URLs, actions, model
input/output, status, errors, and standalone HTML exports.

I placed it in the AI section because it is specifically for AI-driven browser
automation and browser-agent debugging.
```

## 2. Awesome Playwright

Target:

```text
https://github.com/mxschmitt/awesome-playwright
```

Status: submitted as https://github.com/mxschmitt/awesome-playwright/pull/136.

Fit notes:

- BrowserTrace is not a Playwright Test reporter.
- It is useful for Playwright scripts that include LLM decisions or browser
  agents.
- Submit only if the PR clearly frames it as Playwright + LLM debugging tooling.

Suggested section:

```text
Utils
```

Suggested entry:

```markdown
- [BrowserTrace](https://github.com/aaronlab/browsertrace) - Local trace viewer for Playwright + LLM browser-agent runs with screenshots, URLs, model I/O, errors, and shareable HTML exports.
```

Suggested PR title:

```text
Add BrowserTrace to Playwright utilities
```

Suggested PR body:

```text
Adds BrowserTrace to the Utils section for teams using Playwright as part of
LLM-driven browser-agent scripts.

BrowserTrace is not a replacement for Playwright Trace Viewer. It captures the
agent-specific context around a Playwright run: model input/output, selected
action, URL, screenshot, status, error, and a standalone HTML export.
```

## 3. Awesome AI Agents

Target:

```text
https://github.com/Jenqyang/Awesome-AI-Agents
```

Status: submitted as https://github.com/Jenqyang/Awesome-AI-Agents/pull/220.

Fit notes:

- This list has a `Tools` section containing agent support tooling.
- BrowserTrace fits only if the maintainer accepts debugging and observability
  tools, not only agent runtimes.

Suggested section:

```text
Applications -> Tools
```

Suggested entry:

```markdown
- [BrowserTrace](https://github.com/aaronlab/browsertrace) - Local flight recorder for AI browser agents with screenshots, URLs, model I/O, failure timelines, and public-safe HTML exports. ![GitHub Repo stars](https://img.shields.io/github/stars/aaronlab/browsertrace?style=social)
```

Suggested PR title:

```text
Add BrowserTrace to AI agent tools
```

Suggested PR body:

```text
Adds BrowserTrace to the Tools section.

BrowserTrace is an MIT-licensed local debugger for AI browser agents. It is
useful for Browser Use, Stagehand, Skyvern, Playwright + LLM scripts, and custom
computer-use agents when a run fails and the developer needs screenshots, URLs,
model I/O, selected actions, status, and errors in one timeline.
```

## 4. Awesome Computer Use Agents

Target:

```text
https://github.com/wjhou/awesome-computer-use-agents
```

Status: submitted as https://github.com/wjhou/awesome-computer-use-agents/pull/2.

Fit notes:

- The list covers GUI/computer-use agents and includes a
  `frameworks/README.md` page for open-source frameworks, tools, and libraries.
- BrowserTrace fits as debugging and observability tooling for web/browser
  computer-use agents.
- The PR frames BrowserTrace as a failed-run inspection tool, not as an agent
  runtime.

Submitted entry:

```markdown
### BrowserTrace
- **Stars**: 3
- **Link**: [GitHub](https://github.com/aaronlab/browsertrace)
- **Tags**: `web` `python` `debugging` `observability`

Local flight recorder for AI browser agents.
```

Verification:

```bash
git diff --check
```

## 5. Computer-Use Agents Overview

Target:

```text
https://github.com/cdxeve/awesome-computer-use-agents
```

Status: submitted as https://github.com/cdxeve/awesome-computer-use-agents/pull/2.

Fit notes:

- The README explicitly curates papers, tools, and benchmarks for terminal and
  GUI computer-use agents.
- BrowserTrace fits the Web Agents table only as an `Open Source Tool`, not as
  an agent runtime.
- The PR keeps the entry to one row to match the target list's format.

Submitted entry:

```markdown
| **BrowserTrace** | 2026 | Open Source Tool | [GitHub](https://github.com/aaronlab/browsertrace) |
```

Verification:

```bash
git diff --check
```

## Skip List

- `e2b-dev/awesome-ai-agents`: the README says the list is only for AI
  assistants and agents, and points SDK/framework/tool submissions to
  `e2b-dev/awesome-sdks-for-ai-agents`.
- Low-star forks with copied README content and no visible curation.
- Broad AI app lists where BrowserTrace would be an unrelated developer tool.

## Stop Rules

- Do not submit the same pitch to many lists.
- Do not open issues asking maintainers to add the project for you.
- Do not ask maintainers or list visitors for stars.
- If maintainers reject the entry as off-topic, accept it and do not argue.
