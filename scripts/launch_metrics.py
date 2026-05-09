"""Collect BrowserTrace launch metrics from GitHub.

The active launch goal is real GitHub adoption, so this script keeps the
numbers auditable after every public post.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

REPO = "aaronlab/browsertrace"
RELEASE_TAG = "v0.1.7"
TARGET_STARS = 1001
DEFAULT_LOG = Path("docs/launch/metrics-log.md")

GitHubRunner = Callable[[list[str]], dict[str, Any]]


@dataclass(frozen=True)
class LaunchSnapshot:
    captured_at: str
    repo: str
    url: str
    stars: int
    forks: int
    watchers: int
    issues: int
    pull_requests: int
    release_tag: str
    release_downloads: int
    release_assets: int
    stars_to_goal: int
    goal_status: str
    note: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def gh_json(args: list[str]) -> dict[str, Any]:
    completed = subprocess.run(
        ["gh", *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def collect_snapshot(
    repo: str = REPO,
    release_tag: str = RELEASE_TAG,
    note: str = "",
    runner: GitHubRunner = gh_json,
    now: datetime | None = None,
) -> LaunchSnapshot:
    repo_payload = runner(
        [
            "repo",
            "view",
            repo,
            "--json",
            "stargazerCount,forkCount,watchers,issues,pullRequests,url",
        ]
    )
    release_payload = runner(["api", f"repos/{repo}/releases/tags/{release_tag}"])

    stars = int(repo_payload["stargazerCount"])
    assets = release_payload.get("assets") or []
    captured_at = (now or datetime.now(timezone.utc)).replace(microsecond=0).isoformat()

    return LaunchSnapshot(
        captured_at=captured_at,
        repo=repo,
        url=str(repo_payload["url"]),
        stars=stars,
        forks=int(repo_payload["forkCount"]),
        watchers=int(repo_payload["watchers"]["totalCount"]),
        issues=int(repo_payload["issues"]["totalCount"]),
        pull_requests=int(repo_payload["pullRequests"]["totalCount"]),
        release_tag=release_tag,
        release_downloads=sum(int(asset.get("download_count", 0)) for asset in assets),
        release_assets=len(assets),
        stars_to_goal=max(0, TARGET_STARS - stars),
        goal_status="complete" if stars >= TARGET_STARS else "incomplete",
        note=note,
    )


def render_summary(snapshot: LaunchSnapshot) -> str:
    data = snapshot.to_dict()
    return "\n".join(
        [
            f"repo: {data['repo']}",
            f"captured_at: {data['captured_at']}",
            f"stars: {data['stars']}",
            f"stars_to_goal: {data['stars_to_goal']}",
            f"forks: {data['forks']}",
            f"watchers: {data['watchers']}",
            f"issues: {data['issues']}",
            f"pull_requests: {data['pull_requests']}",
            f"release_downloads: {data['release_downloads']}",
            f"goal_status: {data['goal_status']}",
            f"note: {data['note']}",
        ]
    )


def markdown_row(snapshot: LaunchSnapshot) -> str:
    note = snapshot.note.replace("|", "\\|")
    return (
        f"| {snapshot.captured_at} | {snapshot.stars} | {snapshot.stars_to_goal} | "
        f"{snapshot.forks} | {snapshot.watchers} | {snapshot.issues} | "
        f"{snapshot.pull_requests} | {snapshot.release_downloads} | {note} |"
    )


def ensure_metrics_log(path: Path) -> None:
    if path.exists():
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                "# BrowserTrace Metrics Log",
                "",
                "Append one row after each meaningful public post or product update.",
                "The launch goal remains incomplete until GitHub reports at least 1001 stars.",
                "",
                "| Captured at | Stars | To 1001 | Forks | Watchers | Issues | PRs | Release downloads | Note |",
                "|---|---:|---:|---:|---:|---:|---:|---:|---|",
            ]
        )
        + "\n"
    )


def append_snapshot(path: Path, snapshot: LaunchSnapshot) -> None:
    ensure_metrics_log(path)
    with path.open("a") as file:
        file.write(markdown_row(snapshot) + "\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=REPO)
    parser.add_argument("--release-tag", default=RELEASE_TAG)
    parser.add_argument("--note", default="")
    parser.add_argument(
        "--append",
        nargs="?",
        const=str(DEFAULT_LOG),
        default=None,
        help="append a markdown row, defaulting to docs/launch/metrics-log.md",
    )
    parser.add_argument("--json", action="store_true", help="print raw JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    snapshot = collect_snapshot(
        repo=args.repo,
        release_tag=args.release_tag,
        note=args.note,
    )

    if args.append:
        append_snapshot(Path(args.append), snapshot)

    if args.json:
        print(json.dumps(snapshot.to_dict(), indent=2))
    else:
        print(render_summary(snapshot))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
