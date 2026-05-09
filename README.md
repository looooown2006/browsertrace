# BrowserTrace

> Local flight recorder for AI browser agents.

[![CI](https://github.com/aaronlab/browsertrace/actions/workflows/ci.yml/badge.svg)](https://github.com/aaronlab/browsertrace/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/aaronlab/browsertrace?color=blue)](https://github.com/aaronlab/browsertrace/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/aaronlab/browsertrace?style=social)](https://github.com/aaronlab/browsertrace/stargazers)

![demo](docs/demo.gif)

**MIT · local-first · no signup · no cloud · Python 3.11+**

---

Your AI browser agent failed. Logs say what code ran, but not what the agent
actually saw, clicked, or decided.

BrowserTrace records each browser-agent step as a timeline: screenshot, URL,
action, model input, model output, status, and error. Open the local UI and jump
straight to the failure.

Built for Browser Use, Stagehand, Skyvern, Playwright + LLM scripts, and custom
computer-use agents.

**Try it:** [live demo](https://aaronlab.github.io/browsertrace/) ·
[debugging walkthrough](https://aaronlab.github.io/browsertrace/debug-browser-agent-failure.html) ·
[integrations](https://aaronlab.github.io/browsertrace/integrations.html) ·
[examples](examples/) ·
[integration request](https://github.com/aaronlab/browsertrace/issues/new?template=integration_request.yml) ·
[launch discussion](https://github.com/aaronlab/browsertrace/discussions/6)

## Install

```bash
# SDK only
pip install "browsertrace @ git+https://github.com/aaronlab/browsertrace@v0.1.6"

# SDK + local web UI
pip install "browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.6"
```

## See a failure trace in 60 seconds

```bash
pip install "browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.6"
browsertrace demo
browsertrace
```

Open `http://127.0.0.1:3000`, click
`demo: checkout agent fails on disabled button`, and inspect the failed step.

Want to inspect an exported trace before installing anything? Open the
[live static demo](https://aaronlab.github.io/browsertrace/) or download
[`browsertrace-demo.html`](https://github.com/aaronlab/browsertrace/releases/download/v0.1.6/browsertrace-demo.html)
from the latest release.

For a walkthrough, read
[How to debug an AI browser-agent failure](https://aaronlab.github.io/browsertrace/debug-browser-agent-failure.html).

For all runnable examples, see the [examples guide](examples/).

For a real browser demo with screenshots from Wikipedia:

```bash
pip install playwright
playwright install chromium
python examples/multipage_failure.py
browsertrace
```

## Use it in your own code

### Decorator (simplest)

`@trace` works on both sync and async functions. The first argument receives the
active `Run`, so you can call `run.step(...)` (or `await run.snapshot(page)`)
from inside.

```python
from browsertrace import trace

# sync
@trace
def my_agent(run, query: str):
    run.step(action=f"search: {query}", screenshot=...)
    run.step(action="click first result", screenshot=...)

# async
@trace
async def my_async_agent(run, page, query: str):
    await run.snapshot(page, action=f"search: {query}")
    await run.snapshot(page, action="click first result")

my_agent("browser agent debugging")
```

### Playwright shortcut

If you have a Playwright `page`, use `run.snapshot(page, action=...)` to skip
the `url=page.url, screenshot=await page.screenshot()` boilerplate:

```python
async with tracer.run("my-task") as run:
    await page.goto("https://example.com")
    await run.snapshot(page, action="opened example.com")
    await page.click("#login")
    await run.snapshot(page, action="clicked login")
```

For `playwright.sync_api`, use `run.snapshot_sync(page, ...)` instead.

### Context manager (more control)

```python
from browsertrace import Tracer

tracer = Tracer()

with tracer.run("my-task") as run:
    run.step(
        action="click login button",
        url=page.url,
        screenshot=await page.screenshot(),     # bytes or path; optional
        model_input={"prompt": "..."},          # optional
        model_output={"selector": "#login"},    # optional
        retries=0,                              # extra metadata via kwargs
    )
```

If the `with` block raises, the run is marked `failed` and the error message
is recorded against the last step.

### Browser Use integration

```python
from browser_use import Agent
from browsertrace import Tracer
from browsertrace.integrations.browser_use import attach_tracer

tracer = Tracer()
agent = Agent(task="...", llm=ChatOpenAI(model="gpt-4o"))

with attach_tracer(agent, tracer, name="my run"):
    await agent.run()
```

### Stagehand integration

```python
from stagehand import Stagehand
from browsertrace import Tracer
from browsertrace.integrations.stagehand import wrap_stagehand

tracer = Tracer()
stagehand = await Stagehand(...).init()
page = wrap_stagehand(stagehand.page, tracer, name="my run")

await page.goto("https://example.com")
await page.act("click the login button")   # auto-recorded
await page.extract("get the headline")      # auto-recorded
page.bt_run.close()
```

For a no-network wrapper demo that does not require a Stagehand install, run
`python examples/stagehand_wrapper_example.py`.

### Skyvern integration

Wrap a Skyvern-shaped client to record high-level task and workflow calls.

```python
from skyvern import Skyvern
from browsertrace import Tracer
from browsertrace.integrations.skyvern import wrap_skyvern

tracer = Tracer()
skyvern = wrap_skyvern(Skyvern(...), tracer, name="my skyvern run")

await skyvern.run_task(
    url="https://example.com",
    prompt="extract the invoice total",
    wait_for_completion=True,
)

skyvern.close()
```

For a no-network wrapper demo that does not require a Skyvern install, run
`python examples/skyvern_wrapper_example.py`.

### Playwright

See `examples/playwright_example.py`, `examples/failure_example.py`, and
`examples/multipage_failure.py`. If you want a no-browser deterministic demo,
run `browsertrace demo`.

## Storage and config

| What | Where | How to override |
|---|---|---|
| SQLite db + screenshots | `~/.browsertrace/` | `Tracer(home="...")` or `BROWSERTRACE_HOME=/path browsertrace` |
| UI port | `3000` | `BROWSERTRACE_PORT=4000 browsertrace` |

## What gets recorded per step

| field           | type              | notes                                  |
|-----------------|-------------------|----------------------------------------|
| `action`        | string            | human description: "click", "type x"   |
| `url`           | string            | page URL at the time                   |
| `screenshot`    | PNG bytes / path  | saved to `~/.browsertrace/screenshots/`|
| `model_input`   | any JSON-able     | prompt / messages sent to the LLM      |
| `model_output`  | any JSON-able     | LLM response / decision                |
| `status`        | `"ok"` / `"error"`| step-level status (red badge if error) |
| `error`         | string            | error message if status is `"error"`   |
| `**metadata`    | any JSON-able     | retries, latency, anything else        |
| `timestamp`     | float (epoch)     | auto                                   |

## Programmatic access

Every trace is also a JSON object you can feed back to an LLM for self-debugging
or pipe into other tools.

```bash
# List runs (most recent first; ?status=failed and ?q= filters work)
curl http://127.0.0.1:3000/api/runs
curl 'http://127.0.0.1:3000/api/runs?status=failed&q=tokyo&limit=20'

# Full timeline for one run
curl http://127.0.0.1:3000/api/run/<run_id>

# AI root-cause summary (set OPENAI_API_KEY first; or pip install browsertrace[ai])
curl http://127.0.0.1:3000/api/run/<run_id>/summary
```

Each run JSON includes the run, every step, model I/O, status, errors, relative
timestamps, and `first_error_index` so an LLM can jump straight to what broke.

## Command line

```bash
browsertrace                      # serve the web UI
browsertrace demo                 # create a deterministic failed demo run
browsertrace list                 # list recent runs in the terminal
browsertrace show <id-or-prefix>  # print a run's timeline
browsertrace export <id> -o run.html   # self-contained HTML bundle (screenshots inlined)
browsertrace export <id> --redact -o public.html   # omit model I/O for sharing
```

`export` produces a single HTML file you can email, attach to an issue, or
upload anywhere. No server, no DB, fully portable. Use `--redact` before
sharing a real trace publicly; it keeps screenshots, actions, URLs, status, and
errors while omitting prompt/model I/O.

## Why not just use ___?

| Tool | Strength | Why you might still want BrowserTrace |
|---|---|---|
| Langfuse / LangSmith / Helicone | Great LLM call tracing, prompt + token + cost | Not browser-agent-first: no DOM, no screenshot, no replay UI built around browser state |
| Browserbase | Hosted browser runtime with built-in recordings | Locks you into their runtime; BrowserTrace works with any local Playwright, Browser Use, computer use |
| Laminar | Generic agent observability with browser session replay | Heavier, hosted-first; BrowserTrace is local-first, ~700 LOC, drop in via decorator |
| **BrowserTrace** | **Local replay debugger built around the browser-agent failure loop** | OSS, runtime-agnostic, no signup, JSON API for AI self-debug |

Smallest useful thing for "my browser agent failed, what happened" — drop in,
fix the bug, get back to building.

## Cloud / Team (coming soon)

Local BrowserTrace will always be free OSS. We're working on a hosted version
for teams that need:

- **One-click share links** for failed runs (send to a teammate, paste in a Slack
  thread, attach to a GitHub issue, no `git clone` required)
- **CI ingestion** — upload traces from your test runs, get a digest of failures
- **Multi-run regression detection** — "this DOM changed since last passing run"
- **Team workspaces, comments, retention beyond a single laptop**

If you want it, **[open a cloud/team interest issue](https://github.com/aaronlab/browsertrace/issues/new?template=cloud_interest.yml)** describing your agent setup and team size. Pricing will likely be:

| Tier | Price | For |
|---|---:|---|
| OSS Local | Free | Solo, local debugging |
| Solo Cloud | $19/mo | Individual dev, hosted share + AI summaries |
| Team | $99/mo | 5 seats, CI, workspaces, regression detection |
| Scale | $249/mo | High-volume, long retention |
| Enterprise | Custom | SSO, VPC, SOC2 |

Real-world feedback shapes what ships first.

## Roadmap

- [x] **v0.1**: SDK + local UI + screenshots + model I/O + step status
- [x] **CLI export**: `browsertrace export <run_id>` static HTML bundle
- [x] **Search/filter**: Filter the run list by status and query text
- [x] **AI summaries**: Optional OpenAI-compatible root-cause endpoint
- [x] **Skyvern wrapper**: Trace high-level task/workflow calls
- [ ] **Multi-run comparison**: "Did this regression appear after my last commit?"
- [ ] **Deeper Skyvern adapter**: Capture workflow state and selected elements
- [ ] **Optional cloud share links**

## Contributing

This is a v0.1 alpha. The fastest way to help:

1. Try it on a real agent. Open an issue with what broke or what you wished worked.
2. If you need a Browser Use / Stagehand / Skyvern / Playwright adapter,
   [open an integration request](https://github.com/aaronlab/browsertrace/issues/new?template=integration_request.yml).
3. If you have a screenshot of a beautiful failure trace, share it on X with `@aaronlab` — it's launch fuel.

Launch discussion: [BrowserTrace v0.1.6](https://github.com/aaronlab/browsertrace/discussions/6).

Changelog: [CHANGELOG.md](CHANGELOG.md).

## License

MIT — see [LICENSE](LICENSE).
