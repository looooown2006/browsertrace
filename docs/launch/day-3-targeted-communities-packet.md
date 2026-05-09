# BrowserTrace Day 3 Targeted Communities Packet

Use this after Day 1 warm posts and only if the owner can reply to technical
questions. The goal is to reach builders who already work with browser agents,
not to post a generic product announcement.

Entry points checked:

- Browser Use Discussions: https://github.com/browser-use/browser-use/discussions
- Stagehand Discussions: https://github.com/browserbase/stagehand/discussions
- Playwright community: https://playwright.dev/community/welcome
- Skyvern Discussions: https://github.com/Skyvern-AI/skyvern/discussions

## Preflight Gate

Run:

```bash
uv run --python 3.11 python scripts/launch_metrics.py --append --note "before Day 3 targeted communities"
```

Submit only if all are true:

- The owner can reply to technical questions the same day.
- The post asks for adapter/workflow feedback, not stars.
- The post is customized to the community and does not look cross-posted.
- The post uses the walkthrough or live demo before asking people to install.
- The community allows this kind of post or there is an existing relevant thread.

Do not post if:

- The only available angle is "please check out my repo."
- The community rules prohibit self-promotion.
- There is already a similar unanswered post from the owner.
- The owner cannot follow up.

## Priority Order

1. Browser Use Discussions
2. Stagehand Discussions or Discord
3. Playwright community channels
4. Skyvern Discussions

Stop after one or two posts if the replies are low quality or negative. Improve
the message before posting anywhere else.

## Browser Use

Best place: GitHub Discussions, preferably a Show and tell, Ideas, or Q&A-style
thread if the category is available.

Title:

```text
Feedback wanted: local traces for failed Browser Use runs
```

Body:

```text
I'm building BrowserTrace, a small local trace viewer for browser-agent failures:
screenshots, URL, action, model input/output, status, and failed-step errors in
one timeline.

The debugging problem I want to solve for Browser Use users is: the agent fails
deep into a run, but the logs do not show what the browser looked like or which
model output caused the wrong action.

Live exported trace:
https://aaronlab.github.io/browsertrace/

Repo:
https://github.com/aaronlab/browsertrace

For Browser Use specifically, what would be most useful to capture?

- Agent task and step number
- Browser screenshot
- URL
- Action/tool call
- Model input and output
- Selector or target element
- DOM/extracted text
- Retry state or memory

I'm trying to decide what the Browser Use adapter should capture first.
```

Metrics:

```bash
uv run --python 3.11 python scripts/launch_metrics.py --append --note "after Browser Use discussion: <URL>"
```

## Stagehand

Best place: GitHub Discussions or Stagehand Discord, where allowed.

Title:

```text
Would a local timeline help debug failed Stagehand act/extract runs?
```

Body:

```text
I'm building BrowserTrace, a local debugger for AI browser-agent runs. It records
each step as a timeline: screenshot, URL, action, model input/output, status,
and error.

For Stagehand users, I'm trying to understand which calls are most important to
wrap first:

- act()
- extract()
- observe()
- agent()
- lower-level Playwright page actions

Live exported trace:
https://aaronlab.github.io/browsertrace/

Repo:
https://github.com/aaronlab/browsertrace

If you have debugged a failed Stagehand run, what state did you wish you had at
failure time?
```

Metrics:

```bash
uv run --python 3.11 python scripts/launch_metrics.py --append --note "after Stagehand post: <URL>"
```

## Playwright

Playwright is broader than AI agents. Do not present BrowserTrace as a
replacement for Playwright Trace Viewer. Share only where the question is about
LLM-guided browser automation, agents, or missing model-decision context.

Best angles:

- Playwright + LLM scripts
- Browser tests where an LLM chooses the next action
- Debugging screenshots plus model output
- Exporting a standalone failure trace for an issue

Short reply for relevant threads:

```text
If the missing piece is the LLM decision context rather than Playwright's browser
trace itself, I'm building a small local tool for that case:

https://aaronlab.github.io/browsertrace/debug-browser-agent-failure.html

It records screenshot, URL, action label, model input/output, and failed-step
error into a local timeline. It is not a replacement for Playwright Trace Viewer;
it is for Playwright scripts where an LLM is part of the control loop.
```

Metrics:

```bash
uv run --python 3.11 python scripts/launch_metrics.py --append --note "after Playwright community reply: <URL>"
```

## Skyvern

Best place: GitHub Discussions, or a relevant adapter/workflow thread. Do not
hijack unrelated bug reports.

Title:

```text
Feedback wanted: what should a Skyvern trace adapter capture?
```

Body:

```text
I'm building BrowserTrace, a local timeline/debugger for failed AI browser-agent
runs. It records screenshots, URL, action, model input/output, status, and
failed-step errors.

Live exported trace:
https://aaronlab.github.io/browsertrace/

Repo:
https://github.com/aaronlab/browsertrace

BrowserTrace now has a basic Skyvern wrapper for high-level task/workflow calls.
I want to know what a deeper adapter should capture to debug failed workflows:

- screenshots
- workflow state
- task prompt
- model output
- selected element or selector
- browser URL
- retry/history state
- extracted data

Which artifacts would be most useful when a Skyvern workflow fails?
```

Metrics:

```bash
uv run --python 3.11 python scripts/launch_metrics.py --append --note "after Skyvern discussion: <URL>"
```

## Triage After Posting

Within 24 hours:

- Convert specific adapter requests into GitHub issues.
- Link each issue from the relevant discussion reply.
- Add useful quotes or summaries to `docs/launch/metrics-log.md`.
- Update the v0.2 milestone if a clear adapter priority emerges.

## Stop Rules

- Do not post in more than two targeted communities on the same day unless
  replies are clearly useful.
- Do not paste identical text across communities.
- Do not argue with moderators or community regulars.
- Do not ask for stars, upvotes, follows, reposts, or "support."
- If a post is removed, do not repost it; learn from the reason and move on.
