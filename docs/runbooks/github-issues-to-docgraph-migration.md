---
kind: runbook
status: implemented
owner: CT
created: 2026-07-19
last_verified: 2026-07-19
---

# GitHub issues to docgraph migration — pdomain-index-pip

## Agent Index

- **Kind:** runbook
- **Status:** implemented
- **Read when:** executing the GitHub Issues cutover for `pdomain-index-pip`, or
  checking whether this repo is ready for it.
- **Search terms:** issue migration, docgraph, delete issues, deletion journal,
  mdformat frontmatter, rename sweep, index hardening.

> **Executed 2026-07-19.** This runbook has been fully carried out. All 21
> GitHub issues were permanently deleted, Issues was disabled
> (`hasIssuesEnabled: false`), and every governed destination is present on
> remote `master`. The audit trail is the
> [deletion journal](../context/github-issue-deletion-journal.md) and the
> [migration ledger](../context/github-issue-migration-ledger.md). It is kept as
> the record of how the cutover ran, not as pending work. The gate table below
> is preserved as the pre-cutover snapshot; gates 6 and 8 were both resolved
> before deletion began.

## What this adapts, and what changed

This runbook narrows the shared 12-repo runbook at
`/workspaces/shared-devtools/docs/runbooks/github-issues-to-docgraph-migration-prompt.md`
to this repository. The shared version stays authoritative for anything not
restated here.

Four things differ from the shared runbook:

1. **Scope is one repository and 21 issues**, not twelve repositories. Batch
   boundaries below are fixed, not discovered at runtime.
1. **One readiness gate currently fails.** `make ci` is red, and the cause
   blocks the migration rather than merely delaying it. See the next section.
1. **A prior handoff proposed a different pattern** and must be retired as part
   of this work, not left to contradict this runbook.
1. **Gate 8 is unverified.** Nobody has confirmed that the `pdomain`
   organization allows issue deletion.

## Fix the mdformat frontmatter gap before anything else

**`make docs-check` destroys YAML frontmatter, so the migration cannot produce a
single governed document until this is fixed.** This is gate 6, and it is a hard
blocker rather than a nuisance.

The repo depends on bare `mdformat>=0.7.22` (`pyproject.toml:11`) with no
frontmatter plugin. Given a frontmatter block, mdformat rewrites the opening
`---` as a thematic break and collapses every field into one heading:

```text
---                          ______________________________________________________________________
kind: handoff
status: "active"      -->    ## kind: handoff status: "active" created: "2026-07-17" ...
owner: CT
---
```

This is already breaking CI. Commit `10d63ed` added
`docs/handoff/2026-07-17-issue-tracker-migration.md`, the first and only
frontmatter-bearing file under `docs/`, and `static-check` has failed ever
since.

The failure surfaced on PR #26 rather than on master because the `ci`
workflow runs only on pull requests. Master's recent runs are all scheduled
`regen-and-deploy` and `dep-refresh` jobs, which never call `make docs-check`.

Every document this migration creates carries frontmatter. Roughly 22 new files
would each reproduce the failure.

Verified fix: add the plugin to the dev dependencies:

```bash
uv add --dev mdformat-frontmatter
uv run mdformat --check README.md CONVENTIONS.md docs   # passes
```

I confirmed this resolves the existing failure. The only difference between the
committed handoff and mdformat's output is the frontmatter block; the prose
needs no change.

Land this fix on master first. It also unblocks PR #26, which is otherwise
mergeable with auto-merge already armed.

Consider adding a master-push trigger to the `ci` workflow in the same change,
so formatting breaks surface at the commit instead of on the next unrelated PR.

## Readiness gates: all ten passed at cutover

Verified 2026-07-19 against the shared runbook's ten gates.

| # | Gate | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Clean working tree | Pass, with a caveat | master clean; migration worktree holds untracked `docs/issues/` |
| 2 | Read `AGENTS.md`, `CONVENTIONS.md`, `DOCGRAPH.md` | Pass | all three present at repo root |
| 3 | `docgraph.toml` enables workflow enforcement and legacy-unverified detection | Pass | `workflow.enabled = true`, `legacy_unverified = true` |
| 4 | `docgraph check --strict` reports zero issues | Pass | 0 issues, 0 blocking |
| 5 | `docs/issues/README.md` and `TEMPLATE.md` exist | Pass, uncommitted | both present in the worktree, untracked |
| 6 | Full CI gate passes | **Fail** | `static-check` red on mdformat frontmatter |
| 7 | Remote and default branch unambiguous | Pass | single `origin`, default `master` |
| 8 | Org-level issue deletion enabled | **Unverified** | not queryable from the repo API |
| 9 | Actor has admin or owner access | Pass | `viewerPermission: ADMIN` |
| 10 | Default branch protected | Pass, with a caveat | force-push and deletion both blocked; `enforce_admins` is `false`, so an admin can bypass |

