# BrowserTrace 7-Day Launch Growth Design

Date: 2026-05-09
Project: `aaronlab/browsertrace`
Current audited stars: 3
Target: more than 1000 GitHub stars

## Objective

Turn BrowserTrace from a launch-ready OSS repo into a visible AI developer tool
through legitimate distribution. The goal is not complete until a current
GitHub audit shows `aaronlab/browsertrace` has more than 1000 stars.

## Operating Boundary

The launch must not use fake stars, bought stars, bots, vote rings, spam, or
deceptive accounts. Growth work should make the project easier to understand,
try, discuss, and share.

Codex can own repo-side work, copywriting, release assets, launch checklists,
issue/discussion triage templates, and daily audits. The owner must still click
publish or authenticate on platforms that require a personal account, including
Hacker News, Product Hunt, X, LinkedIn, Reddit, Discord, WeChat, Jike, and
similar communities.

## Positioning

Primary line:

> Local flight recorder for AI browser agents.

Expanded pitch:

BrowserTrace records what a browser agent saw, clicked, decided, and returned at
each step. When a Browser Use, Stagehand, Playwright + LLM, Skyvern, or
computer-use run fails, developers can open a local timeline with screenshots,
URLs, actions, model input/output, errors, and an exportable HTML report.

The most important memory hook is the before/after:

- Before: 1500 lines of logs and no idea what step 47 saw.
- After: open localhost, jump to the failed step, inspect screenshot and model
  I/O.

## Audience

The first launch should focus on developers already feeling browser-agent
debugging pain:

- Browser Use, Stagehand, Playwright + LLM, Skyvern, and computer-use builders.
- AI infra and observability developers who understand traces but need browser
  state, not just LLM call logs.
- OSS/devtools audiences on Hacker News and Product Hunt.
- Chinese AI builder communities on WeChat, Jike, X, and Xiaohongshu.

The first audience is narrow by design. General AI audiences are too broad
unless the post shows a concrete failure trace.

## Growth Strategy

Recommended approach: demo-first, community-paced launch.

1. Improve the repo share surface before wide posting.
2. Ship one excellent demo GIF and one zero-install exported HTML trace.
3. Start with warm/owned communities to gather early feedback.
4. Use feedback to tighten the README and launch copy.
5. Run Show HN only when the project is easy to try and the owner can reply.
6. Use Product Hunt after assets are strong enough for a broader maker audience.
7. Spend the rest of the week replying, fixing sharp edges, and turning
   feedback into visible issues or PRs.

This beats a one-day blast because each channel teaches the next one, and it
reduces the risk of wasting Show HN or Product Hunt with weak first-run assets.

## Channel Rules

Hacker News Show HN is appropriate only when people can try what was made. The
submission must not be a landing page, signup page, or fundraiser, and the owner
should not ask friends to upvote or comment. BrowserTrace qualifies only if the
demo and install path stay low-friction.

Product Hunt should use a personal maker account. Product Hunt allows sharing
the launch link, but the ask should be to visit, try, and comment, not to upvote.
The launch should use prepared visuals, a clear tagline, a maker comment, and a
demo link.

Reddit should be treated as community engagement, not a posting surface. Avoid
mass posting repeated links. Post only where self-promotion is allowed or where
the post stands alone as a useful debugging write-up.

## Deliverables

Repo and demo assets:

- Dynamic demo recorder that can record the latest failed run instead of a stale
  hardcoded run ID.
- Fresh demo GIF or screenshot sequence showing the failed-step timeline.
- GitHub social preview candidate at 1280 x 640 and under 1 MB.
- Current release asset links and canonical `aaronlab` links.
- README first screen with crisp hook, demo, and 60-second try path.

Launch assets:

- `LAUNCH.md` as the owner-facing launch control room.
- Channel-specific copy for HN, Product Hunt, X, LinkedIn, Reddit, WeChat, Jike,
  and Xiaohongshu.
- Response templates for praise, bug reports, skeptical comments, comparison
  questions, and cloud/security questions.
- Outreach target list with one relevant ask per community.
- Daily metrics checklist: stars, visitors if available, issues, discussions,
  comments, forks, release downloads, and recurring objections.

## 7-Day Schedule

Day 0: asset hardening

- Fix demo recorder.
- Generate or refresh demo media.
- Verify release, README, badges, discussions, and canonical links.
- Prepare final post copy and response templates.

Day 1: warm launch

- Publish X/LinkedIn and Chinese community posts.
- Ask for feedback, not stars.
- Create issues for repeated requests within the same day.

Day 2: Show HN

- Submit `Show HN: BrowserTrace - record and replay AI browser-agent runs to
  find bugs` if Day 1 feedback shows the first-run path is understandable.
- Owner stays available for comments.
- Reply technically and briefly; never paste generated comments.

Day 3: targeted communities

- Share a value-first debugging write-up in one or two relevant communities.
- Prefer Browser Use, Stagehand, Playwright, Skyvern, or local AI-agent groups
  over generic startup communities.

Day 4: Product Hunt prep

- Prepare listing images, tagline, first maker comment, and demo link.
- Schedule only if the visual assets are strong and the owner can monitor the
  launch.

Day 5: tutorial content

- Publish a practical post: "How to debug a browser agent failure with
  screenshots and model I/O."
- Link BrowserTrace as the reproducible example.

Day 6: integration outreach

- Open or comment on relevant integration issues where welcome.
- Invite adapter PRs for Skyvern and other browser-agent frameworks.

Day 7: retrospective and second iteration

- Audit stars, comments, issues, and drop-off points.
- Ship one visible improvement from launch feedback.
- Decide whether to run Product Hunt, defer it, or use another dev community.

## Success Metrics

Primary metric:

- Current GitHub `stargazerCount > 1000` for `aaronlab/browsertrace`.

Leading indicators:

- 50+ stars: first messaging works outside warm network.
- 100+ stars: Show HN or a community post resonated.
- 250+ stars: repo is shareable without personal explanation.
- 500+ stars: broader AI/devtools audience understands the category.
- 1000+ stars: launch plus follow-up loops have reached durable visibility.

Behavioral indicators:

- Users open issues with concrete framework requests.
- Users ask for cloud/share/team workflow.
- Users compare BrowserTrace to Langfuse, LangSmith, Browserbase, or Laminar.
- Maintainers or framework users mention integrations.

## Risks

Weak demo:

- Mitigation: record a simple, deterministic failure first. A polished but fake
  scenario is less valuable than a clear trace of what broke.

Over-broad audience:

- Mitigation: lead with browser-agent failure pain, not generic AI observability.

Spam perception:

- Mitigation: one post per channel, tailored copy, no mass DM, no direct upvote
  asks, and real technical replies.

Owner availability:

- Mitigation: prepare response templates and avoid submitting to HN/Product Hunt
  unless the owner can monitor the thread.

PyPI not published:

- Mitigation: keep GitHub install path prominent until credentials are available.
  If PyPI becomes available, update install commands immediately.

## Verification

Before each public launch step:

- `gh repo view aaronlab/browsertrace --json owner,url,homepageUrl,stargazerCount`
  shows canonical `aaronlab` ownership and current stars.
- `uv run --python 3.11 --extra dev pytest -q` passes.
- README install and demo commands work from a clean checkout.
- Release asset link opens without authentication.
- Demo media is present and renders in the README.
- No launch copy asks directly for upvotes or stars.

The active objective remains incomplete until the primary metric is achieved.
