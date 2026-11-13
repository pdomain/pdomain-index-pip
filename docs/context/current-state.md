<!--
Status: active
Owner: CT
Created: 2026-07-14
Last verified: 2026-11-13
Kind: context
-->

# Current state

## Agent Index

- **Status:** active
- **Owner:** CT
- **Created:** 2026-07-14
- **Last verified:** 2026-11-13
- **Kind:** context
- **Read when:** starting repository work or checking current operational truth.
- **Search terms:** current state, index generator, CI, release workflow, risks.

## What matters now

The repository generates a static PEP 503 index from allowlisted GitHub Release
assets.

The current trust boundary, allowlist, digest behavior, consumer
configuration, publication flow, and tooling-release path are in the
[release-asset index architecture](../architecture/python-release-asset-index.md).

`just ci` is the local verification gate. It installs locked dependencies,
runs pre-commit, Ruff, basedpyright, actionlint, ShellCheck, Markdown
formatting checks, and pytest, regenerates the index, and runs strict
docgraph checks. Release preflight uses this gate and regenerates the local
index; it does not publish that output.

`gh_json()` resolves `gh` to an absolute path before it starts a subprocess. It
raises a named error when `gh` is not on `PATH`. The
[architecture](../architecture/python-release-asset-index.md#github-cli-invocation)
records the limit of that check.

## In-flight work

Open work is the [roadmap](../roadmap.md). That list is the only copy. The
intent map classifies the same items and points at it.

GitHub Issues is disabled, so `docs/issues/` is the issue tracker. The
[documentation governance architecture](../architecture/documentation-governance.md)
records the completed tracker cutover and its retained audit evidence.

The [migration ledger](github-issue-migration-ledger.md) maps all 21 former
GitHub issues to their governed destinations. The
[deletion journal](github-issue-deletion-journal.md) records their deletion
and verification on 2026-07-19.

## Risks and test health

No red or flaky tests are documented.

Asset enumeration depends on the GitHub API. Regeneration fails closed when an
allowlisted repository or release cannot be read.

See the architecture evidence for the implementation and tests.
