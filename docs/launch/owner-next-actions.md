# BrowserTrace Owner Next Actions

This is the shortest owner-facing checklist. Use it when the repo is ready and
the owner can perform account/login actions personally.

Chinese version: `docs/launch/owner-next-actions.zh-CN.md`

Do not ask for stars, upvotes, reposts, vote swaps, or artificial engagement.
Ask for workflow feedback from people building browser agents.

## 1. Unblock PyPI

This is the highest-friction launch blocker. Public posts convert better after
the install command becomes:

```bash
pip install "browsertrace[ui]"
```

If you must post before PyPI is configured, use the tested no-install `uvx`
trial path in replies:

```bash
uvx --from "browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.11" browsertrace demo
uvx --from "browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.11" browsertrace list
uvx --from "browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.11" browsertrace
```

Configure PyPI Trusted Publisher:

| Field | Value |
|---|---|
| PyPI project | `browsertrace` |
| GitHub owner | `aaronlab` |
| GitHub repository | `browsertrace` |
| Workflow filename | `publish.yml` |
| Environment name | `pypi` |

Then run:

```bash
gh workflow run Publish --repo aaronlab/browsertrace
```

Verification after publish:

```bash
python -m pip index versions browsertrace
pipx run --spec "browsertrace[ui]" browsertrace --help
```

Tracking issue: https://github.com/aaronlab/browsertrace/issues/5

## 2. Maintain The GitHub Profile README

The live public profile README repo is now `aaronlab/aaronlab`. The old
`aaronlab/aaronagent` repo is only a redirect for old traffic.

Use this source draft when refreshing the profile README:

```text
docs/launch/github-profile-readme.md
```

Keep BrowserTrace as the first featured project during launch.

Tracking issue: https://github.com/aaronlab/browsertrace/issues/13

## 3. Upload The GitHub Social Preview

GitHub link previews still need the repository-level image uploaded manually.
Use the ready asset:

```text
docs/social-preview.png
```

In GitHub, open repository Settings -> General -> Social preview and upload the
PNG. This should happen before external posts so shared links show the
BrowserTrace card instead of a generated GitHub card.

Tracking issue: https://github.com/aaronlab/browsertrace/issues/15

## 4. Submit The Sitemap To Search Consoles

Search indexing is a slower growth channel, but it compounds after launch. The
sitemap and robots file are already live:

```text
https://aaronlab.github.io/browsertrace/sitemap.xml
https://aaronlab.github.io/browsertrace/robots.txt
```

Use:

```text
docs/launch/search-indexing-submission.md
```

Tracking issue: https://github.com/aaronlab/browsertrace/issues/16

## 5. Publish Day 1 Posts

Use this packet:

```text
docs/launch/day-1-publish-packet.md
```

Recommended order:

1. X
2. LinkedIn
3. One or two relevant WeChat AI-builder groups
4. Jike

Use `docs/demo.mp4` as primary media and `docs/demo-poster.png` as backup.

Tracking issue: https://github.com/aaronlab/browsertrace/issues/9

## 6. Submit Directories And Newsletters

Use:

```text
docs/launch/directory-submission-sheet.md
docs/launch/outreach-targets.md
```

Submit once per target. Do not repeatedly submit or ask for votes.

Tracking issue: https://github.com/aaronlab/browsertrace/issues/10

## 7. Submit High-Fit GitHub Awesome List PRs

Use:

```text
docs/launch/github-awesome-list-submissions.md
```

Start with `angrykoala/awesome-browser-automation`. Submit one focused PR and
wait for maintainer feedback before trying lower-fit lists.

Tracking issue: https://github.com/aaronlab/browsertrace/issues/18

## 8. Record Metrics After Each Action

After every public post, profile update, PyPI publish, or directory submission:

```bash
uv run --python 3.11 python scripts/launch_metrics.py --append --note "after <action>: <URL or note>"
uv run --python 3.11 python scripts/launch_metrics.py --json
```

The goal remains incomplete until GitHub reports more than 1000 stars:

```bash
gh repo view aaronlab/browsertrace --json stargazerCount,url,homepageUrl,owner
```
