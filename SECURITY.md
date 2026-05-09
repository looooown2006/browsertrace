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

Report privately by emailing the maintainer or by opening a GitHub security
advisory if available for the repository.

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
- Do not attach trace exports containing secrets, customer data, private URLs,
  cookies, tokens, or proprietary prompts to public issues.