Two gates need action before the migration starts: fix gate 6 as described
above, and confirm gate 8 with an owner. Commit the gate 5 scaffolding as the
migration branch's first commit so the template is governed rather than
floating.

## Scope: 21 issues in two clusters

The repo has 20 open issues and 1 closed issue. All 20 open issues carry
`status:backlog`; none are in progress, which matches the clean working tree.

**The rename sweep, `#1`–`#15`.** It has a parent spec (`#1`, "Spec: Rename
pd-index → pd-index-pip") plus one tracking issue for each affected repository
or area: `pd-book-tools`, `pd-ocr-cli`, `pd-ocr-labeler`, `pd-ocr-labeler-spa`,
`pd-ocr-synth`, `pd-ocr-trainer`, `pd-png-optimizer`, and `pd-prep-for-pgdp`. It
also includes workspace-level sweeps and a verification grep. These issues
predate the effort/model triage convention and carry no effort labels. No
linked pull requests were found, so treat them as unstarted.

**Index-generator hardening, `#16`–`#18`, `#20`, `#21`.** This is newer,
standalone work: two bugs (`#16` dependency-confusion-safe index docs, `#17`
failing regen on unexpected asset-fetch errors), plus `#20` generator tests and
`#21` resolving the `gh` executable before subprocess invocation. `#18`
overlaps the rename cluster: it updates the README to the canonical Pages URL.

**The closed issue, `#19`.** "Add sha256 fragments to simple-index distribution
links", `stateReason: COMPLETED`, already shipped. It gets one ledger row, not a
governed issue record.

Both clusters are real unfinished backlog, not stale noise. Neither may be
deleted from GitHub before its work survives into the tree.

## Retire the conflicting handoff

`docs/handoff/2026-07-17-issue-tracker-migration.md` prescribes a different
pattern. It would fold the open backlog into a new `docs/roadmap.md` and dump
verbatim issue text into a `docs/decisions/` archive. Then it would commit that
archive and `git rm` it, so Git history becomes the tombstone. That mirrors the
`pdomain-ocr-cli` and `pdomain-ocr-simple-gui` migrations.

**This runbook supersedes that plan.** The owner chose the shared runbook's
governed-records pattern on 2026-07-19: per-issue documents under `docs/issues/`
that stay live and docgraph-governed, a completed-issue ledger, and an
append-only deletion journal. Provenance stays queryable without `git show`.

Route the handoff through `doc-retirer` with this runbook as the superseding
document. Do not leave both live. A future agent reading only the handoff would
produce the wrong artifacts.

Keep two findings from the handoff; they remain accurate and useful:

- The mdformat frontmatter gap, which that document diagnosed correctly. This
  runbook resolves it rather than working around it.
- This repo has no `.pre-commit-config.yaml` and no `pre-commit` binary, so the
  `pre-commit-update` pin-bump failure seen in sibling repos does not apply
  here. Static checks run through `make docs-check`.

## Three fixed batches

The shared runbook caps batches at 10 issues. These three batches follow the
cluster boundaries above, so each commit is reviewable as one coherent unit.

| Batch | Issues | Count | Theme |
| --- | --- | --- | --- |
| 1 | `#1`–`#10` | 10 | Rename sweep: spec, preflight, per-repo tracking |
| 2 | `#11`–`#15`, `#19` | 6 | Rename sweep: workspace areas, verification, plus the closed-issue ledger row |
| 3 | `#16`–`#18`, `#20`, `#21` | 5 | Index-generator hardening |

Run the shared runbook's full nine-step post-batch sequence after each batch:

1. Stage.
1. `docgraph reindex`.
1. `docgraph check --strict` at zero.
1. `git diff --check`.
1. Focused tests for any architecture claim needing code inspection.
1. Repository CI when source or config changed.
1. Read-only review.
1. Fix every Critical and Important finding.
1. Commit locally with the issue range in the message.

Delete no GitHub issues during batch processing.

## Destinations in this repo

This repo has `docs/architecture/`, `docs/context/`, `docs/conventions/`,
`docs/decisions/`, `docs/handoff/`, and `docs/process/`. It has no `docs/plans/`,
`docs/specs/`, or `docs/research/`, so the shared runbook's references to active
plans and specs resolve to `docs/issues/` records here.

| Content | Destination |
| --- | --- |
| Active, deferred, blocked, or owner-decision work | `docs/issues/YYYY-MM-DD-gh-NNN-short-slug.md` |
| Completed issues (`#19`) | `docs/context/github-issue-migration-ledger.md` |
| Present-tense shipped behavior | `docs/architecture/python-release-asset-index.md` |
| Durable rationale | `docs/context/decisions.md` (append-only; never overwrite) |
| Deferred or unresolved intent | `docs/context/intent-map.md` |
| Active work and risks | `docs/context/current-state.md` |
| Deletion audit trail | append-only deletion journal under `docs/context/` |

`docgraph.toml` infers `kind = "issue"` and `status = "active"` for anything
under `issues/**`, so per-issue records need no manual kind declaration. They
still need frontmatter and a matching Agent Index.

The already-scaffolded `docs/issues/README.md` fixes two of these paths. It
links the ledger at `docs/context/github-issue-migration-ledger.md` and points
open records at `docs/context/intent-map.md`. Use those exact paths. Until
batch 2 creates the ledger, that link dangles and `docgraph check --strict`
reports one blocking error — expected before the migration runs, and resolved
by the ledger's first commit.

## Trigger

Run this when gates 6 and 8 both pass and the owner has given an explicit go for
this repository.

## Preconditions

All ten gates in the shared runbook's "Repository readiness gates" must hold.
Two currently do not: fix the mdformat frontmatter gap (gate 6), and confirm
organization-level issue deletion (gate 8). Owner authorization for permanent
deletion applies only after every cutover gate passes, including the pushed and
verified replacement.

## Steps

Follow the shared runbook's copyable prompt, in this order:

1. Inventory with raw exports and SHA-256 digests.
1. Classify.
1. Prove architecture coverage for the one closed issue.
1. Create governed records.
1. Reconcile lifecycle state.
1. Process the three batches above.
1. Push and verify the durable replacement.
1. Permanently delete and disable Issues.

This document supplies the repo-specific scope, batches, destinations, and
gate status. The shared runbook supplies the procedure.

Two repo-specific insertions:

- Before batch 1, commit the untracked `docs/issues/README.md` and
  `TEMPLATE.md`, and retire the conflicting handoff.
- Land the mdformat fix on master and let PR #26 merge before branching, so the
  migration branch does not carry an unrelated red CI gate.

## Verification

The shared runbook's "Final verification" section is the check:

1. Full CI gate.
1. `docgraph reindex`.
1. `docgraph check --strict` at zero issues.
1. `git diff --check`.
1. A fresh GitHub issue count of zero.
1. `hasIssuesEnabled: false`.
1. Every migration and deletion-journal commit present on remote `master`.

Add one repo-specific check: confirm `make docs-check` passes with frontmatter
intact across every new governed document, since that gap caused the original
gate 6 failure.

## Rollback

GitHub issue deletion is permanent, so no rollback exists after the deletion
phase. That is why deletion is gated behind a pushed, verified replacement and
an append-only deletion journal.

Before any deletion, rollback means abandoning the migration branch. The branch
`migrate/github-issues-docgraph` currently holds zero commits ahead of master,
so nothing is at risk today. If any deletion or verification fails, stop the
cutover immediately rather than retrying with a different issue ID.

## Related documents

- Shared source runbook:
  `/workspaces/shared-devtools/docs/runbooks/github-issues-to-docgraph-migration-prompt.md`
- Superseded plan: [`docs/handoff/2026-07-17-issue-tracker-migration.md`](../handoff/2026-07-17-issue-tracker-migration.md)
- Repo docgraph rules: [`DOCGRAPH.md`](../../DOCGRAPH.md)
- Architecture record: [`docs/architecture/python-release-asset-index.md`](../architecture/python-release-asset-index.md)
