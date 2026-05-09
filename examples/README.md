# BrowserTrace Examples

Use these examples to create local traces before wiring BrowserTrace into a real
agent. The first three examples do not require API keys or hosted browser
accounts.

## Fastest Path

```bash
pip install "browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.5"
browsertrace demo
browsertrace
```

Open `http://127.0.0.1:3000` and inspect
`demo: checkout agent fails on disabled button`. From a source checkout,
`python examples/no_api_failure_demo.py` creates the same trace.

## Example Matrix

| Example | Use when | Extra services | Command |
|---|---|---:|---|
| `no_api_failure_demo.py` | You want the fastest failing trace | None | `python examples/no_api_failure_demo.py` |
| `stagehand_wrapper_example.py` | You want to see Stagehand-style `act` and `extract` calls recorded | None | `python examples/stagehand_wrapper_example.py` |
| `skyvern_wrapper_example.py` | You want to see Skyvern-style task calls recorded | None | `python examples/skyvern_wrapper_example.py` |
| `basic_example.py` | You want the smallest manual SDK example | None | `python examples/basic_example.py` |
| `failure_example.py` | You want a deterministic failed run with richer steps | None | `python examples/failure_example.py` |
| `playwright_example.py` | You have Playwright installed and want browser screenshots | Local Chromium | `python examples/playwright_example.py` |
| `multipage_failure.py` | You want a multi-page Playwright failure demo | Local Chromium | `python examples/multipage_failure.py` |
| `browseruse_example.py` | You already use Browser Use and want to attach tracing | Browser Use + LLM | `python examples/browseruse_example.py` |

For Playwright examples, install the browser runtime first:

```bash
pip install playwright
playwright install chromium
```

## Where Traces Are Stored

By default BrowserTrace stores SQLite data and screenshots in
`~/.browsertrace/`. To keep example output isolated, set `BROWSERTRACE_HOME`:

```bash
BROWSERTRACE_HOME=/tmp/browsertrace-demo python examples/stagehand_wrapper_example.py
BROWSERTRACE_HOME=/tmp/browsertrace-demo browsertrace
```
