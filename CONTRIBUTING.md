# Contributing to BrowserTrace

Thanks for helping improve BrowserTrace.

BrowserTrace is intentionally small: a local-first recorder for AI browser
agent runs. Good contributions make failed browser-agent runs easier to inspect,
export, or integrate with real agent frameworks.

## Development Setup

```bash
git clone https://github.com/aaronlab/browsertrace
cd browsertrace
uv run --python 3.11 --extra dev pytest -q
```

The test suite should pass before opening a pull request.

## Useful Local Checks

```bash
uv run --python 3.11 --extra dev pytest -q
uv build
python examples/no_api_failure_demo.py
browsertrace
```

## Contribution Areas

- Framework integrations: Browser Use, Stagehand, Skyvern, Playwright, and
  computer-use agents.
- Export improvements: portable HTML, redaction, and issue attachments.
- Debugging workflow: clearer failure markers, search, filters, and summaries.
- Documentation: short examples from real browser-agent failures.

## Design Principles

- Keep the base SDK dependency-light.
- Keep data local by default.
- Prefer small, inspectable features over broad observability-platform scope.
- Add tests for behavior changes.
- Keep optional framework integrations optional.

## Pull Requests

For each PR, include:

- What user problem it solves.
- How to try it locally.
- Test commands run.
- Screenshots or exported traces for UI/demo changes.

