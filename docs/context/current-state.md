<!--
Status: active
Owner: CT
Created: 2026-07-14
Last verified: 2026-11-06
Kind: context
-->

# Current state

## Agent Index

- **Status:** active
- **Owner:** CT
- **Created:** 2026-07-14
- **Last verified:** 2026-11-06
- **Kind:** context
- **Read when:** starting repository work or checking current operational truth.
- **Search terms:** current state, index generator, CI, release workflow, risks.

## What matters now

The repository generates a static PEP 503 index from allowlisted GitHub Release
assets.

The current trust boundary, digest behavior, consumer configuration, and
publication flow are in the
[release-asset index architecture](../architecture/python-release-asset-index.md).

`make ci` is the local verification gate. It runs Ruff, basedpyright,
actionlint, ShellCheck, Markdown formatting checks, and pytest.

## In-flight work

Open work is the [roadmap](../roadmap.md).

GitHub Issues is disabled, so `docs/issues/` is the issue tracker.

The audit trail for the 2026-07-19 deletion of all 21 GitHub issues is the
[migration ledger](github-issue-migration-ledger.md) and the
[deletion journal](github-issue-deletion-journal.md).

## Risks and test health

No red or flaky tests are documented.

Asset enumeration depends on the GitHub API. Regeneration fails closed when an
allowlisted repository or release cannot be read.

See the architecture evidence for the implementation and tests.
