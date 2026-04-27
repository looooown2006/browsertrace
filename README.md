# BrowserTrace

> See what your AI browser agent did and why it failed.

![demo](docs/demo.gif)

**v0.1 alpha · MIT · single-machine · no signup · no cloud**

---

It's 3 AM. Your browser agent crashed mid-run. You have 1500 lines of logs, no
screenshots, an expired cookie, and a closed browser. You don't know what page
it was on, what selector it tried, or what the model thought before clicking.

BrowserTrace is the recorder you wish you had. One decorator, every step
captured, local timeline UI. Find the bug in 30 seconds, not 30 minutes.

## Install

```bash
pip install git+https://github.com/aaronagent/browsertrace
playwright install chromium    # only needed for the example below
```

## See it in 60 seconds

```bash
git clone https://github.com/aaronagent/browsertrace && cd browsertrace
pip install -e ".[ui]" && pip install playwright && playwright install chromium
python examples/multipage_failure.py    # a research agent fails on Wikipedia
browsertrace                            # opens http://127.0.0.1:3000
```

Click the failed `research agent: find Tokyo's population` run.
You'll see 4 screenshots (Wikipedia → search → article → failure), the exact
moment the agent picked the wrong selector, and the model output expanded
inline showing the bad decision.

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

### Playwright

See `examples/playwright_example.py` and `examples/multipage_failure.py`.

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
# List runs (most recent first; ?status=failed to filter)
curl http://127.0.0.1:3000/api/runs
curl 'http://127.0.0.1:3000/api/runs?status=failed&limit=20'

# Full timeline for one run
curl http://127.0.0.1:3000/api/run/<run_id>
```

Each run JSON includes the run, every step, model I/O, status, errors, relative
timestamps, and `first_error_index` so an LLM can jump straight to what broke.

## Why not just use ___?

| Tool | What it does | What it doesn't |
|---|---|---|
| Langfuse / LangSmith / Helicone | Trace LLM API calls (prompts, tokens, latency) | No DOM, no screenshots, no replay UI |
| Browserbase | Hosted browser runtime with recordings | Locks you into Browserbase's runtime |
| Laminar | Generic agent observability | Heavy, hosted, more setup |
| **BrowserTrace** | **Local replay debugger for any browser agent** | No cloud, no signup, runtime-agnostic |

We're the smallest useful thing for the specific "my browser agent failed,
what happened" loop. ~600 LOC, drop in, fix the bug.

## Roadmap

- [x] **v0.1 (you are here)**: SDK + local UI + screenshots + model I/O + step status
- [ ] **v0.2**: One-command `browsertrace export <run_id>` static HTML bundle (shareable, redactable)
- [ ] **v0.3**: Search and filter the run list + timeline (action / URL / model text)
- [ ] **v0.4**: AI root-cause summary on failed runs (consumes `/api/run/<id>` JSON)
- [ ] **v0.5**: Multi-run comparison ("did this regression appear after my last commit?")
- [ ] **v0.6**: First-class Stagehand / Skyvern adapters
- [ ] **v0.7**: Optional cloud share links

## Contributing

This is a v0.1 alpha. The fastest way to help:

1. Try it on a real agent. Open an issue with what broke or what you wished worked.
2. If you build a Stagehand / Skyvern / computer use adapter, PRs welcome.
3. If you have a screenshot of a beautiful failure trace, share it on X with `@aaronagent` — it's launch fuel.

## License

MIT — see [LICENSE](LICENSE).
