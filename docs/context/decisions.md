<!--
Status: active
Owner: CT
Created: 2026-07-14
Last verified: 2026-11-12
Kind: context
-->

# Durable decisions

## Agent Index

- **Status:** active
- **Owner:** CT
- **Created:** 2026-07-14
- **Last verified:** 2026-11-12
- **Kind:** context
- **Read when:** checking durable repository decisions and their evidence.
- **Search terms:** decisions, docgraph migration, spec lifecycle, lint suppression.

### 2026-07-14 — Govern repository documentation with docgraph

- **Context:** Repository documentation lacked explicit lifecycle metadata,
  authored context, and graph-integrity enforcement.
- **Decision:** Track the repository root as the docgraph scope, use `master` as
  the workflow base, enforce touched-document metadata, and detect
  legacy-unverified live documents.
- **Rationale:** Explicit status and graph checks keep current truth
  distinguishable from stale or historical material.
- **Evidence:** `docgraph.toml`, `DOCGRAPH.md`, and the three files in
  `docs/context/`.
- **Remaining work:** none.

### 2026-07-14 — Promote shipped truth before retiring implementation documents

- **Context:** The earlier convention described moving a completed design spec
  into architecture as a whole file.
- **Decision:** Promote current behavior and durable rationale into architecture
  and context first. Then remove completed checklist scaffolding after neighbor
  analysis, tombstone recording, reindexing, and strict checks.
- **Rationale:** Current retrieval should contain shipped truth and residual
  intent without obsolete execution projections.
- **Evidence:** `CONVENTIONS.md`, `DOCGRAPH.md`, and the active doc-retirer policy
  used for this migration.
- **Remaining work:** none.

### 2026-07-14 — Keep only live lint suppressions

- **Context:** The Ruff configuration suppressed `ANN401`, but an unsuppressed
  audit produced no `ANN401` finding. The shared script rules covered more
  call sites than the catalogue described.
- **Decision:** Remove the unused `ANN401` ignore and document the full safety
  basis for `T201`, `S603`, `S607`, `S101`, and `SC2086`.
- **Rationale:** A suppression catalogue is trustworthy only when it matches
  source and configuration.
- **Evidence:** `pyproject.toml`, `scripts/regen_index.py`,
  `scripts/update_github_actions.py`, `scripts/release-common.sh`, and
  `docs/conventions/lint-deviations.md`.
- **Remaining work:** Automated catalogue drift detection remains deferred in
  `docs/context/intent-map.md`.

### 2026-07-14 — Verify legacy guidance as active

- **Context:** Six inferred live documents were stale or legacy-unverified and
  lacked explicit lifecycle evidence.
- **Decision:** Keep `AGENTS.md`, `CLAUDE.md`, `CONVENTIONS.md`,
  `docs/conventions/ignored-surfaces.md`,
  `docs/conventions/lint-deviations.md`, and
  `docs/process/writing-style.md` active.
- **Rationale:** Each document still governs or accurately describes current
  repository behavior; none is implementation scaffolding or superseded
  history.
- **Evidence:** Commit `4a3d73f` created the assistant guidance and conventions;
  commits `799968c` and `2e4235a` refreshed or established the writing rules;
  commit `e4f3a79` added ignore and lint governance. `Makefile`,
  `.github/workflows/ci.yml`, `.github/workflows/regen.yml`, `.gitignore`,
  `pyproject.toml`, and `scripts/release-common.sh` implement the current
  commands, surfaces, and suppressions.
- **Remaining work:** none.

### 2026-07-19 Retired: Issue tracker migration pickup prompt

- **Old path:** `docs/handoff/2026-07-17-issue-tracker-migration.md` (deleted
  2026-11-09; read it with `git show 1549d08:docs/handoff/2026-07-17-issue-tracker-migration.md`)
- **Outcome:** superseded
- **Superseded by:** `docs/runbooks/github-issues-to-docgraph-migration.md`
- **Rationale kept:** The handoff proposed a `docs/roadmap.md` plus
  archive-then-`git rm` pattern. The owner chose governed `docs/issues/` records
  instead, so the procedure was never run. Its two durable findings survive: the
  mdformat frontmatter gap, which it diagnosed correctly and which commits
  `5238389` and `4a774a6` fixed, and the absence of `.pre-commit-config.yaml` in
  this repo. Its scope assumption did not hold — five of the six index-hardening
  issues were already implemented.
