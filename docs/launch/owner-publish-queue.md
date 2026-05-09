# BrowserTrace Owner Publish Queue

This queue lists the launch actions that require the owner's personal accounts,
login sessions, 2FA, and human replies. Codex can prepare and audit everything
around these steps, but the owner must click publish.

Do not ask for stars, upvotes, or vote swaps. Ask for workflow feedback from
people building browser agents.

## Ready Links

- Repo: https://github.com/aaronlab/browsertrace
- Live demo: https://aaronlab.github.io/browsertrace/
- Walkthrough: https://aaronlab.github.io/browsertrace/debug-browser-agent-failure.html
- Release: https://github.com/aaronlab/browsertrace/releases/tag/v0.1.7
- Launch discussion: https://github.com/aaronlab/browsertrace/discussions/6
- Feedback issue: https://github.com/aaronlab/browsertrace/issues/3

## Media

- Primary video: `docs/demo.mp4`
- Poster image: `docs/demo-poster.png`
- Backup GIF: `docs/demo.gif`
- Social preview: `docs/social-preview.png`
- Press kit: `docs/launch/press-kit.md`

## Day 1 Warm Launch

Use `docs/launch/day-1-publish-packet.md` as the single owner-facing checklist.

1. X
   - Use the `## X` draft in `docs/launch/channel-copy.md`.
   - Attach `docs/demo.mp4`.
   - Pin the post for 48 hours only if it gets real replies.
2. LinkedIn
   - Use the `## LinkedIn` draft in `docs/launch/channel-copy.md`.
   - Attach `docs/demo.mp4` or `docs/demo-poster.png`.
   - Ask what context people need when their browser agent fails.
3. WeChat groups
   - Use the `## WeChat Group` draft in `docs/launch/channel-copy.md`.
   - Post to one or two relevant AI-builder groups first.
   - Reply with the live demo before asking anyone to install locally.
4. Jike
   - Use the `## Jike` draft in `docs/launch/channel-copy.md`.
   - Keep the tone conversational and ask for builders who use Browser Use,
     Stagehand, Playwright + LLM, or computer-use agents.

After each post, append a metrics row and save the post URL plus notable replies
in `docs/launch/metrics-log.md`.

```bash
uv run --python 3.11 python scripts/launch_metrics.py --append --note "after X post: <post URL>"
```

## Day 2 Developer Discovery

1. Hacker News Show HN
   - Use `docs/launch/day-2-show-hn-packet.md` as the submission checklist.
   - Use the `## Hacker News` title and first comment draft in
     `docs/launch/channel-copy.md`.
   - Submit only when the owner can reply for several hours.
   - Do not ask anyone to upvote.
2. Targeted communities
   - Use `docs/launch/outreach-targets.md` to pick one high-fit community.
   - Prefer Browser Use, Stagehand, Playwright, or Skyvern users over generic AI
     communities.
   - Check rules first; if self-promotion is restricted, share the walkthrough
     only when it answers an existing debugging thread.

## Day 3-5 Broader Posts

Use `docs/launch/day-3-targeted-communities-packet.md` before posting in
Browser Use, Stagehand, Playwright, or Skyvern communities.

0. PyPI publishing
   - Configure PyPI Trusted Publishing from `docs/release/pypi-publishing.md`.
   - Run the `Publish` workflow only after PyPI is configured.
   - After publish verification, update public posts to use
     `pip install "browsertrace[ui]"`.
1. Reddit or Discord
   - Use the value-first Reddit draft in `docs/launch/channel-copy.md`.
   - Lead with the debugging walkthrough, not the repo.
2. Product Hunt draft
   - Use `docs/launch/day-4-product-hunt-packet.md` as the listing checklist.
   - Use the Product Hunt tagline, description, maker comment, and first comment
     from `docs/launch/channel-copy.md`.
   - Prepare the listing before launch day; do not launch unless the owner can
     reply throughout the day.
3. Xiaohongshu
   - Use the `## Xiaohongshu` draft in `docs/launch/channel-copy.md`.
   - Use `docs/demo-poster.png` as the first image and mention
     `aaronlab/browsertrace` plainly.
4. Chinese long-form
   - Use `docs/launch/chinese-tutorial-post.md`.
   - Publish only where technical OSS posts are welcome.
   - Ask for browser-agent debugging workflow feedback, not stars or reposts.

## Reply Workflow

- Use `docs/launch/response-templates.md` as notes, not as copy-paste replies.
- For bug reports, ask the user to open an issue with their agent stack, trace
  type, and whether the failing step involved screenshots, selectors, or model
  output.
- For public trace sharing, ask them to run
  `browsertrace export <run_id> --redact -o public.html` before attaching files
  to issues or posts.
- For integration requests, point to the v0.2 milestone and ask which adapter
  would unblock them first.

## Metrics Check

Run after each major post:

```bash
uv run --python 3.11 python scripts/launch_metrics.py --append --note "after <channel>: <post URL>"
uv run --python 3.11 python scripts/launch_metrics.py --json
gh issue list --repo aaronlab/browsertrace --state all --limit 20
```
