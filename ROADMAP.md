# BrowserTrace Roadmap

BrowserTrace is a local flight recorder for AI browser agents. The roadmap
prioritizes work that makes failed Browser Use, Stagehand, Skyvern, Playwright +
LLM, and computer-use runs easier to inspect, export, and discuss.

## Current Release

`v0.1.10` is the current launch release.

Shipped:

- Local SDK and CLI for recording browser-agent steps.
- Local web UI for inspecting runs.
- Screenshots, URLs, actions, model input/output, status, and errors.
- `browsertrace demo` for a deterministic first run without API keys.
- `browsertrace export` for standalone HTML traces.
- `browsertrace export --public` for public-safe sharing without prompt/model
  I/O, screenshots, or URLs.
- Basic Browser Use, Stagehand, and Skyvern-shaped integration examples.
- GitHub Pages live demo, integration guides, launch kit, and public-safe demo
  asset.

## Launch Blockers

These are owner-only account actions. They are important for growth, but they
cannot be completed by a contributor PR.

| Issue | Why it matters |
|---|---|
| [#5 PyPI publishing](https://github.com/aaronlab/browsertrace/issues/5) | Enables normal `pip install browsertrace` instead of GitHub install URLs. |
| [#13 GitHub profile README](https://github.com/aaronlab/browsertrace/issues/13) | Makes `aaronlab` profile traffic point to BrowserTrace during launch. |
| [#15 Social preview](https://github.com/aaronlab/browsertrace/issues/15) | Makes shared repo links show the BrowserTrace card. |
| [#16 Search console submission](https://github.com/aaronlab/browsertrace/issues/16) | Starts long-tail indexing for the GitHub Pages docs and demos. |
| [#18 Awesome list submissions](https://github.com/aaronlab/browsertrace/issues/18) | Prepares high-fit curated-list submissions without mass-posting. |

## v0.2 Product Tracks

| Track | Current issue | Good contribution shape |
|---|---|---|
| Browser Use trace fields | [#11](https://github.com/aaronlab/browsertrace/issues/11) | Add fields that real Browser Use failures expose safely, with no required API keys in tests. |
| Stagehand adapter depth | [#8](https://github.com/aaronlab/browsertrace/issues/8) | Capture `act`, `extract`, `observe`, or agent calls with small examples and focused tests. |
| Skyvern workflow depth | [#4](https://github.com/aaronlab/browsertrace/issues/4) | Capture task/workflow status, selected elements, and failure state where the API exposes them. |
| Playwright + LLM trace shape | [#12](https://github.com/aaronlab/browsertrace/issues/12) | Document and test fields that help LLM-guided Playwright scripts explain failures. |
| Multi-run comparison | Open an issue with a real regression case | Compare two runs enough to answer whether a failure appeared after a code or prompt change. |
| Export ergonomics | Open a focused issue | Improve redaction, attachment flow, or public-safe trace sharing without hosted infrastructure. |

## Contribution Guidelines

Good roadmap PRs are narrow and testable:

- Keep optional framework dependencies optional.
- Avoid network access, real API keys, and hosted browser accounts in tests.
- Use `BROWSERTRACE_HOME` for isolated local data in examples and tests.
- Use `browsertrace export <run_id> --public -o public.html` before sharing a
  real trace publicly.
- Include the exact command used to verify the change.

Start with `CONTRIBUTING.md`, then open an integration request if the work
depends on a specific browser-agent framework.

## Success Signals

The project is moving in the right direction when:

- New users can install with `pip install "browsertrace[ui]"`.
- Browser-agent builders report which trace fields they need.
- External issues and PRs include real failure shapes instead of generic feature
  requests.
- Public posts and directory submissions ask for workflow feedback, not stars or
  upvotes.
- The live GitHub audit eventually reports more than 1000 stars.