- **Why deleted on 2026-11-09:** Retired docs live in Git history, not the live
  tree. It was first kept as a session-continuity record. The runbook now names it
  as a Git-history reference instead of a link. Removal commit: `d8bf26cd`
- **Remaining work:** none.

### 2026-07-19 Implemented: GitHub issues to docgraph migration runbook

- **Path:** `docs/runbooks/github-issues-to-docgraph-migration.md`
- **Outcome:** implemented
- **Evidence:** All 21 GitHub issues permanently deleted and verified absent;
  Issues disabled (`hasIssuesEnabled: false`); every governed destination
  present on remote `master` at commit `3c9a4df`. Audit trail in
  `docs/context/github-issue-deletion-journal.md` and
  `docs/context/github-issue-migration-ledger.md`.
- **Rationale kept:** Status moved from `active` to `implemented` so agents do
  not read it as pending work. Its pre-cutover gate table is preserved as a
  snapshot, with a banner recording that gates 6 and 8 were resolved before
  deletion began.
- **Remaining work:** none for the migration. Issue #21's work — resolving the
  `gh` executable — remains open in `docs/issues/`, and the rename cluster
  remains `needs-owner-decision`.

### 2026-11-06 — The roadmap lists only remaining work

- **Context:** On 2026-07-19 the owner rejected a `docs/roadmap.md` that would
  archive every GitHub issue before deletion. That archive was never written.
  Open work later sat in issue files, two plans, and the intent map.
- **Decision:** Add `docs/roadmap.md` as a short list of work that is still
  unfinished. Do not archive closed issues there. Shipped index behavior stays
  in `docs/architecture/python-release-asset-index.md`. This replaces the
  2026-07-19 choice not to create a roadmap, for a remaining-work list only.
  It does not revive the archive-then-delete pattern.
- **Rationale:** A remaining-work list is a different document from the
  rejected archive. Readers can see what is left without rereading the
  migration.
- **Evidence:** This documentation pass. Neither open plan is implemented.
  `gh_json()` still calls `subprocess.run(["gh", *args])` in
  `scripts/regen_index.py`, and every task in the rename closeout plan is
  unchecked. `uv run pytest tests/test_regen_index.py` passed 18 tests on
  2026-11-06. Commit `4a91b14` removed the GitHub Actions workflows.
- **Remaining work:** the list in `docs/roadmap.md`.

### 2026-11-07 — Correct the roadmap decision's historical context

- **Correction:** The 2026-11-06 entry conflates the proposed roadmap with a
  separate issue archive. The owner rejected a roadmap plus a separate
  archive-then-delete pattern. The separate archive was never written.
- **Evidence:** The 2026-07-19 retirement entry above records the rejected
  pattern and the choice of governed `docs/issues/` records instead.
- **Decision unchanged:** The roadmap lists remaining work only.

### 2026-11-12 — One remaining-work list, and shipped release behavior lives in architecture

- **Context:** The same unfinished items were written in full in
  `docs/roadmap.md`, `docs/context/intent-map.md`, and `docs/issues/README.md`.
  The allowlist match, publish authentication, and tooling-release path were
  described in the README and the scripts, and not in the architecture doc.
- **Decision:** `docs/roadmap.md` is the only remaining-work list. The intent
  map keeps each item's classification and points at that list. Issue files
  keep the evidence. This refines the 2026-11-06 entry above. It does not
  revive an archive of closed issues. Shipped allowlist matching, publish
  authentication, and the tooling-release path now live in
  `docs/architecture/python-release-asset-index.md`.
- **Separate repositories:** The roadmap records four considerations. They are
  not approved builds. The one worth a separate repository is a single shared
  release driver: on 2026-11-12, thirteen of the repositories under
  `/mnt/work/projects/pdomain` had `scripts/release-common.sh`, in eight
  different SHA-256 hashes. A generic Python index library, a dep-refresh
  product, and a rename sweep are not candidates to build from this
  repository.
- **Rationale:** Readers should see unfinished work in one place, and current
  behavior in the architecture doc.
- **Evidence:** This documentation pass. `sha256sum` of those
  `release-common.sh` copies on 2026-11-12. A read of `scripts/regen_index.py`,
  `scripts/publish-index.sh`, `scripts/do-release.sh`, and
  `scripts/release-common.sh` the same day.
- **Remaining work:** the list in `docs/roadmap.md`. The rename disposition
  and the dep-refresh disposition are still owner decisions.
