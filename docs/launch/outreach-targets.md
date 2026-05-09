# BrowserTrace Outreach Targets

Post only where the community rules allow it. The ask is feedback from people building browser agents, not votes or stars.

| Channel | Audience | Entry point | Suggested timing | Post type | Owner action | Notes |
|---|---|---|---|---|---|---|
| X | AI builders, OSS devtools people | Personal account | Day 1 | Story post plus follow-up quickstart | Post from personal account | Pin for the first 48 hours if it gets replies |
| LinkedIn | Developer tools and AI infra audience | Personal account | Day 1 | Technical problem/solution post | Post from personal account | Ask what context their logs miss |
| WeChat AI groups | Chinese AI builders | Owner's relevant groups | Day 1 | Short group message | Post manually | Reply with demo commands only when asked |
| Jike | Chinese builders and indie hackers | Personal account | Day 1 | Short product story | Post manually | Keep it conversational |
| Hacker News Show HN | OSS/devtools developers | `https://news.ycombinator.com/submit` | Day 2 | Show HN repo submission | Submit and monitor comments | Only submit when available for several hours |
| Browser Use community | Browser-agent practitioners | `https://github.com/browser-use/browser-use/discussions` | Day 3 | Integration-focused feedback ask | Post where allowed | Lead with Browser Use trace/debug feedback |
| Stagehand community | Browser automation and agent builders | `https://github.com/browserbase/stagehand/discussions` and `https://discord.gg/stagehand` | Day 3 | Adapter feedback ask | Post where allowed | Lead with Stagehand + Playwright local tracing |
| Playwright community | Automation engineers | `https://playwright.dev/community/welcome` | Day 3 or 6 | Debugging write-up | Post where allowed | Emphasize Playwright + LLM scripts, not generic promo |
| Skyvern users | Browser automation agent users | `https://github.com/Skyvern-AI/skyvern/discussions` | Day 6 | Adapter request and issue link | Comment where relevant | Avoid hijacking unrelated threads |
| Reddit | AI agent or local LLM builders | `r/AI_Agents`, `r/Playwright`, or one high-fit subreddit | Day 3 or 5 | Value-first text post | Check subreddit rules before posting | Prefer one high-fit community over many posts |
| Product Hunt | Makers and early adopters | Product Hunt maker dashboard | Day 4 draft, later launch | Product listing | Create draft from personal account | Launch only when gallery/demo assets are ready |
| AgentKart | Open-source AI agent marketplace visitors | `https://www.agentkart.ai/submit` | Day 2 or 4 | Directory submission | Submit from owner account if login is required | Position as an agent debugging tool, not an agent runtime |
| Agent Hub | People browsing AI agents, MCPs, and skills | `https://agent-hub.dev/` | Day 4 | Directory suggestion | Submit/contact if available | Fit is weaker unless framed as agent tooling |
| AgDex | AI agent ecosystem directory readers | `https://agdex.ai/` | Day 4 | Directory suggestion | Submit/contact if available | Developer tools and observability category is the best fit |
| agentfirst.directory | Agent-first tooling ecosystem | `https://agentfirst.directory/` | Day 4 | Directory suggestion | Submit/contact if available | Browser Automation category already includes related tools |
| console.dev | Devtools newsletter readers | `https://console.dev/` | Day 5 | Short editorial pitch | Contact from owner email/account | Lead with local-first browser-agent debugging and the redacted export release |
| GitHub Discussions | Existing repo visitors | `https://github.com/aaronlab/browsertrace/discussions/6` | Daily | Feedback collection | Update launch discussion | Link from posts when people ask where to comment |

## Priority Order

1. X, LinkedIn, WeChat, and Jike for quick warm feedback.
2. Hacker News once the first-run path is clearly understandable.
3. Browser Use and Stagehand communities because they match the product.
4. Reddit only with a useful write-up and after checking local rules.
5. Directory/newsletter submissions after `v0.1.6` links are stable.
6. Product Hunt after the visual assets are strong enough for a broader audience.

## Directory And Newsletter Pitch

Use this for directories and newsletters that accept new tool suggestions. Keep
the subject concrete and do not ask for stars.

Subject:

```text
BrowserTrace: local flight recorder for AI browser agents
```

Body:

```text
BrowserTrace is an MIT-licensed local debugger for AI browser agents.

It records each browser-agent step as a timeline with screenshots, URL, action,
model input/output, status, and errors, then exports a standalone HTML trace.
The v0.1.6 release includes `browsertrace demo` for first-run onboarding and
`browsertrace export --redact` so real traces can be shared publicly without
prompt/model I/O.

Useful for Browser Use, Stagehand, Skyvern, Playwright + LLM scripts, and custom
computer-use agents.

Repo: https://github.com/aaronlab/browsertrace
Live demo: https://aaronlab.github.io/browsertrace/
Browser Use guide: https://aaronlab.github.io/browsertrace/browser-use-debugging.html
Release: https://github.com/aaronlab/browsertrace/releases/tag/v0.1.6
```

Submission notes:

- Submit only once per directory/newsletter.
- If a directory requires an account, use the owner's account.
- If a directory has no visible submission form, use this as an owner email or
  contact-form pitch.
- Track every submission URL or email target in `docs/launch/metrics-log.md`.

## First Targeted Community Posts

Use these only after the Day 1 warm posts have a live demo link and at least one
real reply or question to reference.

1. Browser Use Discussions
   - Best angle: "I am building a local trace viewer for failed browser-use runs
     and want feedback on which fields matter at failure time."
   - Link order: Browser Use guide first, live trace second, repo third.
   - Feedback sink: `https://github.com/aaronlab/browsertrace/issues/11`
   - Best category: Show and tell or Q&A. Existing threads about selectors,
     generated Playwright scripts, and audit trails are relevant only if the
     reply directly answers the thread.
   - Do not open a Browser Use issue unless reporting an actual Browser Use bug
     or proposing a concrete adapter.
2. Stagehand Discussions or Discord
   - Best angle: "For Stagehand + Playwright scripts, would a local timeline of
     screenshots, URLs, actions, and model I/O make failure triage easier?"
   - Link order: Stagehand guide first, live trace second, repo third.
   - Feedback sink: `https://github.com/aaronlab/browsertrace/issues/8`
   - Ask whether a first-class Stagehand wrapper should capture `act`,
     `extract`, `observe`, or `agent` calls first.
3. Playwright community
   - Best angle: "This is for Playwright scripts that include LLM decisions, not
     a replacement for Playwright trace viewer."
   - Use Discord or LinkedIn only when the topic is LLM-guided automation.
     Share only the debugging write-up unless people ask for the repo.
4. Skyvern Discussions
   - Best angle: "I am planning a Skyvern adapter and want to know which failure
     artifacts are most useful: screenshots, step prompts, model outputs, or
     workflow state."
   - Link order: Skyvern guide first, live trace second, repo third.
   - Link to the existing BrowserTrace Skyvern adapter issue if asked for a
     tracking thread.

## Do Not Do

- Do not mass-post the same link to many communities.
- Do not DM strangers asking for stars.
- Do not ask for upvotes on Hacker News or Product Hunt.
- Do not post in communities where self-promotion is disallowed.
- Do not use generated replies verbatim on Hacker News.
