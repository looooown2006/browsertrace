"""Tests for the CLI (browsertrace list / show / export)."""

from __future__ import annotations

import py_compile
import sqlite3
from pathlib import Path
from io import StringIO
from contextlib import redirect_stdout

import pytest

from browsertrace import Tracer


@pytest.fixture
def cli(tmp_path, monkeypatch):
    """Reload the CLI module bound to an isolated BROWSERTRACE_HOME."""
    monkeypatch.setenv("BROWSERTRACE_HOME", str(tmp_path))
    import importlib
    import browsertrace.cli as cli_mod
    importlib.reload(cli_mod)
    return cli_mod, tmp_path


def _seed(tmp_path, name, fail=False):
    tracer = Tracer(home=tmp_path)
    if fail:
        try:
            with tracer.run(name) as run:
                run.step(action="step 0", url="https://example.com")
                run.step(action="step 1", url="https://example.com/x")
                raise RuntimeError("intentional")
        except RuntimeError:
            pass
    else:
        with tracer.run(name) as run:
            run.step(action="step 0")
    return run.id


def test_cli_module_compiles_on_python311():
    """Guard against Python 3.11 f-string syntax regressions.

    The package supports Python 3.11, so CLI source must parse on 3.11 before
    any import-time tests can run.
    """
    root = Path(__file__).resolve().parents[1]
    py_compile.compile(str(root / "browsertrace" / "cli.py"), doraise=True)


def test_cli_list_prints_recent_runs(cli):
    cli_mod, tmp_path = cli
    _seed(tmp_path, "first")
    _seed(tmp_path, "second")
    buf = StringIO()
    with redirect_stdout(buf):
        rc = cli_mod.main(["list"])
    out = buf.getvalue()
    assert rc == 0
    assert "first" in out
    assert "second" in out


def test_cli_show_prints_steps_and_url(cli):
    cli_mod, tmp_path = cli
    rid = _seed(tmp_path, "showme", fail=True)
    buf = StringIO()
    with redirect_stdout(buf):
        rc = cli_mod.main(["show", rid[:8]])  # short prefix should also work
    out = buf.getvalue()
    assert rc == 0
    assert "showme" in out
    assert "step 0" in out
    assert "https://example.com" in out


def test_cli_show_unknown_run_id_returns_2(cli):
    cli_mod, _ = cli
    # Need a real DB file or _open() will exit 1, so seed an empty one.
    Tracer(home=cli[1])
    rc = cli_mod.main(["show", "nonexistent-id"])
    assert rc == 2


def test_cli_export_writes_html_with_inlined_screenshots(cli, tmp_path):
    cli_mod, home = cli
    tracer = Tracer(home=home)
    png = b"\x89PNG\r\n\x1a\n" + b"\x00" * 16
    with tracer.run("export-me") as run:
        run.step(action="snap", screenshot=png)

    out_file = tmp_path / "out.html"
    rc = cli_mod.main(["export", run.id, "-o", str(out_file)])
    assert rc == 0
    body = out_file.read_text()
    assert "export-me" in body
    assert "data:image/png;base64" in body  # screenshot inlined


def test_cli_export_writes_model_input_and_output(cli, tmp_path):
    cli_mod, home = cli
    tracer = Tracer(home=home)
    with tracer.run("model-io") as run:
        run.step(
            action="choose button",
            model_input={"prompt": "Which checkout button should I click?"},
            model_output={"selector": "button.checkout.primary"},
        )

    out_file = tmp_path / "model-io.html"
    rc = cli_mod.main(["export", run.id, "-o", str(out_file)])

    assert rc == 0
    body = out_file.read_text()
    assert "Model input" in body
    assert "Which checkout button should I click?" in body
    assert "Model output" in body
    assert "button.checkout.primary" in body


def test_cli_export_redact_hides_model_io(cli, tmp_path):
    cli_mod, home = cli
    tracer = Tracer(home=home)
    with tracer.run("sensitive-export") as run:
        run.step(
            action="ask model",
            model_input={"prompt": "private checkout token sk-browsertrace-test"},
            model_output={"selector": "#pay-now", "reason": "private model answer"},
        )

    out_file = tmp_path / "redacted.html"
    rc = cli_mod.main(["export", run.id, "--redact", "-o", str(out_file)])

    assert rc == 0
    body = out_file.read_text()
    assert "private checkout token" not in body
    assert "private model answer" not in body
    assert "Model I/O redacted" in body


def test_cli_export_redact_screenshots_omits_inlined_images(cli, tmp_path):
    cli_mod, home = cli
    tracer = Tracer(home=home)
    png = b"\x89PNG\r\n\x1a\n" + b"\x00" * 16
    with tracer.run("screenshot-redaction") as run:
        run.step(action="visible private page", screenshot=png)

    out_file = tmp_path / "redacted-screenshots.html"
    rc = cli_mod.main(["export", run.id, "--redact-screenshots", "-o", str(out_file)])

    assert rc == 0
    body = out_file.read_text()
    assert "data:image/png;base64" not in body
    assert "Screenshot redacted" in body


def test_cli_demo_creates_failed_demo_run(cli):
    cli_mod, home = cli
    buf = StringIO()

    with redirect_stdout(buf):
        rc = cli_mod.main(["demo"])

    assert rc == 0
    out = buf.getvalue()
    assert "demo: checkout agent fails on disabled button" in out
    assert "browsertrace" in out

    with sqlite3.connect(home / "db.sqlite") as conn:
        run = conn.execute(
            "SELECT id, status, error FROM runs WHERE name=?",
            ("demo: checkout agent fails on disabled button",),
        ).fetchone()
        assert run is not None
        assert run[1] == "failed"
        assert "button was disabled" in run[2]
        steps = conn.execute(
            "SELECT COUNT(*) FROM steps WHERE run_id=?",
            (run[0],),
        ).fetchone()[0]
    assert steps == 4


def test_cli_no_args_routes_to_serve(cli, monkeypatch):
    """`browsertrace` with no args should call serve."""
    cli_mod, _ = cli

    called = {"v": False}
    def fake_serve():
        called["v"] = True
    monkeypatch.setattr("browsertrace.server.main", fake_serve)
    cli_mod.main([])
    assert called["v"]
