# BrowserTrace Owner Next Actions

This is the shortest owner-facing checklist. Use it when the repo is ready and
the owner can perform account/login actions personally.

Chinese version: `docs/launch/owner-next-actions.zh-CN.md`

Do not ask for stars, upvotes, reposts, vote swaps, or artificial engagement.
Ask for workflow feedback from people building browser agents.

## 10-Minute Owner Unblock

If you only have one short session, do these in order and let Codex handle the
follow-up verification, README updates, metrics, and issue comments:

1. Configure PyPI Trusted Publisher at https://pypi.org/manage/account/publishing/
   with the exact values in section 1.
2. Upload `docs/social-preview.png` in
   https://github.com/aaronlab/browsertrace/settings under General -> Social
   preview.
3. Pin `aaronlab/browsertrace` from the GitHub profile page with
   Profile -> Customize your pins.
4. Publish the Day 1 X/LinkedIn/WeChat/Jike posts from
   `docs/launch/day-1-publish-packet.md`, using `docs/demo.mp4`.

After step 1, tell Codex "PyPI is configured" so it can run the publish workflow
and replace GitHub-tag install commands with normal `pip install` commands.
After steps 2-4, send the posted URLs or a short channel note so Codex can log
metrics and update the tracking issues.

## 1. Unblock PyPI

This is the highest-friction launch blocker. Public posts convert better after
the install command becomes:

```bash
pip install "browsertrace[ui]"
```

If you must post before PyPI is configured, use the tested no-install `uvx`
trial path in replies:

```bash
uvx --from "browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.13" browsertrace doctor
uvx --from "browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.13" browsertrace demo
uvx --from "browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.13" browsertrace list
uvx --from "browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.13" browsertrace
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

Pin BrowserTrace on the public GitHub profile:

```text
Profile -> Customize your pins -> aaronlab/browsertrace
```

The GitHub API available here does not expose profile pinning, so this must be
done once in the GitHub UI.

Profile pinning tracking issue:
https://github.com/aaronlab/browsertrace/issues/24

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

## 7. Monitor High-Fit GitHub Awesome List PRs

Use:

```text
docs/launch/github-awesome-list-submissions.md
```

The three prepared PRs are already open:

- `angrykoala/awesome-browser-automation#112`
- `mxschmitt/awesome-playwright#136`
- `Jenqyang/Awesome-AI-Agents#220`

Monitor maintainer feedback and do not open additional list PRs until one of
these receives a response.

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
