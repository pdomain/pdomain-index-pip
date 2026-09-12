---
kind: handoff
status: "retired"
created: "2026-07-17"
created_at: "2026-07-17T09:19:04Z"
owner: CT
branch: master
scope: issue-tracker-migration
worktree: /workspaces/pdomain/pdomain-index-pip
base_commit: cab8705b88e86757d695a8b40c40062dcb682729
supersedes: ""
superseded_by: "docs/runbooks/github-issues-to-docgraph-migration.md"
---

# Issue tracker migration pickup prompt — pdomain-index-pip

## Agent Index

- **Kind:** handoff
- **Status:** retired
- **Read when:** picking up the task of migrating this repo's GitHub issue
  tracker into docs, before creating `docs/roadmap.md` or touching any issue.
- **Search terms:** issue tracker migration, roadmap migration, close issues,
  archive issues, docgraph handoff, pd-index-pip backlog

> **Retired 2026-07-19.** Superseded by the
> [migration runbook](../runbooks/github-issues-to-docgraph-migration.md), which
> uses governed `docs/issues/` records instead of the `docs/roadmap.md` plus
> archive-then-`git rm` pattern proposed here. This document's mdformat
> frontmatter finding was correct and has been fixed; its `pre-commit` note
> remains accurate. Its scope assumption did not hold: five of the six
> index-hardening issues were already implemented. Do not follow the procedure
> below.

## Goal

Clear this repo's GitHub issue tracker: migrate the open backlog into a new
`docs/roadmap.md`, archive every issue's full text (body + comments) into Git
history, then delete the issues from GitHub. This is the same pattern already
run on `pdomain-ocr-cli` (50 issues) and `pdomain-ocr-simple-gui` (37 issues,
roadmap-first). Do not perform the migration in this handoff-writing session —
this document only records the plan and findings for whoever runs it.

## Current state

As of this handoff, `pdomain-index-pip` has 20 open issues and 1 closed issue
(`#19`, `stateReason: COMPLETED` — "Add sha256 fragments to simple-index
distribution links"; trivial, already shipped, no migration action needed for
it).

Label breakdown across the 20 open issues:

- `kind:feature` — 14 issues (`#2`–`#15`). These are sub-tasks of one rename
  effort: spec `#1` ("Spec: Rename pd-index → pd-index-pip") plus a tracking
  issue per affected repo/area. None carry effort or model-triage labels,
  consistent with being an older batch of tracking issues from one plan.
- `kind:chore` — 3 issues (`#18`, `#20`, `#21`).
- `kind:bug` — 2 issues (`#16`, `#17`).
- `kind:spec` — 1 issue (`#1`, the rename spec itself — parent of the
  `kind:feature` cluster).
- `status:backlog` — all 20 open issues carry this label; none are in
  progress.
- Effort/model-triage labels (`effort:S`/`effort:M`, `model:sonnet`,
  `model-effort:low`/`medium`) appear only on the 5 newer issues
  `#16`–`#18`, `#20`, `#21` — the rename-cluster issues (`#1`–`#15`) predate
  that triage convention.

Representative titles:

- `#1` — Spec: Rename pd-index → pd-index-pip
- `#2` — Preflight (manual, by CT)
- `#4` — `pd-ocr-cli`: rename references
- `#11` — Workspace `CLAUDE.md` + `.gitignore`
- `#14` — Sweep workspace `docs/` and the renamed `pd-index-pip/` repo's own
  internals
- `#15` — Workspace-wide verification grep
- `#16` — Document dependency-confusion-safe pip and uv index usage
- `#17` — Fail regen when release asset fetches fail unexpectedly
- `#18` — Update README to canonical pd-index-pip Pages URL
- `#20` — Add tests for simple-index generator behavior
- `#21` — Resolve gh executable before subprocess invocation

Read: this is real, unfinished backlog, not stale noise. It splits into two
clusters — (1) the pd-index → pd-index-pip rename sweep (`#1`–`#15`), whose
per-repo and per-area tracking issues appear largely unstarted (no linked
PRs found during this pass), and (2) newer, standalone hardening work on the
index generator and its docs (`#16`–`#18`, `#20`, `#21`). Both clusters need
to survive into `docs/roadmap.md` before their issues are deleted.

Repo facts confirmed this session: `docs/decisions/` already exists (holds
`private-index-resolution.md` among others); there is no `docs/roadmap.md`
yet; docgraph is present (`DOCGRAPH.md` at repo root, `docs/architecture/`,
`docs/context/`, `docs/conventions/`, `docs/decisions/`, `docs/process/` all
exist); the acting account has admin rights on the repo (required later for
`gh issue delete`). Working tree was clean at the start of this session.

## Decisions

- **Scope:** migrate all 20 **open** issues. The 1 closed issue (`#19`) is
  trivial and already implemented — it needs no roadmap entry, only a
  one-line mention in the archive doc for completeness if convenient.
- **Roadmap-first is REQUIRED, not optional.** Because these 20 issues are
  unfinished backlog (not closed-but-undone busywork), the roadmap must be
  authored and committed *before* any issue is deleted. Never delete an
  issue without first carrying its still-open work into `docs/roadmap.md`.
  This mirrors the `pdomain-ocr-simple-gui` precedent, where issues were
  closed as `COMPLETED` but the work wasn't actually done, so the roadmap
  had to absorb it first.

## The proven procedure

