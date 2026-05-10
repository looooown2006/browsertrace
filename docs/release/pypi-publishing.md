# PyPI Trusted Publishing

BrowserTrace should use PyPI Trusted Publishing instead of long-lived API
tokens. The GitHub workflow is `.github/workflows/publish.yml`.

## Current Status

As of 2026-05-09:

- PyPI still returns `404` for `https://pypi.org/pypi/browsertrace/json`, so
  the package is not published yet.
- GitHub release `v0.1.15` has the wheel and sdist ready.
- The GitHub repository has a `pypi` environment.
- The `Publish` workflow exists and has not been run yet.
- The `publish` job has `contents: read` and `id-token: write`, so it can
  download the built artifact and request the PyPI Trusted Publisher token.

## Owner Setup

Configure a PyPI trusted publisher with these values:

| Field | Value |
|---|---|
| PyPI project | `browsertrace` |
| GitHub owner | `aaronlab` |
| GitHub repository | `browsertrace` |
| Workflow filename | `publish.yml` |
| Environment name | `pypi` |

If PyPI requires a project to exist first, create the project through PyPI's
pending publisher flow for the same values above.

## GitHub Setup

The repository has a `pypi` environment. Review it in GitHub repository
settings before the first publish:

1. Open `Settings -> Environments`.
2. Open `pypi`.
3. Add a required reviewer if you want manual approval before publishing.

## Publish

After PyPI trusted publishing is configured:

```bash
gh workflow run Publish --repo aaronlab/browsertrace
```

The workflow is manual on purpose. GitHub releases should not attempt PyPI
publishing until the trusted publisher is configured by the owner. The workflow
builds the wheel and sdist, then publishes with OpenID Connect.

## Verify

```bash
python -m pip index versions browsertrace
pipx run --spec "browsertrace[ui]" browsertrace --help
```

After verification, update README install commands from GitHub URLs to:

```bash
pip install browsertrace
pip install "browsertrace[ui]"
```

## Small Docs Fixes

PyPI trusted publishing setup is owner-only. For small docs fixes around release
or packaging notes, use the
[First PR Recipe](https://github.com/aaronlab/browsertrace/blob/main/CONTRIBUTING.md#first-pr-recipe)
to keep the first contribution small and reviewable.
