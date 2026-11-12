---
Status: active
Owner: CT
Created: 2026-07-15
Last verified: 2026-11-12
Kind: process
Level: I1
---

# Issues

## Agent Index

- **Kind:** process
- **Status:** active
- **Level:** I1
- **Last verified:** 2026-11-12
- **Read when:** filing an issue or checking active and migrated issue records.
- **Search terms:** issues folder, issue report, migration, issue lifecycle.

## Purpose

`docs/issues/` holds governed issue reports that need a durable, citable record.
Each report is a docgraph node, so repository intent does not depend on an
external issue tracker.

## Convention

- Store reports in `docs/issues/`.
- Name migrated GitHub records `YYYY-MM-DD-gh-NNN-short-slug.md`.
- Keep frontmatter and Agent Index lifecycle fields consistent.
- Use `Status: active` for unresolved work.
- On resolution, route through `doc-retirer`. Promote anything durable into the
  doc that owns it. Delete the report. Write a tombstone to
  `docs/context/decisions.md`. Git history keeps the report.
- Link each record from governed context.
- Stage each record before reindexing and running the strict docgraph check.
- Copy `docs/issues/TEMPLATE.md` when creating a report. The template is
  excluded from the index. It must not be linked as a governed node.

## Open issues

The [roadmap](../roadmap.md) is the remaining-work list. These issue files are
still open:

- [The rename cluster still needs a disposition](2026-07-19-gh-001-015-rename-sweep.md).
- [Dep-refresh branch accumulation](2026-08-08-dep-refresh-cannot-auto-land.md).

## Where shipped work is recorded

Shipped index behavior is the
[release-asset index architecture](../architecture/python-release-asset-index.md).

The [migration ledger](../context/github-issue-migration-ledger.md) maps former
GitHub issues to their destinations. The
[deletion journal](../context/github-issue-deletion-journal.md) records their
deletion and verification.
