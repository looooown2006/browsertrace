# aaronlab GitHub Profile README Draft

This is the source draft for the live profile repository `aaronlab/aaronlab`.
GitHub only renders a personal profile README when the repository name matches
the account name exactly.

Current note: the old public profile README repository `aaronlab/aaronagent`
now acts as a redirect for old traffic. Keep the live profile README in
`aaronlab/aaronlab`.

## README Draft

```markdown
# Aaron Lab

I build AI agent systems, browser automation tools, and local-first developer
workflows.

## Featured Project

### BrowserTrace

Local flight recorder for AI browser agents.

![BrowserTrace social preview](https://raw.githubusercontent.com/aaronlab/browsertrace/main/docs/social-preview.png)

BrowserTrace helps Browser Use, Stagehand, Skyvern, Playwright + LLM, and
custom computer-use builders debug failed browser-agent runs with local step
timelines.

- Records screenshots, URLs, actions, model input/output, status, and errors.
- Opens failed runs in a local web UI.
- Exports standalone HTML traces.
- Supports public-safe exports that omit prompts, model I/O, screenshots, and
  URLs.
- MIT licensed and local-first.

Repo: https://github.com/aaronlab/browsertrace

Live demo: https://aaronlab.github.io/browsertrace/

Try locally before PyPI publishing is enabled:

~~~bash
uvx --from "browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.14" browsertrace doctor
uvx --from "browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.14" browsertrace demo
~~~

Computer-use guide:
https://aaronlab.github.io/browsertrace/computer-use-agent-debugging.html

Runnable examples:
https://github.com/aaronlab/browsertrace/tree/main/examples

Roadmap: https://github.com/aaronlab/browsertrace/blob/main/ROADMAP.md

Launch feedback:
https://github.com/aaronlab/browsertrace/issues/3

Good first issue:
https://github.com/aaronlab/browsertrace/issues/195

First PR Recipe:
https://github.com/aaronlab/browsertrace/blob/main/CONTRIBUTING.md#first-pr-recipe keeps the first contribution small and reviewable.

Public-safe demo export:
https://github.com/aaronlab/browsertrace/releases/download/v0.1.14/browsertrace-demo-public.html

## Troubleshooting

For profile-reader follow-up, local first-run issues, CI failures, or AI/coding-agent troubleshooting replies, ask for debugging/workflow details plus JSON CLI diagnostics when safe to share:

~~~bash
browsertrace doctor --json
browsertrace list --status failed --json
browsertrace show <run_id> --json
~~~

## Current Focus

- AI browser-agent debugging
- Browser automation and computer-use agents
- LLM observability for local workflows
- Agent evaluation and tool reliability

## Open-Source Projects

| Project | Focus |
|---|---|
| [browsertrace](https://github.com/aaronlab/browsertrace) | Local traces for failed AI browser-agent runs |
| [claude-code-source-analysis](https://github.com/aaronlab/claude-code-source-analysis) | Claude Code source analysis and learning notes |
| [agent-bench-lite](https://github.com/aaronlab/agent-bench-lite) | Lightweight AI agent evaluation benchmark |
| [mcp-shield](https://github.com/aaronlab/mcp-shield) | MCP server security audit tooling |
| [openclaw](https://github.com/aaronlab/openclaw) | Personal AI assistant experiments |

## Feedback

If you build browser agents, the most useful BrowserTrace feedback is:

- Which framework do you use?
- What context is missing when a run fails?
- Are local HTML exports enough, or do you need hosted share links?
- Which adapter should be improved first?

Launch discussion:
https://github.com/aaronlab/browsertrace/discussions/6
```

## Owner Action

1. Keep the profile repository available as `aaronlab/aaronlab`.
2. Keep the draft above in `README.md`.
3. Keep BrowserTrace as the first featured project during launch.
4. Recheck the profile page after publishing profile changes.
