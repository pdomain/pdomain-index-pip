---
Status: active
Owner: CT
Created: 2026-07-19
Last verified: 2026-11-10
Kind: reference
Level: I1
---

# GitHub issue migration ledger

## Agent Index

- **Kind:** reference
- **Status:** active
- **Level:** I1
- **Last verified:** 2026-11-10
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
They lived outside the governed docs tree and were not committed. The issues
have since been deleted, so they cannot be re-exported. The
[deletion journal](github-issue-deletion-journal.md) preserves their digests.

None of the 21 issues carried comments, so no comment text was lost in
migration.

## Verification changed five classifications

Five issues were labelled `status:backlog` but are already implemented. Each was
verified against current source on 2026-07-19 rather than inferred from issue
state. Issue #21 was checked the same way and was genuinely still open then.
It was implemented on 2026-11-10.

## Ledger

| # | Title | State | Outcome | Destination | Evidence | Deleted |
| --- | --- | --- | --- | --- | --- | --- |
| 1–15 | Rename sweep cluster | OPEN | Needs owner decision | [gh-001-015 record](../issues/2026-07-19-gh-001-015-rename-sweep.md) | Plan and spec files absent from `/workspaces`; superseded by the `pdomain-*` rename | Yes |
| 16 | Document dependency-confusion-safe pip and uv index usage | OPEN | Implemented | [architecture](../architecture/python-release-asset-index.md) Consumer resolution boundary | `README.md:49-63` — `explicit = true`, `tool.uv.sources` per package, warns against unrestricted `--extra-index-url` | Yes |
| 17 | Fail regen when release asset fetches fail unexpectedly | OPEN | Implemented | [architecture](../architecture/python-release-asset-index.md) Trust boundary | `scripts/regen_index.py:89-91,126-129,156-159` — matches repo-not-found narrowly, re-raises otherwise | Yes |
| 18 | Update README to canonical pd-index-pip Pages URL | OPEN | Implemented | `README.md` | `README.md:30` — `https://pdomain.github.io/pdomain-index-pip/simple/` | Yes |
| 19 | Add sha256 fragments to simple-index distribution links | CLOSED (COMPLETED) | Implemented | [architecture](../architecture/python-release-asset-index.md) Integrity metadata | `scripts/regen_index.py:226-228` — appends `#sha256=` when GitHub supplies a digest | Yes |
| 20 | Add tests for simple-index generator behavior | OPEN | Implemented | [architecture](../architecture/python-release-asset-index.md) Evidence | `tests/test_regen_index.py` — 18 tests passing on 2026-11-07 | Yes |
| 21 | Resolve gh executable before subprocess invocation | OPEN | Implemented | [architecture](../architecture/python-release-asset-index.md) GitHub CLI invocation | `scripts/regen_index.py:80-86` — resolves `shutil.which("gh")` and raises a named error when it is missing | Yes |

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

All 21 GitHub issues were deleted and verified absent on 2026-07-19. The
[deletion journal](github-issue-deletion-journal.md) records owner authorization,
the destination commit `3c9a4df`, each deletion, and its verification.

The State column records issue state at export. The Deleted column reflects
the completed cutover. Open work survives in the governed destination records.

## Related

- [Migration runbook](../runbooks/github-issues-to-docgraph-migration.md)
- [Issues folder](../issues/README.md)
- [Intent map](intent-map.md)
- [Current state](current-state.md)
