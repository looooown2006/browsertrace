# Changelog

BrowserTrace uses small release tags while the project is still alpha. Dates are
UTC.

## Unreleased

- No unreleased changes.

## 0.1.9 - 2026-05-09

- Added `browsertrace export --redact-urls` so exported HTML traces can omit
  private domains, query strings, or internal paths from step URLs.
- Updated public sharing docs to show prompt/model I/O, screenshot, and URL
  redaction together.

## 0.1.8 - 2026-05-09

- Added `browsertrace export --redact-screenshots` so exported HTML traces can
  omit screenshots when page state may reveal private data.
- Updated sharing docs and launch copy to distinguish model I/O redaction from
  screenshot redaction.

## 0.1.7 - 2026-05-09

- Added a no-dependency Browser Use-shaped callback demo so users can inspect
  adapter output without installing Browser Use, using an API key, or launching
  a browser.
- Added a comparison page for BrowserTrace versus Playwright Trace Viewer,
  LangSmith, Langfuse, and Browserbase.
- Added a Playwright + LLM feedback issue and linked it from the guide and
  launch packet.

## 0.1.6 - 2026-05-09

- HTML exports now show both model input and model output by default, matching
  the recorded trace data and public positioning.
- `browsertrace export --redact` still omits both prompt/model I/O for public
  sharing.

## 0.1.5 - 2026-05-09

- Added `browsertrace demo`, a packaged no-browser/no-API demo command that
  creates a deterministic failed checkout-agent trace after installation.
- Updated launch copy and walkthroughs to use the lower-friction demo command.

## 0.1.4 - 2026-05-09

- Added `browsertrace export --redact` for shareable HTML traces that omit
  prompt/model I/O while keeping screenshots, actions, URLs, status, and errors.
- Pinned temporary GitHub install commands to `v0.1.4` while PyPI publishing is
  waiting on owner-side Trusted Publisher setup.
- Updated the public roadmap and launch tooling to track the current release.

## 0.1.3 - 2026-05-09

- Added a runnable examples guide under `examples/`.
- Added no-network wrapper examples for Stagehand and Skyvern.
- Added a checked-in GitHub Pages workflow.
- Improved package metadata for future PyPI publishing.
- Refreshed launch surfaces, discussion text, and release links to match the
  current launch-ready branch.

## 0.1.2 - 2026-05-09

- Added `browsertrace.integrations.skyvern.wrap_skyvern`.
- Added public `Run.close(error=None)` for integration-created runs.
- Published release assets: wheel, sdist, demo HTML, demo video, and poster.
- Updated the launch kit and public integration pages.

## 0.1.1 - 2026-05-09

- Prepared the first launch-ready release.
- Added the deterministic no-API failure demo.
- Added the live static demo and debugging walkthrough.
- Added launch materials for owner-run social, Show HN, Product Hunt, and
  targeted community posts.

## 0.1.0 - 2026-05-09

- Initial BrowserTrace SDK, local UI, CLI, SQLite storage, screenshots, model
  input/output, step status, search/filter, export, and optional AI summary
  endpoint.
