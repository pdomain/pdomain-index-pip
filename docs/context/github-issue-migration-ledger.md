---
Status: active
Owner: CT
Created: 2026-07-19
Last verified: 2026-07-19
Kind: reference
Level: I1
---

# GitHub issue migration ledger

## Agent Index

- **Kind:** reference
- **Status:** active
- **Level:** I1
- **Last verified:** 2026-07-19
- **Read when:** tracing where a former GitHub issue went, or auditing the
  issue-tracker cutover.
- **Search terms:** migration ledger, GitHub issues, provenance, raw digest,
  deletion status, issue cutover.

## What this records

**This ledger accounts for all 21 GitHub issues that existed on
`pdomain/pdomain-index-pip` before the tracker cutover.** Every issue appears
exactly once. The count matches GitHub's 20 open plus 1 closed at export time on
2026-07-19.

Raw exports were taken with `gh issue view --json` and digested with SHA-256.
They live outside the governed docs tree and are not committed. Re-export and
re-digest before acting on any row.

None of the 21 issues carried comments, so no comment text was lost in
migration.

## Verification changed five classifications

Five issues were labelled `status:backlog` but are already implemented. Each was
verified against current source on 2026-07-19 rather than inferred from issue
state. Issue #21 was checked the same way and is genuinely still open.

## Ledger

| # | Title | State | Outcome | Destination | Evidence | Deleted |
| --- | --- | --- | --- | --- | --- | --- |
| 1–15 | Rename sweep cluster | OPEN | Needs owner decision | [gh-001-015 record](../issues/2026-07-19-gh-001-015-rename-sweep.md) | Plan and spec files absent from `/workspaces`; superseded by the `pdomain-*` rename | No |
| 16 | Document dependency-confusion-safe pip and uv index usage | OPEN | Implemented | [architecture](../architecture/python-release-asset-index.md) Consumer resolution boundary | `README.md:49-63` — `explicit = true`, `tool.uv.sources` per package, warns against unrestricted `--extra-index-url` | No |
| 17 | Fail regen when release asset fetches fail unexpectedly | OPEN | Implemented | [architecture](../architecture/python-release-asset-index.md) Trust boundary | `scripts/regen_index.py:84-86,121-124` — matches repo-not-found narrowly, re-raises otherwise | No |
| 18 | Update README to canonical pd-index-pip Pages URL | OPEN | Implemented | `README.md` | `README.md:30` — `https://pdomain.github.io/pdomain-index-pip/simple/` | No |
| 19 | Add sha256 fragments to simple-index distribution links | CLOSED (COMPLETED) | Implemented | [architecture](../architecture/python-release-asset-index.md) Integrity metadata | `scripts/regen_index.py:221-223` — appends `#sha256=` when GitHub supplies a digest | No |
| 20 | Add tests for simple-index generator behavior | OPEN | Implemented | [architecture](../architecture/python-release-asset-index.md) Evidence | `tests/` — 3 files, 26 tests passing | No |
| 21 | Resolve gh executable before subprocess invocation | OPEN | Still open | [gh-021 record](../issues/2026-07-19-gh-021-resolve-gh-executable.md) | `scripts/regen_index.py:82` still calls `subprocess.run(["gh", *args])` | No |

## Node IDs and digests

Issues #1–#15 have their node IDs and digests recorded in the
[rename sweep record](../issues/2026-07-19-gh-001-015-rename-sweep.md). The
remaining six:

| # | Node ID | Raw digest (SHA-256) |
| --- | --- | --- |
| 16 | `I_kwDOSWRi3c8AAAABDJFSeQ` | `a3aa493d665be5696644025922350b000cba33f50d988381c416649a78ffc4fd` |
| 17 | `I_kwDOSWRi3c8AAAABDJFStQ` | `f1c0fe6964b6ef9e60cd8541d7480bc7ad5c12c5bca3b45767e70a1d3257fe8b` |
| 18 | `I_kwDOSWRi3c8AAAABDJFS5Q` | `1980705ce9748e771d6eaa3e8686fc80dd3abf7e86923b0d613a43fd7917097f` |
| 19 | `I_kwDOSWRi3c8AAAABDJFTFw` | `a22f958583a1d8716181309ac39efd5b12da93e85d70723ae5d381e0954edccb` |
| 20 | `I_kwDOSWRi3c8AAAABDJFTRQ` | `d3f25550dde98c6d1b726ca28673f1d45aaca1b9c683e9fc8f691f18d19a6251` |
| 21 | `I_kwDOSWRi3c8AAAABDJFTgA` | `81420bbb78642fa6f4e7bb523a546d2a9ed2e5d2656c03c7c120b08ba3c2a3c4` |

Issues #16 through #21 were authored by ConcaveTrillion on 2026-05-22 and all
originate from the deep review and security scan report
`reports/security-review-2026-05-22/pd-index-pip.md`. None has a milestone.

## Deletion status

**No GitHub issue has been deleted.** The Deleted column above is `No` for every
row, and stays that way until the cutover gates in the
[migration runbook](../runbooks/github-issues-to-docgraph-migration.md) pass.

Two gates are still outstanding: organization-level issue deletion has not been
confirmed for the `pdomain` org, and this migration has not been pushed to the
remote default branch. Deletion is permanent and requires an explicit owner go.

When deletion proceeds, record each batch in an append-only deletion journal
alongside this ledger and update the Deleted column.

## Related

- [Migration runbook](../runbooks/github-issues-to-docgraph-migration.md)
- [Issues folder](../issues/README.md)
- [Intent map](intent-map.md)
- [Current state](current-state.md)
