"""Local web UI for viewing traces. Run via: `browsertrace` or `python -m browsertrace.server`."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from .tracer import DEFAULT_HOME

app = FastAPI(title="BrowserTrace", docs_url=None, redoc_url=None)
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


def _db() -> sqlite3.Connection:
    conn = sqlite3.connect(DEFAULT_HOME / "db.sqlite")
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
        runs.append(d)
    return runs


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
    steps = []
    for s in step_rows:
        d = dict(s)
        for k in ("model_input", "model_output", "metadata"):
            if d.get(k):
                try:
                    d[k] = json.loads(d[k])
                except (TypeError, ValueError):
                    pass
        steps.append(d)
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


@app.get("/screenshot/{run_id}/{step_index}")
def screenshot(run_id: str, step_index: int) -> FileResponse:
    path = DEFAULT_HOME / "screenshots" / run_id / f"{step_index:04d}.png"
    if not path.exists():
        raise HTTPException(404, "Screenshot not found")
    return FileResponse(path)


def main() -> None:
    import uvicorn

    print("BrowserTrace UI: http://127.0.0.1:3000")
    print(f"Storage:        {DEFAULT_HOME}")
    uvicorn.run(app, host="127.0.0.1", port=3000, log_level="warning")


if __name__ == "__main__":
    main()
