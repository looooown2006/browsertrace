# BrowserTrace launch — 文案草稿

## English (X / Twitter)

### 草稿 1（功能向，简短）
```
Shipped BrowserTrace — a tiny OSS tool to debug AI browser agents.

Your agent fails in prod → you stare at logs → no idea why.

Drop in 1 decorator → it auto-records every step (screenshot, action,
model I/O, URL). Open localhost → see exactly where it broke.

Works with Browser Use, Playwright, anything.

github.com/aaronagent/browsertrace
[GIF]
```

### 草稿 2（场景向，故事感）
```
3 AM. My browser agent crashed mid-run.
1500 lines of logs. No screenshots. Cookies gone.
I have no idea what step 47 saw.

So I built BrowserTrace.

@trace your agent → record every step → open the timeline.
Find the bug in 30 seconds, not 30 minutes.

Free, OSS, runs locally.
github.com/aaronagent/browsertrace
[GIF]
```

### 草稿 3（kicker 短句版）
```
Your AI browser agent failed. Why?

Screenshots: gone. DOM: changed. Logs: useless.

BrowserTrace records every step the agent took.
Replay it like a debugger.

OSS, 1-line setup. github.com/aaronagent/browsertrace
[GIF]
```

**推荐先发草稿 2**：故事开场最容易拉到 AI dev 圈的注意。

---

## 中文（小红书 / 即刻 / 微信）

### 小红书笔记（标题党版本）
```
🪄 凌晨 3 点 debug AI agent 时，我手搓了个工具

做 browser agent 的人都懂这种痛：

跑了 5 分钟，挂了。
log 一堆乱七八糟，截图没存，浏览器关了。
你只能再跑一次试图复现 → 结果复现不了 → 抓瞎

所以我做了 BrowserTrace。

✅ 装一行代码
✅ 自动录每一步：截图、动作、AI 在想啥、URL
✅ 本地打开网页看时间线，1 分钟找到挂在哪一步

完全开源，本地跑，不上云。

GitHub：aaronagent/browsertrace
（首页星标更新中）

#AIagent #browseruse #开发者工具 #开源
```

### 即刻短动态
```
做了个开源小工具：BrowserTrace

如果你也在跑 browser agent（Browser Use / Stagehand / 自研），
agent 挂了不知道为什么的痛，应该懂。

装一行 Python decorator → 每步自动录截图 + action + LLM 输入输出 →
本地 web UI 1 分钟看清楚挂在哪。

github.com/aaronagent/browsertrace

求 star 求 issue 求骂🙏
```

---

## Hacker News（Show HN）

### 标题
```
Show HN: BrowserTrace – record and replay AI browser-agent runs to find bugs
```

### 正文
```
Hi HN,

I've been building browser-using AI agents (with Browser Use and direct
Playwright + LLM) and got tired of staring at log files trying to figure out
why a 5-minute run failed at step 47.

BrowserTrace is a small Python library + local web UI that records every
step of an agent run: screenshot, URL, the action the model decided on,
model input/output, and timing. Open localhost:3000, click into the run,
scrub through the timeline.

It's intentionally tiny:
- ~600 lines, no cloud, no auth, no signup
- pip install + 1 decorator
- SQLite + filesystem; data stays on your machine
- Works with anything (Browser Use, Playwright, computer use)

Adjacent tools either trace LLM calls and ignore the browser (Langfuse,
LangSmith), lock you into one runtime (Browserbase recordings), or are
broader generic observability stacks (Laminar). I wanted the smallest
useful thing for the specific "my browser agent failed, what happened"
loop, so I built it.

Repo: https://github.com/aaronagent/browsertrace

Roadmap: AI root-cause classification, public share links (Loom-style),
replay-from-step-N, regression-test generation. Happy to take feedback on
priorities.
```

---

## 微信 AI 群（钩子文案）

```
最近做了个小工具，给跑 browser agent 的同好用：

BrowserTrace —— agent 挂了，1 分钟找到挂在哪一步。
开源、本地、装一行代码。

github.com/aaronagent/browsertrace

求各位试试，bug 反馈直接私我或 issue。
```

---

## 配套素材清单

要发推之前必须先准备：

- [ ] **demo GIF**（关键）：录屏 30-60 秒，展示
  - 跑 `python examples/playwright_example.py`
  - 打开 `localhost:3000` 看 run 列表
  - 点进 timeline 看 3 个 step 的截图
  - **不要超过 60 秒，不要加音乐，不要花哨字幕**

- [ ] **README 第一屏**：要有一张 hero screenshot（timeline 视图）
- [ ] **GitHub repo 首页**：description、topics（`ai-agents`、`browser-automation`、`observability`、`debugging`、`llm`）、license、第一个 release tag (v0.1.0)

---

## 发布顺序建议

1. **Day 0（你）**：录 GIF、贴到 README、打 v0.1.0 tag、确认 repo public 之前所有 link 都对
2. **Day 1 早**：在微信 AI 群发钩子（warm audience，最容易拿到第一波反馈）
3. **Day 1 中**：发 X（草稿 2）+ 即刻
4. **Day 1 晚**：发小红书
5. **Day 2-3**（根据 Day 1 反馈）：发 Hacker News Show HN（HN 一次性机会，前 24 小时最关键，且周二早上美东时间发最好）
6. **Day 3-7**：在 Browser Use Discord、Stagehand Discord、AI agent Reddit 选一个去发，**不要广撒网**

**重要原则**：每个 channel 发完，等 24 小时看反馈再决定下一个 channel 怎么调整文案。不要一天全发。