1. **Pull every in-scope issue verbatim.** For each of the 20 open issues
   (and optionally `#19` for completeness):

   ```bash
   gh issue view N --repo pdomain/pdomain-index-pip \
     --json number,title,author,createdAt,closedAt,state,stateReason,labels,body,comments,url
   ```

   Save each to a scratch file and `sha256sum` it so the archive step can be
   checked against the pulled content later.

1. **Author `docs/roadmap.md`**, mirroring the structure of
   `../pdomain-ocr-cli/docs/roadmap.md` (frontmatter with `kind: plan`,
   `status: active`, `owner`, `created`, `last_verified`; an `## Agent Index`
   block; `## Goal`, `## Architecture`, `## Tech Stack`, `## Global Constraints`; then work clusters broken into `## Now`, `## Next`, `## Later`). Tag every migrated item with its originating `#NNN` so it stays
   cross-referenceable after the issue is gone. Keep the two natural
   clusters from Current State above as distinct sections or sub-groupings
   (rename sweep vs. index-generator hardening) rather than flattening them.

1. **Render the archive doc**,
   `docs/decisions/2026-07-DD-closed-issues-archive.md` (use the actual run
   date for `DD`): docgraph frontmatter (`Kind: decision`, `Status: retired`)
   plus an `## Agent Index` block, then `## Context` / `## Decision` / `## Consequences` / `## Supersedes` sections, then one `## #N — <title>`
   subsection per issue with its metadata (author, created/closed dates,
   state, stateReason, labels, url) followed by the full body and every
   comment verbatim. Add `<!-- markdownlint-disable -->` immediately after
   the frontmatter closing `---` so the verbatim issue text doesn't trip
   markdownlint. This file's own git history is the durable snapshot,
   despite the file being deleted in step 4.

1. **Commit roadmap + archive together** in one commit. Then, in a
   **second, separate commit**, `git rm` the archive file, with a commit
   message that cites the first commit's SHA so a future reader can run
   `git show <sha>:<path>` to retrieve the full archive. The roadmap file
   stays live in the tree; the archive file does not — Git history is the
   tombstone.

1. **Only after the archive commit exists**, and only with an explicit
   human "go" (this is permanent and irreversible), delete each in-scope
   issue: `gh issue delete N --repo pdomain/pdomain-index-pip --yes`. Do not
   run this step automatically or speculatively.

## Gotchas

- `pre-commit-update` may bump `.pre-commit-config.yaml` as a side effect of
  any commit and abort it, **if a `.pre-commit-config.yaml` exists**. As of
  this handoff, `pdomain-index-pip` has no `.pre-commit-config.yaml` and no
  `pre-commit` binary in its venv — this repo's static checks run through
  `make docs-check` (`uv run mdformat --check README.md CONVENTIONS.md docs`), not pre-commit. If a pre-commit config is added later and it
  bumps the pin, revert with `git checkout -- .pre-commit-config.yaml` and
  retry with `SKIP=pre-commit-update git commit ...`.
- **`mdformat` mangles YAML frontmatter in this repo.** `make docs-check`
  runs plain `mdformat` with no frontmatter plugin installed
  (`mdformat-frontmatter` is not a dependency here), so running `mdformat`
  (not `--check`) on a frontmatter-bearing file — such as this handoff, or
  the roadmap/archive docs step 2/3 create — will rewrite the leading `---`
  block into a thematic break and squash the fields into a heading,
  destroying it. Never run bare `uv run mdformat <file>` on a docgraph doc
  with frontmatter; only ever use `--check`, and if `--check` fails solely
  because of the frontmatter block, that is this pre-existing tooling gap,
  not a real formatting defect — fix wrapping/prose issues by hand instead
  of letting `mdformat` rewrite the file. Validate frontmatter-bearing docs
  with the `docgraph_check` MCP tool (or `docgraph check` CLI) instead, and
  treat that as authoritative over `mdformat --check` for this class of
  file. Cross-check any wording changes for readability but leave the
  frontmatter alone.
- Verbatim issue text in the archive doc may still need
  `<!-- markdownlint-disable -->` (see step 3) if a markdownlint-style
  check is later added — it is not enforced today, but the marker costs
  nothing and matches the CLI/GUI precedent.

## Pointers

- `docs/roadmap.md` — does not exist yet; this is what step 2 creates.
- `docs/decisions/` — existing directory; step 3's archive doc lands here
  (temporarily).
- `DOCGRAPH.md` — repo-root docgraph rules; read before authoring either new
  doc.
- `../pdomain-ocr-cli/docs/roadmap.md` — structural reference for step 2.
- `../pdomain-ocr-simple-gui/docs/roadmap.md` — second structural reference;
  closer precedent since its issues were also unfinished backlog despite
  being marked closed.

## Reference worked examples

- `pdomain-ocr-cli` archive-then-remove commit: `9498407`.
- `pdomain-ocr-simple-gui` archive commit `ec3979f`, followed by the removal
  commit `7f3be6b`.
- Agent memory note: `closed-issue-archive-pattern` (in the Claude Code
  per-project memory store) documents this same add-then-`git rm` pattern
  and why the archive file is removed from the tree after being committed.

## Resume steps

1. `gh issue view 1 --repo pdomain/pdomain-index-pip --json number,title,author,createdAt,closedAt,state,stateReason,labels,body,comments,url`
   (start pulling issue content, beginning with the parent spec issue).
1. `cat ../pdomain-ocr-simple-gui/docs/roadmap.md` (load the closer structural
   reference before drafting this repo's roadmap).
1. `ls docs/decisions/` (confirm naming conventions already in use in this
   repo's decisions folder before adding the archive doc).
