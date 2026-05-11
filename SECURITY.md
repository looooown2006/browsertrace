# Security Policy

BrowserTrace records browser-agent traces locally. Traces may contain screenshots,
URLs, prompts, model outputs, selectors, and other debugging metadata. Treat
trace exports as potentially sensitive.

## Supported Versions

| Version | Supported |
|---|---|
| `0.1.x` | Yes |

## Reporting a Vulnerability

If you find a security issue, please do not open a public issue with exploit
details or sensitive traces.

Use a private GitHub vulnerability report from the repository Security tab if
that option is available. If private reporting is unavailable, open a minimal
public issue without exploit details, secrets, private URLs, screenshots,
prompts, model output, or customer data, and ask the maintainer to establish a
private follow-up path.

For non-sensitive browser-agent workflow questions, use the closest public
debugging guide for context. Security-sensitive details should still stay
private.

- Browser Use guide: https://aaronlab.github.io/browsertrace/browser-use-debugging.html
- Stagehand guide: https://aaronlab.github.io/browsertrace/stagehand-debugging.html
- Skyvern guide: https://aaronlab.github.io/browsertrace/skyvern-debugging.html
- Playwright + LLM guide: https://aaronlab.github.io/browsertrace/playwright-llm-debugging.html
- Computer-use guide: https://aaronlab.github.io/browsertrace/computer-use-agent-debugging.html

Include:

- A short description of the issue.
- Reproduction steps.
- Impacted BrowserTrace version.
- Whether the issue can expose local files, screenshots, prompts, model output,
  API keys, or trace exports.

## Data Handling Notes

- BrowserTrace stores data locally by default under `~/.browsertrace/` or
  `BROWSERTRACE_HOME`.
- HTML exports inline screenshots and model output. Review exports before
  sharing them publicly.
- Use `browsertrace export <run_id> --public -o public.html` before public
  sharing to omit prompt/model I/O, screenshots, and URLs.
- Do not attach trace exports containing secrets, customer data, private URLs,
  cookies, tokens, or proprietary prompts to public issues.
