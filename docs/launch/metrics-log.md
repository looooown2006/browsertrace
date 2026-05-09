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
| 2026-05-09T12:49:11+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 6 | after fresh PyPI blocker audit: https://github.com/aaronlab/browsertrace/issues/5#issuecomment-4412558067; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T12:51:29+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 6 | after standalone roadmap added for contributor onboarding; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T12:53:08+00:00 | 3 | 998 | 1 | 0 | 13 | 0 | 6 | after new good-first issue for Windows PowerShell first-run docs: https://github.com/aaronlab/browsertrace/issues/19; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T12:55:18+00:00 | 3 | 998 | 1 | 0 | 13 | 0 | 6 | after local PR-ready awesome-playwright branch prepared: https://github.com/aaronlab/browsertrace/issues/18#issuecomment-4412569111; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T12:57:33+00:00 | 3 | 998 | 1 | 0 | 13 | 0 | 6 | after local PR-ready Awesome-AI-Agents branch prepared: https://github.com/aaronlab/browsertrace/issues/18#issuecomment-4412572970; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T13:00:10+00:00 | 3 | 998 | 1 | 0 | 13 | 0 | 6 | after GitHub profile draft refresh: https://github.com/aaronlab/browsertrace/issues/13#issuecomment-4412577175; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T13:02:06+00:00 | 3 | 998 | 1 | 0 | 13 | 0 | 6 | after Chinese owner next-actions checklist added; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T13:05:18+00:00 | 3 | 998 | 1 | 0 | 13 | 0 | 6 | after PyPI discovery metadata update; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T13:08:53+00:00 | 3 | 998 | 1 | 0 | 13 | 0 | 6 | after v0.1.10 release notes conversion update: https://github.com/aaronlab/browsertrace/releases/tag/v0.1.10; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T13:11:37+00:00 | 3 | 998 | 1 | 0 | 13 | 0 | 6 | after Windows PowerShell first-run docs update for issue #19; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T13:14:24+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 6 | after uvx GitHub no-install quickstart added to docs and v0.1.10 release; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T13:17:14+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 6 | after launch publish packets updated with uvx no-install trial; traffic views 48/25 unique, clones 100/52 unique |
| 2026-05-09T13:19:30+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 6 | after longform launch posts updated with uvx no-install trial; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T13:21:35+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 6 | after PyPI blocker issue updated with uvx no-install workaround: https://github.com/aaronlab/browsertrace/issues/5#issuecomment-4412618379; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T13:23:22+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 6 | after launch discussion updated with uvx no-install trial: https://github.com/aaronlab/browsertrace/discussions/6#discussioncomment-16862345; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T13:25:33+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 6 | after Day 1 owner issue updated with uvx no-install trial: https://github.com/aaronlab/browsertrace/issues/9; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T13:27:56+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 6 | after directory submission sheet and issue #10 updated with uvx no-install trial; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T13:30:25+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 6 | after awesome-list submission notes and issue #18 updated with reviewer links and uvx trial; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T13:32:44+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 6 | after owner next-actions checklists updated with uvx fallback before PyPI; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T13:34:59+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 6 | after LAUNCH control room refreshed with current audit and uvx fallback; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T13:39:32+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 6 | after Day 3 outreach uvx fallback; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T13:42:02+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 6 | after stale public release-reference cleanup; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T13:43:55+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 6 | after launch feedback issue #3 uvx trial update; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T13:47:14+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 6 | after awesome-browser-automation PR #112 submitted; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T13:49:51+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 6 | after Publish workflow trusted-publisher permission guard; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T13:54:02+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 6 | after old aaronagent profile repo redirected to BrowserTrace; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T13:56:12+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 6 | after old aaronagent repo metadata redirected to BrowserTrace; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T13:59:02+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 6 | after awesome-playwright PR #136 submitted; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T14:01:43+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 6 | after Awesome-AI-Agents PR #220 submitted; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T14:08:11+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 0 | after v0.1.11 doctor release published and uvx verified; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T14:11:18+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 0 | after old aaronagent redirect updated to v0.1.11 doctor path; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T14:17:16+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 0 | after issue body v0.1.11 sync; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T14:22:38+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 0 | after uvx-first quickstart docs update; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T14:25:59+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 0 | after live aaronlab profile README created; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T14:27:16+00:00 | 3 | 998 | 1 | 0 | 11 | 0 | 0 | after profile README issue #13 closed; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T14:29:13+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 0 | after good-first issue #20 and examples uvx quickstart update; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T14:32:30+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 0 | after README contributing path update; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T14:35:38+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 0 | after launch discussion #6 updated to v0.1.11 uvx path; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T14:37:58+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 0 | after owner-action issues #9 and #10 uvx-first sync; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T14:39:32+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 0 | after launch feedback issue #3 uvx-first sync; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T14:42:27+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 0 | after PyPI metadata twine-check audit; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T14:44:08+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 0 | after homepage uvx quickstart added; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T14:48:22+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 1 | after awesome-playwright PR #136 lint verification comment; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T14:51:59+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 1 | after awesome-list fork metadata audit; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T14:54:11+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 1 | after homepage quickstart copy button added; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T14:56:22+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 1 | after launch kit quickstart copy block added; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T14:58:58+00:00 | 3 | 998 | 1 | 0 | 13 | 0 | 1 | after Windows PowerShell uvx docs and good-first issue rotation; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T14:59:30+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 1 | after good-first issue #20 closed; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T15:01:44+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 1 | after social preview asset upload instructions verified; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T15:04:05+00:00 | 3 | 998 | 1 | 0 | 12 | 0 | 1 | after guide pages uvx-first quickstart sync; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T15:06:30+00:00 | 3 | 998 | 2 | 0 | 12 | 1 | 1 | after CI/Pages verification and external PR monitoring; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T15:07:09+00:00 | 3 | 998 | 2 | 0 | 12 | 1 | 1 | after awesome-list monitoring update on issue 18; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T15:13:21+00:00 | 3 | 998 | 2 | 0 | 12 | 1 | 1 | after computer-use debugging guide published; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T15:17:48+00:00 | 3 | 998 | 2 | 0 | 12 | 1 | 1 | after computer-use loop example published; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T15:19:36+00:00 | 3 | 998 | 2 | 0 | 12 | 1 | 1 | after profile and feedback issue link computer-use guide; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T15:21:04+00:00 | 3 | 998 | 2 | 0 | 12 | 1 | 1 | after launch discussion computer-use update; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T15:23:24+00:00 | 3 | 998 | 2 | 0 | 12 | 1 | 1 | after search indexing checklist key URL update; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T15:26:15+00:00 | 3 | 998 | 2 | 0 | 12 | 1 | 1 | after computer-use guide copy button; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T15:30:28+00:00 | 3 | 998 | 2 | 0 | 12 | 1 | 1 | after copy buttons added to guide quickstarts; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T15:36:42+00:00 | 3 | 998 | 2 | 0 | 12 | 1 | 0 | after v0.1.12 release published and verified; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T15:47:28+00:00 | 3 | 998 | 2 | 0 | 12 | 1 | 0 | after roadmap and contributor onboarding refresh; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T15:55:12+00:00 | 3 | 998 | 2 | 0 | 11 | 0 | 0 | after external contributor PR #22 merged: uvx troubleshooting note; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T15:58:45+00:00 | 3 | 998 | 2 | 0 | 12 | 0 | 0 | after good-first issue #23 opened and profile links rotated; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T16:00:42+00:00 | 3 | 998 | 2 | 0 | 12 | 0 | 0 | after launch discussion contributor update: https://github.com/aaronlab/browsertrace/discussions/6#discussioncomment-16863200; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T16:04:57+00:00 | 3 | 998 | 2 | 0 | 12 | 0 | 0 | after TechArticle structured data deployed on core guide pages; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T16:08:37+00:00 | 3 | 998 | 2 | 0 | 12 | 0 | 0 | after Show HN first-run replies refreshed with doctor, uvx troubleshooting, and #23 contribution path; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T16:11:42+00:00 | 3 | 998 | 2 | 0 | 12 | 0 | 0 | after README contributors and good-first issue badges added; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T16:14:08+00:00 | 3 | 998 | 2 | 0 | 12 | 0 | 0 | after owner-action issues #5 and #9 refreshed for v0.1.12 and PyPI 404 audit; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T16:17:34+00:00 | 3 | 998 | 2 | 0 | 12 | 0 | 0 | after llms.txt contribution links deployed; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T16:21:02+00:00 | 3 | 998 | 2 | 0 | 12 | 0 | 0 | after core guide pages advertised llms.txt alternate link; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T16:24:09+00:00 | 3 | 998 | 2 | 0 | 12 | 0 | 0 | after press kit trial and contribution paths deployed; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T16:28:39+00:00 | 3 | 998 | 2 | 0 | 12 | 0 | 0 | after launch packets synced with doctor and contribution path; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T16:31:52+00:00 | 3 | 998 | 2 | 0 | 12 | 0 | 0 | after owner launch checklists synced with doctor fallback; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T16:36:03+00:00 | 3 | 998 | 2 | 0 | 12 | 0 | 0 | after launch trial copy synced with doctor first-run path; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T16:39:30+00:00 | 3 | 998 | 2 | 0 | 12 | 0 | 0 | after live aaronlab profile added BrowserTrace trial path; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T16:43:36+00:00 | 3 | 998 | 2 | 0 | 12 | 0 | 0 | after PyPI metadata guide links added; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T16:46:19+00:00 | 3 | 998 | 2 | 0 | 12 | 0 | 0 | after launch discussion updated with current trial and good-first paths: https://github.com/aaronlab/browsertrace/discussions/6#discussioncomment-16863453; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T16:49:55+00:00 | 3 | 998 | 2 | 0 | 12 | 0 | 0 | after sitemap exposed llms.txt discovery URL; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T16:51:49+00:00 | 3 | 998 | 2 | 0 | 12 | 0 | 0 | after live sitemap URL audit: all sitemap entries returned 200; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T16:55:46+00:00 | 3 | 998 | 2 | 0 | 12 | 0 | 0 | after owner checklist added GitHub profile pinning action; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T16:59:54+00:00 | 3 | 998 | 2 | 0 | 13 | 0 | 0 | after profile pinning owner-action issue opened and linked: https://github.com/aaronlab/browsertrace/issues/24; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T17:02:24+00:00 | 3 | 998 | 2 | 0 | 13 | 0 | 0 | after PyPI owner-action issue refreshed for v0.1.12: https://github.com/aaronlab/browsertrace/issues/5; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T17:04:51+00:00 | 3 | 998 | 2 | 0 | 13 | 0 | 0 | after v0.1.12 release notes added live demo, contribution, and discussion links; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T17:07:12+00:00 | 3 | 998 | 2 | 0 | 13 | 0 | 0 | after open issues attached to v0.2 milestone and milestone description refreshed; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T17:11:40+00:00 | 3 | 998 | 2 | 0 | 14 | 0 | 0 | after good-first public-safe export docs issue added to llms.txt: https://github.com/aaronlab/browsertrace/issues/25; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T17:16:10+00:00 | 3 | 998 | 2 | 0 | 14 | 0 | 0 | after live aaronlab profile linked public-safe export docs issue: https://github.com/aaronlab/browsertrace/issues/25; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T17:18:33+00:00 | 3 | 998 | 2 | 0 | 14 | 0 | 0 | after v0.1.12 release notes linked public-safe export docs issue: https://github.com/aaronlab/browsertrace/issues/25; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T17:21:56+00:00 | 3 | 998 | 2 | 0 | 14 | 0 | 0 | after README AI extra install path updated for pre-PyPI users; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T17:23:42+00:00 | 3 | 998 | 2 | 0 | 14 | 0 | 0 | after owner 10-minute unblock checklist added; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T17:26:03+00:00 | 3 | 998 | 2 | 0 | 14 | 0 | 0 | after directory sheet marked awesome-list PRs open; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T17:32:34+00:00 | 3 | 998 | 2 | 0 | 14 | 0 | 0 | after v0.1.13 doctor onboarding release published and uvx verified: https://github.com/aaronlab/browsertrace/releases/tag/v0.1.13; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T17:33:05+00:00 | 3 | 998 | 2 | 0 | 13 | 0 | 0 | after v0.1.13 owner issues updated and doctor docs issue closed: https://github.com/aaronlab/browsertrace/issues/23; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T17:33:48+00:00 | 3 | 998 | 2 | 0 | 13 | 0 | 0 | after launch discussion updated to v0.1.13 and #25 contribution path: https://github.com/aaronlab/browsertrace/discussions/6; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T17:35:42+00:00 | 3 | 998 | 2 | 0 | 13 | 0 | 0 | after profile draft moved to v0.1.13 and open contribution issue #25; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T17:37:22+00:00 | 3 | 998 | 2 | 0 | 13 | 0 | 2 | after owner-action issue bodies synced to v0.1.13: #5 #9; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T17:39:47+00:00 | 3 | 998 | 2 | 0 | 13 | 0 | 2 | after open issue bodies synced from v0.1.12 to v0.1.13: #3 #10 #18 #25; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T17:44:25+00:00 | 3 | 998 | 2 | 0 | 13 | 0 | 2 | after README public-safe export sharing example added for issue #25; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T17:46:31+00:00 | 3 | 998 | 2 | 0 | 12 | 0 | 2 | after issue #25 closed and profile/discussion feedback links moved to #3; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T17:50:58+00:00 | 3 | 998 | 2 | 0 | 13 | 0 | 2 | after good-first issue #26 opened and launch docs/discussion linked it; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T17:53:26+00:00 | 3 | 998 | 2 | 0 | 13 | 0 | 2 | after live profile and profile draft linked good-first issue #26; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T17:58:02+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 2 | after IndexNow key published and Bing IndexNow submission returned 202: https://github.com/aaronlab/browsertrace/issues/16#issuecomment-4413214819; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T17:59:59+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 2 | after generic IndexNow API submission returned 200: https://github.com/aaronlab/browsertrace/issues/16; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T18:07:09+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 2 | after PR #27 merged, issue #26 closed, and good-first issue #28 opened; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T18:09:15+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 2 | after launch discussion contributor update: https://github.com/aaronlab/browsertrace/discussions/6#discussioncomment-16864016; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T18:12:55+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 2 | after PR template contributor onboarding update; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T18:16:10+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 2 | after security policy private-reporting path update; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T18:18:45+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 2 | after Browser Use troubleshooting guide update for issue #11; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T18:21:16+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 2 | after Browser Use callback compatibility docs for issue #11; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T18:24:18+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 2 | after Browser Use model input context update for issue #11; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T18:26:58+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 2 | after Stagehand result capture update for issue #8; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T18:33:35+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 2 | after v0.1.14 release, profile sync, issue sync, and discussion update: https://github.com/aaronlab/browsertrace/releases/tag/v0.1.14; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T18:36:14+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 2 | after Skyvern nested run metadata extraction update; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T18:41:40+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 0 | after Playwright LLM no-network example for issue #12; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T18:45:36+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 0 | after Windows public-safe export docs for issue #28; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T18:48:27+00:00 | 3 | 998 | 3 | 0 | 14 | 0 | 0 | after good-first issue #29 rotation and live profile sync; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T18:49:48+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 0 | after issue #28 closed and good-first issue #29 kept open; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T18:51:35+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 0 | after IndexNow refresh for updated docs and issue #16 comment; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T18:55:17+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 0 | after launch discussion update for #29 and Playwright LLM example; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T18:58:29+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 0 | after pytest isolated trace storage docs for issue #29; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T19:01:01+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 0 | after issue #29 closed and good-first issue #30 rotation; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T19:03:54+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 0 | after GitHub Actions public-safe export artifact docs for issue #30; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T19:05:58+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 0 | after issue #30 closed and good-first issue #31 rotation; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T19:08:22+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 0 | after Playwright sync snapshot docs for issue #31; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T19:10:25+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 0 | after issue #31 closed and good-first issue #32 rotation; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T19:12:56+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 0 | after GitLab CI public-safe export artifact docs for issue #32; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T19:15:09+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 0 | after issue #32 closed and good-first issue #33 rotation; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T19:18:45+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 0 | after export run id prefix troubleshooting and ambiguity fix for issue #33; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T19:21:01+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 0 | after issue #33 closed and good-first issue #34 rotation; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T19:24:33+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 0 | after browsertrace show failed-run docs for issue #34; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T19:27:57+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 0 | after issue #34 closed and good-first issue #35 rotation; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T19:31:02+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 0 | after browsertrace list limit docs for issue #35; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T19:32:46+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 0 | after issue #35 closed and good-first issue #36 rotation; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T19:36:01+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 0 | after browsertrace doctor output docs for issue #36; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T19:37:23+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 0 | after issue #36 closed and good-first issue #37 rotation; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T19:39:49+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 0 | after CLI help docs for issue #37; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T19:41:15+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 0 | after issue #37 closed and good-first issue #38 rotation; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T19:44:13+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 0 | after environment variable quick reference docs for issue #38; traffic views 52/29 unique, clones 103/54 unique |
| 2026-05-09T19:46:05+00:00 | 3 | 998 | 3 | 0 | 13 | 0 | 0 | after issue #38 closed and good-first issue #39 rotation; traffic views 52/29 unique, clones 103/54 unique |
