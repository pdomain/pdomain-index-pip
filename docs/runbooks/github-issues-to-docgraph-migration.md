---
kind: runbook
status: retired
owner: CT
created: 2026-07-19
last_verified: 2026-11-13
---

# GitHub issues to docgraph migration — pdomain-index-pip

## Agent Index

- **Kind:** runbook
- **Status:** retired
- **Last verified:** 2026-11-13
- **Read when:** tracing the completed tracker migration through historical references.
- **Search terms:** issue migration, retired runbook, cutover, tombstone.

This procedure was retired on 2026-11-13. Its durable outcome is now in
[documentation governance](../architecture/documentation-governance.md).
This tombstone preserves links from the append-only deletion journal and
other historical evidence.

## Trigger

There is no pending cutover. The 21-issue migration completed on 2026-07-19;
commit `e3d1b98` records that outcome.

## Preconditions

Current issue work remains in the [roadmap](../roadmap.md) and governed issue
records. Migration completion does not resolve their owner decisions.

## Steps

The obsolete execution steps have been removed. Recover the original
procedure with
`git show bb3983a:docs/runbooks/github-issues-to-docgraph-migration.md`.
Do not rerun its deletion batches.

## Verification

The [migration ledger](../context/github-issue-migration-ledger.md) and
[deletion journal](../context/github-issue-deletion-journal.md) retain
destinations, node IDs, digests, and recorded absence checks. Those are
historical results, not newly repeated GitHub API checks.

## Rollback

GitHub issue deletion is irreversible. Governed destinations and Git history
retain the surviving evidence; this tombstone does not restore external
tickets.
