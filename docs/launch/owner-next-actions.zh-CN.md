# BrowserTrace Owner 下一步动作

这是给 `aaronlab/browsertrace` 发布用的最短中文执行清单。这里列的都是
需要你本人登录账号、2FA、发帖或提交的动作。

不要买 star、刷 star、互赞、求 upvote、求转发。对外只问一件事：正在做
browser agent 的人，失败时最缺什么调试信息？

## 10 分钟 Owner 解锁顺序

如果你只有一小段时间，按这个顺序做；后面的验证、README 更新、指标记录和
issue comment 都交给 Codex 继续处理：

1. 在 https://pypi.org/manage/account/publishing/ 配置 PyPI Trusted
   Publisher，字段完全照第 1 节填。
2. 打开 https://github.com/aaronlab/browsertrace/settings，在 General ->
   Social preview 上传 `docs/social-preview.png`。
3. 在 GitHub 个人主页点 Profile -> Customize your pins，置顶
   `aaronlab/browsertrace`。
4. 用 `docs/launch/day-1-publish-packet.md` 发 X、LinkedIn、微信群、即刻，
   主素材用 `docs/demo.mp4`。

第 1 步做完后告诉 Codex “PyPI 配好了”，我就可以运行发布 workflow，并把公开
安装命令从 GitHub tag 改成正常的 `pip install`。第 2-4 步做完后，把帖子 URL
或群名发给 Codex，我会记录指标并更新跟踪 issue。

## 1. 先解锁 PyPI

这是当前最大安装转化阻塞。完成后公开文案可以从 GitHub 安装 URL 改成：

```bash
pip install "browsertrace[ui]"
```

如果必须在 PyPI 配置前先发帖或回复，用已经验证过的 uvx 试用路径：

```bash
uvx --from "browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.14" browsertrace doctor
uvx --from "browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.14" browsertrace demo
uvx --from "browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.14" browsertrace list
uvx --from "browsertrace[ui] @ git+https://github.com/aaronlab/browsertrace@v0.1.14" browsertrace
```

在 PyPI 配置 Trusted Publisher：

| 字段 | 值 |
|---|---|
| PyPI project | `browsertrace` |
| GitHub owner | `aaronlab` |
| GitHub repository | `browsertrace` |
| Workflow filename | `publish.yml` |
| Environment name | `pypi` |

配置完后运行：

```bash
gh workflow run Publish --repo aaronlab/browsertrace
```

验证：

```bash
python -m pip index versions browsertrace
pipx run --spec "browsertrace[ui]" browsertrace --help
```

跟踪 issue: https://github.com/aaronlab/browsertrace/issues/5

## 2. 维护 GitHub 个人 Profile README

当前真正会渲染个人主页的 profile repo 是 `aaronlab/aaronlab`。旧 repo
`aaronlab/aaronagent` 只作为旧流量 redirect 使用。

正确的 repo 是：

```text
aaronlab/aaronlab
```

刷新 README 时使用这个源草稿：

```text
docs/launch/github-profile-readme.md
```

在 GitHub 个人主页置顶 BrowserTrace：

```text
Profile -> Customize your pins -> aaronlab/browsertrace
```

当前可用的 GitHub API 不暴露 profile pinning，所以这一步需要你在 GitHub UI
里手动做一次。

Profile pinning 跟踪 issue:
https://github.com/aaronlab/browsertrace/issues/24

跟踪 issue: https://github.com/aaronlab/browsertrace/issues/13

## 3. 上传 GitHub Social Preview

打开 GitHub 仓库设置：

```text
Settings -> General -> Social preview
```

上传：

```text
docs/social-preview.png
```

这样别人分享 repo 链接时会显示 BrowserTrace 卡片，而不是 GitHub 默认图。

跟踪 issue: https://github.com/aaronlab/browsertrace/issues/15

## 4. 提交搜索引擎收录

sitemap 和 robots 已经在线：

```text
https://aaronlab.github.io/browsertrace/sitemap.xml
https://aaronlab.github.io/browsertrace/robots.txt
```

按这个文件操作：

```text
docs/launch/search-indexing-submission.md
```

跟踪 issue: https://github.com/aaronlab/browsertrace/issues/16

## 5. 发 Day 1 warm launch

使用：

```text
docs/launch/day-1-publish-packet.md
docs/launch/channel-copy.md
```

推荐顺序：

1. X
2. LinkedIn
3. 一两个真正相关的微信 AI builder 群
4. 即刻

主素材用：

```text
docs/demo.mp4
```

备用图：

```text
docs/demo-poster.png
```

跟踪 issue: https://github.com/aaronlab/browsertrace/issues/9

## 6. 提交目录、newsletter、awesome lists

目录和 newsletter：

```text
docs/launch/directory-submission-sheet.md
docs/launch/outreach-targets.md
```

GitHub awesome lists：

```text
docs/launch/github-awesome-list-submissions.md
```

已经打开的 PR：

| 目标 | PR |
|---|---|
| `angrykoala/awesome-browser-automation` | `https://github.com/angrykoala/awesome-browser-automation/pull/112` |
| `mxschmitt/awesome-playwright` | `https://github.com/mxschmitt/awesome-playwright/pull/136` |
| `Jenqyang/Awesome-AI-Agents` | `https://github.com/Jenqyang/Awesome-AI-Agents/pull/220` |

现在只监控维护者反馈，不再追加提交新的 awesome-list PR。

目录/newsletter 跟踪 issue: https://github.com/aaronlab/browsertrace/issues/10

Awesome list 跟踪 issue: https://github.com/aaronlab/browsertrace/issues/18

## 回复小贡献问题

如果有人问怎么做一个小的文档贡献，先给当前 good first issue：

```text
https://github.com/aaronlab/browsertrace/issues/200
```

然后给 First PR Recipe：

```text
https://github.com/aaronlab/browsertrace/blob/main/CONTRIBUTING.md#first-pr-recipe keeps the first contribution small and reviewable.
```

## 回复本地首跑 / CI / agent 调试问题

遇到 local first-run issues, CI failures, or AI/coding-agent troubleshooting replies 时，先问对方补充 debugging/workflow details；如果可以安全分享，再让对方贴这组 JSON CLI diagnostics：

```bash
browsertrace doctor --json
browsertrace list --status failed --json
browsertrace show <run_id> --json
```

## 7. 每做完一个动作就记录指标

```bash
uv run --python 3.11 python scripts/launch_metrics.py --append --note "after <action>: <URL or note>"
uv run --python 3.11 python scripts/launch_metrics.py --json
```

目标只有一个：GitHub 实时显示超过 1000 stars 才算完成。

```bash
gh repo view aaronlab/browsertrace --json stargazerCount,url,homepageUrl,owner
```
