# BrowserTrace Metrics Log

Append one row after each meaningful public post or product update. This is the
source of truth for whether a channel actually moves GitHub adoption.

The active objective remains incomplete until GitHub reports at least 1001
stars for `aaronlab/browsertrace`.

## How to Append

```bash
uv run --python 3.11 python scripts/launch_metrics.py --append --note "baseline before Day 1 posts"
uv run --python 3.11 python scripts/launch_metrics.py --append --note "after X and LinkedIn posts"
uv run --python 3.11 python scripts/launch_metrics.py --json
```

## Log

| Captured at | Stars | To 1001 | Forks | Watchers | Issues | PRs | Release downloads | Note |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| 2026-05-09T08:30:00+00:00 | 3 | 998 | 0 | 0 | 3 | 0 | 0 | Baseline before owner Day 1 publish actions |
| 2026-05-09T08:39:38+00:00 | 3 | 998 | 0 | 0 | 3 | 0 | 0 | after metrics tracker added |
| 2026-05-09T09:00:57+00:00 | 3 | 998 | 0 | 0 | 3 | 0 | 0 | after GitHub launch discussion update: https://github.com/aaronlab/browsertrace/discussions/6#discussioncomment-16860867 |
| 2026-05-09T09:06:15+00:00 | 3 | 998 | 0 | 0 | 3 | 0 | 0 | after Skyvern wrapper issue update: https://github.com/aaronlab/browsertrace/issues/4#issuecomment-4412113944 |
| 2026-05-09T09:14:55+00:00 | 3 | 998 | 0 | 0 | 3 | 0 | 0 | after v0.1.2 release: https://github.com/aaronlab/browsertrace/releases/tag/v0.1.2 |
| 2026-05-09T09:17:29+00:00 | 3 | 998 | 0 | 0 | 3 | 0 | 0 | after v0.1.2 public follow-up: discussion https://github.com/aaronlab/browsertrace/discussions/6#discussioncomment-16861042 and PyPI issue https://github.com/aaronlab/browsertrace/issues/5#issuecomment-4412137133 |
| 2026-05-09T09:19:19+00:00 | 3 | 998 | 0 | 0 | 3 | 0 | 0 | after GitHub repo description update to include Skyvern |
| 2026-05-09T09:21:06+00:00 | 3 | 998 | 0 | 0 | 3 | 0 | 0 | after PyPI issue title update: https://github.com/aaronlab/browsertrace/issues/5 |
| 2026-05-09T09:25:05+00:00 | 3 | 998 | 0 | 0 | 3 | 0 | 0 | after integrations landing page published: https://aaronlab.github.io/browsertrace/integrations.html |
| 2026-05-09T09:28:03+00:00 | 3 | 998 | 0 | 0 | 3 | 0 | 1 | after README and homepage integration link audit |
| 2026-05-09T09:33:19+00:00 | 3 | 998 | 0 | 0 | 3 | 0 | 1 | after custom GitHub Pages workflow deployment: https://github.com/aaronlab/browsertrace/actions/runs/25597763887 |
| 2026-05-09T09:37:29+00:00 | 3 | 998 | 0 | 0 | 3 | 0 | 1 | after Skyvern example and issue update: https://github.com/aaronlab/browsertrace/issues/4#issuecomment-4412182416 |
| 2026-05-09T09:40:39+00:00 | 3 | 998 | 0 | 0 | 3 | 0 | 1 | after Stagehand wrapper example: https://github.com/aaronlab/browsertrace/commit/6dcb4fd13d42519428cc4a406ed439975efd241f |
| 2026-05-09T09:43:32+00:00 | 3 | 998 | 0 | 0 | 3 | 0 | 1 | after examples guide: https://github.com/aaronlab/browsertrace/tree/main/examples |
| 2026-05-09T09:46:37+00:00 | 3 | 998 | 0 | 0 | 3 | 0 | 1 | after packaging metadata update: https://github.com/aaronlab/browsertrace/commit/415035846821195d7e42272a40c4f9d27d1b1f6f |
| 2026-05-09T09:48:42+00:00 | 3 | 998 | 0 | 0 | 3 | 0 | 1 | after PyPI issue body refresh: https://github.com/aaronlab/browsertrace/issues/5 |
| 2026-05-09T09:51:06+00:00 | 3 | 998 | 0 | 0 | 3 | 0 | 1 | after v0.1.2 discussion refresh: https://github.com/aaronlab/browsertrace/discussions/6 |
| 2026-05-09T09:55:53+00:00 | 3 | 998 | 0 | 0 | 3 | 0 | 1 | after v0.1.3 release: https://github.com/aaronlab/browsertrace/releases/tag/v0.1.3 |
| 2026-05-09T09:59:00+00:00 | 3 | 998 | 0 | 0 | 3 | 0 | 1 | after README GitHub install pinned to v0.1.3: https://github.com/aaronlab/browsertrace/commit/16d33636ef7890fc13dc44e7cf5593f1943feb8d |
| 2026-05-09T10:01:19+00:00 | 3 | 998 | 0 | 0 | 4 | 0 | 1 | after roadmap cleanup: milestone v0.2 updated, Stagehand issue https://github.com/aaronlab/browsertrace/issues/8, Skyvern help-wanted label https://github.com/aaronlab/browsertrace/issues/4 |
| 2026-05-09T10:03:53+00:00 | 3 | 998 | 0 | 0 | 4 | 0 | 1 | after changelog added: https://github.com/aaronlab/browsertrace/blob/main/CHANGELOG.md |
| 2026-05-09T10:05:56+00:00 | 3 | 998 | 0 | 0 | 4 | 0 | 1 | after v0.1.3 release notes refresh: https://github.com/aaronlab/browsertrace/releases/tag/v0.1.3 |
| 2026-05-09T10:07:48+00:00 | 3 | 998 | 0 | 0 | 5 | 0 | 1 | after owner Day 1 launch checklist issue: https://github.com/aaronlab/browsertrace/issues/9 |
| 2026-05-09T10:15:25+00:00 | 3 | 998 | 0 | 0 | 5 | 0 | 0 | after v0.1.4 redacted export release: https://github.com/aaronlab/browsertrace/releases/tag/v0.1.4 |
| 2026-05-09T10:16:44+00:00 | 3 | 998 | 0 | 0 | 5 | 0 | 0 | after PyPI issue and Day 1 checklist refresh for v0.1.4: https://github.com/aaronlab/browsertrace/issues/5 and https://github.com/aaronlab/browsertrace/issues/9#issuecomment-4412270684 |
| 2026-05-09T10:17:59+00:00 | 3 | 998 | 0 | 0 | 5 | 0 | 0 | after GitHub topic refresh: added browser-agents topic |
| 2026-05-09T10:19:14+00:00 | 3 | 998 | 0 | 0 | 5 | 0 | 0 | after redacted sharing docs in walkthrough and tutorial drafts |
| 2026-05-09T10:20:20+00:00 | 3 | 998 | 0 | 0 | 5 | 0 | 0 | after Day 1 issue body update to v0.1.4 and redacted export command |
| 2026-05-09T10:22:51+00:00 | 3 | 998 | 0 | 0 | 5 | 0 | 0 | after directory and newsletter outreach targets added |
| 2026-05-09T10:23:58+00:00 | 3 | 998 | 0 | 0 | 6 | 0 | 0 | after directory/newsletter owner-action issue: https://github.com/aaronlab/browsertrace/issues/10 |
| 2026-05-09T10:29:51+00:00 | 3 | 998 | 0 | 0 | 6 | 0 | 0 | after v0.1.5 packaged demo command release: https://github.com/aaronlab/browsertrace/releases/tag/v0.1.5 |
| 2026-05-09T10:30:32+00:00 | 3 | 998 | 0 | 0 | 6 | 0 | 0 | after owner-action issues updated to v0.1.5 and browsertrace demo quickstart |
| 2026-05-09T10:34:09+00:00 | 3 | 998 | 0 | 0 | 6 | 0 | 0 | after v0.1.6 full model I/O HTML export release: https://github.com/aaronlab/browsertrace/releases/tag/v0.1.6 |
| 2026-05-09T10:34:48+00:00 | 3 | 998 | 0 | 0 | 6 | 0 | 0 | after owner-action issues updated to v0.1.6 full model I/O export |
| 2026-05-09T10:37:48+00:00 | 3 | 998 | 0 | 0 | 6 | 0 | 0 | after Browser Use debugging landing page added |
| 2026-05-09T10:39:45+00:00 | 3 | 998 | 0 | 0 | 7 | 0 | 0 | after Browser Use adapter feedback issue: https://github.com/aaronlab/browsertrace/issues/11 |
| 2026-05-09T10:41:48+00:00 | 3 | 998 | 0 | 0 | 7 | 0 | 0 | after Stagehand debugging landing page added |
| 2026-05-09T10:45:31+00:00 | 3 | 998 | 0 | 0 | 7 | 0 | 0 | after Skyvern debugging landing page added |
| 2026-05-09T10:47:56+00:00 | 3 | 998 | 0 | 0 | 7 | 0 | 0 | after Playwright LLM debugging landing page added |
| 2026-05-09T10:49:38+00:00 | 3 | 998 | 0 | 0 | 7 | 0 | 0 | after owner launch checklist issues updated with stack landing pages |
| 2026-05-09T10:52:41+00:00 | 3 | 998 | 0 | 0 | 7 | 0 | 0 | after comparison landing page added |
| 2026-05-09T10:55:33+00:00 | 3 | 998 | 0 | 0 | 7 | 0 | 0 | after Browser Use no-dependency callback demo added |
| 2026-05-09T10:57:03+00:00 | 3 | 998 | 0 | 0 | 8 | 0 | 0 | after Playwright LLM feedback issue: https://github.com/aaronlab/browsertrace/issues/12 |
| 2026-05-09T11:01:56+00:00 | 3 | 998 | 0 | 0 | 8 | 0 | 0 | after v0.1.7 release: https://github.com/aaronlab/browsertrace/releases/tag/v0.1.7 |
| 2026-05-09T11:02:33+00:00 | 3 | 998 | 0 | 0 | 8 | 0 | 0 | after owner issues updated for v0.1.7 |
| 2026-05-09T11:05:24+00:00 | 3 | 998 | 0 | 0 | 8 | 0 | 0 | after directory submission sheet added |
| 2026-05-09T11:05:48+00:00 | 3 | 998 | 0 | 0 | 8 | 0 | 0 | after directory submission issue updated: https://github.com/aaronlab/browsertrace/issues/10#issuecomment-4412372147 |
| 2026-05-09T11:07:41+00:00 | 3 | 998 | 0 | 0 | 8 | 0 | 0 | after v0.1.7 launch discussion update: https://github.com/aaronlab/browsertrace/discussions/6#discussioncomment-16861693 |
| 2026-05-09T11:14:03+00:00 | 3 | 998 | 0 | 0 | 8 | 0 | 0 | after v0.1.8 screenshot redaction release: https://github.com/aaronlab/browsertrace/releases/tag/v0.1.8 |
| 2026-05-09T11:14:35+00:00 | 3 | 998 | 0 | 0 | 8 | 0 | 0 | after v0.1.8 launch discussion and owner issue update |
| 2026-05-09T11:18:45+00:00 | 3 | 998 | 0 | 0 | 8 | 0 | 0 | after v0.1.9 URL redaction release: https://github.com/aaronlab/browsertrace/releases/tag/v0.1.9 |
| 2026-05-09T11:19:07+00:00 | 3 | 998 | 0 | 0 | 8 | 0 | 0 | after v0.1.9 launch discussion and owner issue update |
| 2026-05-09T11:27:21+00:00 | 3 | 998 | 0 | 0 | 8 | 0 | 0 | after v0.1.10 public export release and launch surface update: https://github.com/aaronlab/browsertrace/releases/tag/v0.1.10 |
| 2026-05-09T11:44:57+00:00 | 3 | 998 | 0 | 0 | 8 | 0 | 0 | after v0.2 milestone and public feedback issue cleanup |
| 2026-05-09T11:48:03+00:00 | 3 | 998 | 0 | 0 | 8 | 0 | 0 | after public-safe demo release asset added: https://github.com/aaronlab/browsertrace/releases/download/v0.1.10/browsertrace-demo-public.html |
| 2026-05-09T11:51:36+00:00 | 3 | 998 | 0 | 0 | 8 | 0 | 0 | after public-safe demo asset linked from launch docs |
| 2026-05-09T11:53:36+00:00 | 3 | 998 | 0 | 0 | 8 | 0 | 0 | after owner action issues linked public-safe demo asset: #9 #10 |
| 2026-05-09T11:55:38+00:00 | 3 | 998 | 0 | 0 | 8 | 0 | 0 | after homepage SoftwareSourceCode structured data update |
| 2026-05-09T11:56:57+00:00 | 3 | 998 | 0 | 0 | 8 | 0 | 0 | after PyPI blocker issue refreshed for v0.1.10 |
| 2026-05-09T11:58:48+00:00 | 3 | 998 | 0 | 0 | 8 | 0 | 1 | after public-safe demo linked from remaining launch packets |
| 2026-05-09T12:00:22+00:00 | 3 | 998 | 0 | 0 | 8 | 0 | 1 | after public-safe demo linked from long-form tutorial drafts |
| 2026-05-09T12:02:44+00:00 | 3 | 998 | 0 | 0 | 8 | 0 | 3 | after launch metrics traffic tracking added; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T12:05:01+00:00 | 3 | 998 | 0 | 0 | 8 | 0 | 3 | after code of conduct added for OSS trust; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T12:07:44+00:00 | 3 | 998 | 0 | 0 | 8 | 0 | 3 | after aaronlab profile README draft added; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T12:09:06+00:00 | 3 | 998 | 0 | 0 | 9 | 0 | 3 | after profile README owner-action issue opened: https://github.com/aaronlab/browsertrace/issues/13; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T12:11:10+00:00 | 3 | 998 | 0 | 0 | 9 | 0 | 4 | after launch discussion refreshed with public-safe demo and traffic metrics: https://github.com/aaronlab/browsertrace/discussions/6#discussioncomment-16861997; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T12:13:07+00:00 | 3 | 998 | 0 | 0 | 9 | 0 | 4 | after owner-action and launch-blocker labels applied to launch queue; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T12:14:54+00:00 | 3 | 998 | 0 | 0 | 9 | 0 | 4 | after examples README install path updated to v0.1.10; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T12:16:00+00:00 | 3 | 998 | 0 | 0 | 10 | 0 | 4 | after good first issue opened for first-run demo troubleshooting: https://github.com/aaronlab/browsertrace/issues/14; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T12:18:11+00:00 | 3 | 998 | 0 | 0 | 10 | 0 | 4 | after profile and good-first issues added to v0.2 milestone; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T12:20:02+00:00 | 3 | 998 | 0 | 0 | 10 | 0 | 4 | after changelog public-safe release asset note added; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T12:21:48+00:00 | 3 | 998 | 0 | 0 | 10 | 0 | 4 | after shortest owner next-actions checklist added; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T12:24:36+00:00 | 3 | 998 | 0 | 0 | 10 | 0 | 4 | after current AI/OSS directory targets added to submission queue; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T12:26:05+00:00 | 3 | 998 | 0 | 0 | 10 | 0 | 6 | after directory submission issue updated with current targets: https://github.com/aaronlab/browsertrace/issues/10#issuecomment-4412513951; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T12:27:40+00:00 | 3 | 998 | 1 | 0 | 10 | 0 | 6 | after live audit observed first fork; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T12:28:59+00:00 | 3 | 998 | 1 | 0 | 10 | 0 | 6 | after first external fork source verified: Jah-yee/browsertrace; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T12:32:28+00:00 | 3 | 998 | 1 | 0 | 11 | 0 | 6 | after social preview owner-action issue #15; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T12:35:45+00:00 | 3 | 998 | 1 | 0 | 11 | 0 | 6 | after launch discussion social-preview/SEO update: https://github.com/aaronlab/browsertrace/discussions/6#discussioncomment-16862100; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T12:38:51+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 6 | after search indexing owner-action issue #16; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T12:39:48+00:00 | 3 | 998 | 1 | 0 | 12 | 1 | 6 | after launch discussion search-indexing update: https://github.com/aaronlab/browsertrace/discussions/6#discussioncomment-16862122; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T12:42:51+00:00 | 3 | 998 | 1 | 0 | 11 | 0 | 6 | after first external contributor PR merged: https://github.com/aaronlab/browsertrace/pull/17; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T12:46:09+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 6 | after GitHub awesome-list owner-action issue #18; traffic views 48/25 unique, clones 100/52 unique |
