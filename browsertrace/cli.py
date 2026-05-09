"""BrowserTrace CLI: list, show, export, serve.

Usage:
    browsertrace                 # start the web UI (default)
    browsertrace demo            # create a deterministic failed demo run
    browsertrace list            # list runs in the terminal
    browsertrace show <run_id>   # print a run's timeline
    browsertrace export <id>     # write a portable HTML bundle to ./<id>.html
    browsertrace export <id> --redact  # omit model I/O from the HTML export
    browsertrace serve           # explicit alias of `browsertrace`
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path
from typing import Optional

from .tracer import DEFAULT_HOME


def _home() -> Path:
    import os
    override = os.environ.get("BROWSERTRACE_HOME")
    return Path(override).expanduser() if override else DEFAULT_HOME


def _db_path() -> Path:
    return _home() / "db.sqlite"


def _open() -> sqlite3.Connection:
    p = _db_path()
    if not p.exists():
        print(f"No traces yet at {_home()}.", file=sys.stderr)
        print("Record one first, then run this command again.", file=sys.stderr)
        sys.exit(1)
    conn = sqlite3.connect(p)
    conn.row_factory = sqlite3.Row
    return conn


def _fmt_status(s: str) -> str:
    return {"completed": "✓ ok", "failed": "✗ fail", "running": "… running"}.get(s, s)


def cmd_list(args) -> int:
    with _open() as c:
        rows = c.execute(
            "SELECT id, name, status, started_at, ended_at FROM runs "
            "ORDER BY started_at DESC LIMIT ?",
            (args.limit,),
        ).fetchall()
    if not rows:
        print("No runs yet.")
        return 0
    for r in rows:
        dur = f"{r['ended_at'] - r['started_at']:.1f}s" if r["ended_at"] else "running"
        print(f"{r['id'][:8]}  {_fmt_status(r['status']):11}  {dur:>8}  {r['name'] or ''}")
    return 0


def cmd_demo(_args) -> int:
    from .demo import DEMO_NAME, create_demo_run

    run_id = create_demo_run(home=_home())
    print(f"Created demo run: {DEMO_NAME}")
    print(f"Run ID: {run_id}")
    print("Run `browsertrace` and open http://127.0.0.1:3000")
    return 0


def cmd_show(args) -> int:
    with _open() as c:
        # Allow short prefix as well as full id.
        run = c.execute(
            "SELECT * FROM runs WHERE id=? OR id LIKE ? LIMIT 1",
            (args.run_id, f"{args.run_id}%"),
        ).fetchone()
        if not run:
            print(f"No run matching {args.run_id!r}.", file=sys.stderr)
            return 2
        steps = c.execute(
            "SELECT * FROM steps WHERE run_id=? ORDER BY step_index", (run["id"],)
        ).fetchall()

    print(f"Run:    {run['id']}")
    print(f"Name:   {run['name'] or '(unnamed)'}")
    print(f"Status: {_fmt_status(run['status'])}")
    if run["error"]:
        print(f"Error:  {run['error']}")
    print(f"Steps:  {len(steps)}")
    print()
    for s in steps:
        status = (s["status"] or "ok")
        marker = "✓" if status == "ok" else "✗"
        print(f"  [{s['step_index']:>2}] {marker} {status:8} {s['action'] or '(no action)'}")
        if s["url"]:
            print(f"        url: {s['url']}")
        if s["error"]:
            print(f"        error: {s['error']}")
    return 0


def cmd_export(args) -> int:
    """Write a self-contained HTML bundle for a run (screenshots inline as base64)."""
    import base64
    with _open() as c:
        run = c.execute(
            "SELECT * FROM runs WHERE id=? OR id LIKE ? LIMIT 1",
            (args.run_id, f"{args.run_id}%"),
        ).fetchone()
        if not run:
            print(f"No run matching {args.run_id!r}.", file=sys.stderr)
            return 2
        steps = c.execute(
            "SELECT * FROM steps WHERE run_id=? ORDER BY step_index", (run["id"],)
        ).fetchall()

    out_path = Path(args.out) if args.out else Path(f"{run['id']}.html")
    parts = [
        "<!doctype html><html><head><meta charset='utf-8'>",
        f"<title>BrowserTrace export · {run['name'] or run['id']}</title>",
        "<style>",
        "body{font:14px/1.5 -apple-system,system-ui,sans-serif;color:#1a1a1a;background:#fafafa;margin:0;padding:24px;max-width:1100px;margin:auto}",
        "h1{font-size:20px;margin:0 0 12px}",
        ".meta{color:#6b7280;font-size:13px;margin-bottom:24px}",
        ".step{background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:16px;margin-bottom:12px;display:grid;grid-template-columns:240px 1fr;gap:16px}",
        ".step.error{border-color:#fca5a5;box-shadow:0 0 0 3px rgba(220,38,38,.08)}",
        ".step img{max-width:100%;border-radius:4px}",
        "code{background:#f3f4f6;padding:1px 4px;border-radius:3px;font-size:12px}",
        "pre{background:#f3f4f6;padding:12px;border-radius:6px;font-size:12px;overflow:auto}",
        ".badge{display:inline-block;padding:2px 8px;border-radius:12px;font-size:11px;font-weight:600;text-transform:uppercase}",
        ".badge.ok{background:#d1fae5;color:#059669}.badge.error{background:#fee2e2;color:#dc2626}",
        "</style></head><body>",
        f"<h1>{_html_escape(run['name'] or run['id'])}</h1>",
        f"<div class=meta>id={run['id']} · status={run['status']} · {len(steps)} steps</div>",
    ]
    if run["error"]:
        parts.append(f"<pre style='background:#fee2e2;color:#dc2626'>{_html_escape(run['error'])}</pre>")

    no_screenshot_html = (
        '<div style="color:#6b7280;text-align:center;padding:48px">'
        "no screenshot"
        "</div>"
    )

    for s in steps:
        is_err = (s["status"] or "ok") != "ok"
        klass = "step error" if is_err else "step"
        badge = "error" if is_err else "ok"
        img_html = ""
        if s["screenshot_path"] and Path(s["screenshot_path"]).exists():
            data = base64.b64encode(Path(s["screenshot_path"]).read_bytes()).decode()
            img_html = f"<img src='data:image/png;base64,{data}' alt='step {s['step_index']}'>"
        parts.append(
            f"<div class='{klass}'>"
            f"<div>{img_html or no_screenshot_html}</div>"
            f"<div>"
            f"<div style='font-size:11px;color:#6b7280;font-weight:600'>STEP {s['step_index']}</div>"
            f"<div style='font-size:15px'>{_html_escape(s['action'] or '')} <span class='badge {badge}'>{s['status'] or 'ok'}</span></div>"
            f"<div style='font-size:12px;color:#6b7280'><code>{_html_escape(s['url'] or '')}</code></div>"
        )
        if s["error"]:
            parts.append(f"<pre style='background:#fee2e2;color:#dc2626'>{_html_escape(s['error'])}</pre>")
        if getattr(args, "redact", False) and (s["model_input"] or s["model_output"]):
            parts.append(
                "<details><summary>Model I/O redacted</summary>"
                "<pre>Prompt and model output omitted from this export.</pre></details>"
            )
        else:
            if s["model_input"]:
                parts.append(
                    "<details><summary>Model input</summary>"
                    f"<pre>{_html_escape(s['model_input'])}</pre></details>"
                )
            if s["model_output"]:
                parts.append(
                    "<details><summary>Model output</summary>"
                    f"<pre>{_html_escape(s['model_output'])}</pre></details>"
                )
        parts.append("</div></div>")
    parts.append("</body></html>")

    out_path.write_text("".join(parts), encoding="utf-8")
    print(f"Wrote {out_path}")
    return 0


def _html_escape(s) -> str:
    if not isinstance(s, str):
        s = str(s) if s is not None else ""
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def cmd_serve(_args) -> int:
    from .server import main as serve_main
    serve_main()
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="browsertrace", description="BrowserTrace CLI")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("serve", help="Start the local web UI (default)")

    p_demo = sub.add_parser("demo", help="Create a deterministic failed demo run")
    p_demo.set_defaults(func=cmd_demo)

    p_list = sub.add_parser("list", help="List recent runs")
    p_list.add_argument("--limit", type=int, default=20)
    p_list.set_defaults(func=cmd_list)

    p_show = sub.add_parser("show", help="Print a run's timeline")
    p_show.add_argument("run_id", help="Full id or unique prefix")
    p_show.set_defaults(func=cmd_show)

    p_export = sub.add_parser("export", help="Write a self-contained HTML bundle for a run")
    p_export.add_argument("run_id")
    p_export.add_argument("-o", "--out", help="Output path (default: <run_id>.html)")
    p_export.add_argument(
        "--redact",
        action="store_true",
        help="Omit model input/output from the exported HTML",
    )
    p_export.set_defaults(func=cmd_export)

    args = parser.parse_args(argv)

    if args.cmd is None or args.cmd == "serve":
        return cmd_serve(args)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
