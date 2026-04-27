"""Local web UI for viewing traces. Run via: `browsertrace` or `python -m browsertrace.server`."""

from __future__ import annotations

import json
import os
import sqlite3
import time
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from .tracer import DEFAULT_HOME

app = FastAPI(title="BrowserTrace", docs_url=None, redoc_url=None)
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


def _home() -> Path:
    """Resolve storage home each call so env override / CLI flag work after import."""
    override = os.environ.get("BROWSERTRACE_HOME")
    return Path(override).expanduser() if override else DEFAULT_HOME


def _db() -> sqlite3.Connection:
    conn = sqlite3.connect(_home() / "db.sqlite", timeout=5.0)
    conn.row_factory = sqlite3.Row
    return conn


def _runs() -> list[dict[str, Any]]:
    with _db() as c:
        rows = c.execute(
            "SELECT id, name, status, started_at, ended_at, error FROM runs "
            "ORDER BY started_at DESC LIMIT 200"
        ).fetchall()
    runs = []
    for r in rows:
        d = dict(r)
        d["duration"] = (
            f"{d['ended_at'] - d['started_at']:.1f}s"
            if d["ended_at"]
            else "running..."
        )
        d["started_human"] = _format_started(d["started_at"])
        runs.append(d)
    return runs


def _format_started(epoch: float) -> str:
    import datetime as _dt
    delta = time.time() - epoch
    if delta < 60:
        return f"{int(delta)}s ago"
    if delta < 3600:
        return f"{int(delta // 60)}m ago"
    if delta < 86400:
        return f"{int(delta // 3600)}h ago"
    return _dt.datetime.fromtimestamp(epoch).strftime("%Y-%m-%d %H:%M")


def _run_detail(run_id: str) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    with _db() as c:
        run_row = c.execute("SELECT * FROM runs WHERE id=?", (run_id,)).fetchone()
        step_rows = c.execute(
            "SELECT * FROM steps WHERE run_id=? ORDER BY step_index", (run_id,)
        ).fetchall()
    if not run_row:
        return None, []
    run = dict(run_row)
    run["duration"] = (
        f"{run['ended_at'] - run['started_at']:.1f}s" if run["ended_at"] else "running..."
    )
    run["started_human"] = _format_started(run["started_at"])
    steps = []
    base_ts = run["started_at"]
    first_error_index = None
    for s in step_rows:
        d = dict(s)
        for k in ("model_input", "model_output", "metadata"):
            if d.get(k):
                try:
                    d[k] = json.loads(d[k])
                except (TypeError, ValueError):
                    pass
        offset = (d.get("timestamp") or base_ts) - base_ts
        d["offset"] = f"+{offset:.2f}s" if offset >= 0 else f"{offset:.2f}s"
        if first_error_index is None and d.get("status") == "error":
            first_error_index = d["step_index"]
        steps.append(d)
    run["first_error_index"] = first_error_index
    return run, steps


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "index.html", {"runs": _runs()})


@app.get("/run/{run_id}", response_class=HTMLResponse)
def run_view(request: Request, run_id: str) -> HTMLResponse:
    run, steps = _run_detail(run_id)
    if not run:
        raise HTTPException(404, "Run not found")
    return templates.TemplateResponse(request, "run.html", {"run": run, "steps": steps})


@app.get("/api/run/{run_id}")
def api_run(run_id: str) -> JSONResponse:
    """JSON export of a full run. Suitable for feeding back to an LLM for self-debug."""
    run, steps = _run_detail(run_id)
    if not run:
        raise HTTPException(404, "Run not found")
    # Strip heavy / non-LLM-useful fields and add screenshot URLs.
    payload_steps = [
        {
            "step_index": s["step_index"],
            "offset": s["offset"],
            "action": s.get("action") or "",
            "url": s.get("url") or "",
            "status": s.get("status") or "ok",
            "error": s.get("error"),
            "model_input": s.get("model_input"),
            "model_output": s.get("model_output"),
            "metadata": s.get("metadata"),
            "screenshot_url": (
                f"/screenshot/{run_id}/{s['step_index']}" if s.get("screenshot_path") else None
            ),
        }
        for s in steps
    ]
    return JSONResponse(
        {
            "run": {
                "id": run["id"],
                "name": run.get("name"),
                "status": run.get("status"),
                "duration": run.get("duration"),
                "started_at": run.get("started_at"),
                "ended_at": run.get("ended_at"),
                "error": run.get("error"),
                "first_error_index": run.get("first_error_index"),
            },
            "steps": payload_steps,
        }
    )


@app.get("/screenshot/{run_id}/{step_index}")
def screenshot(run_id: str, step_index: int) -> FileResponse:
    # Path-traversal guard: run_id must be a UUID-shaped string and step_index is int.
    if not run_id.replace("-", "").isalnum() or len(run_id) > 64:
        raise HTTPException(400, "Bad run id")
    base = (_home() / "screenshots").resolve()
    target = (base / run_id / f"{step_index:04d}.png").resolve()
    try:
        target.relative_to(base)
    except ValueError:
        raise HTTPException(400, "Bad path")
    if not target.exists():
        raise HTTPException(404, "Screenshot not found")
    return FileResponse(target)


def main() -> None:
    import uvicorn

    port = int(os.environ.get("BROWSERTRACE_PORT", "3000"))
    print(f"BrowserTrace UI: http://127.0.0.1:{port}")
    print(f"Storage:        {_home()}")
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")


if __name__ == "__main__":
    main()
