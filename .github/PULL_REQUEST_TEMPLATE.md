Replace every placeholder before requesting review. Keep the PR small enough to
review in one pass.

For the first contribution flow, use
`CONTRIBUTING.md#first-pr-recipe`; it keeps the first contribution small and reviewable.
Please also follow `CODE_OF_CONDUCT.md` in PR discussions and reviews.

## Summary

- What changed:
- Why it matters:

## Linked Issue

- Fixes #123 or Refs #123
- If there is no linked issue, say why this PR is still focused.

## Test Plan

- [ ] I ran `uv run --python 3.11 --extra dev pytest -q`
- [ ] I included the exact error/output if a check could not be run.

Optional for PRs that touch issue reports, CI, or AI/coding-agent troubleshooting:

```bash
browsertrace doctor --json
browsertrace list --status failed --json
browsertrace show <run_id> --json
```

## Demo / Screenshots

If this changes UI, examples, exports, or README launch flow, attach a
screenshot, GIF, or exported trace.
