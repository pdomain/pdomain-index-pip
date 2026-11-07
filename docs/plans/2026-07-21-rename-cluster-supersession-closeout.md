---
Status: active
Owner: CT
Created: 2026-07-21
Last verified: 2026-11-07
Kind: plan
---

# Rename Cluster Supersession Closeout Plan

## Agent Index

- **Kind:** plan
- **Status:** active
- **Owner:** CT
- **Created:** 2026-07-21
- **Last verified:** 2026-11-07
- **Read when:** closing the obsolete rename cluster.
- **Search terms:** rename cluster, superseded, closeout, doc-retirer.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the obsolete pd-index rename cluster without inventing a replacement implementation sweep.

**Architecture:** Use docgraph retirement to apply one lifecycle decision across the issue and authored context. Preserve historical evidence and leave source code untouched.

**Tech Stack:** Markdown, docgraph lifecycle tools, Git

**Spec:** [Close the obsolete pd-index rename cluster as superseded](../specs/2026-07-21-rename-cluster-supersession-design.md)

Checked against the issue and authored context on 2026-11-07: no closeout task
has been applied. Obtain the owner's disposition before execution. The
dep-refresh decision and deferred work also remain open.

______________________________________________________________________

## Goal

Close the obsolete cluster without creating implementation work.

## Architecture

Use docgraph retirement to reconcile the issue and authored context.

## Tech Stack

Markdown, docgraph lifecycle tools, and Git.

## Global Constraints

- Preserve provenance and historical evidence.
- Do not edit source code or other repositories.
- Do not create a legacy-name sweep.

### Task 1: Apply the superseded disposition

**Files:**

- Modify: `docs/issues/2026-07-19-gh-001-015-rename-sweep.md`

- Verify: `docs/context/current-state.md`

- Modify: `docs/context/intent-map.md`

- Modify: `docs/roadmap.md`

- Append: `docs/context/decisions.md`

- [ ] **Step 1: Start governed retirement**

Invoke `docgraph:doc-retirer` for the issue with this adjudication:

```text
Close as superseded. The current pdomain-index-pip rename superseded the absent
pd-index-pip plan. Do not create a legacy-name sweep. Preserve migrated evidence
and require a new scoped workspace issue if cleanup is wanted.
```

Expected: the skill proposes allowed lifecycle edits before changing docs.

- [ ] **Step 2: Record the exact resolution**

Set the resolution prose to:

```markdown
## Resolution

Superseded on <actual closeout date>. The workspace completed a later `pdomain-*` rename,
so the absent `pd-index-pip` plan no longer defines valid implementation work.
No replacement sweep is authorized. File a new scoped workspace issue if
current, non-historical legacy names still need cleanup.
```

Use the status and surviving destination selected by `docgraph:doc-retirer`.
Preserve provenance and historical evidence there. If the issue is removed,
record its tombstone and repair inbound references as that workflow requires.

- [ ] **Step 3: Reconcile authored context**

Remove only the rename entry from `docs/context/intent-map.md` and
`docs/roadmap.md`. Preserve the dep-refresh owner decision, the active `gh`
issue, and all deferred work. Keep `docs/context/current-state.md` pointing to
the roadmap. Append the approved disposition to `docs/context/decisions.md`.
Do not add a sweep elsewhere.

- [ ] **Step 4: Run lifecycle and docs gates**

Run:

```bash
docgraph reindex
docgraph check --strict
make docs-check AI=1
```

Expected: all commands pass.

- [ ] **Step 5: Commit**

```bash
git add -A -- docs/issues/2026-07-19-gh-001-015-rename-sweep.md docs/context/intent-map.md docs/context/decisions.md docs/roadmap.md
git commit -m "docs: close rename cluster as superseded"
```

### Task 2: Prove no implementation scope leaked

**Files:**

- Verify: `docs/issues/2026-07-19-gh-001-015-rename-sweep.md`

- Verify: `docs/context/current-state.md`

- Verify: `docs/context/intent-map.md`

- Verify: `docs/roadmap.md`

- Verify: `docs/context/decisions.md`

- [ ] **Step 1: Search active context**

Run: `rg -n "rename effort|rename cluster|needs owner decision" docs/context/current-state.md docs/context/intent-map.md`

Expected: no match for the superseded cluster.

- [ ] **Step 2: Confirm no replacement sweep exists**

Run: `find docs/plans docs/specs -type f -print | rg 'legacy.*sweep|rename-to-pip'`

Expected: no output.

- [ ] **Step 3: Run the repository gate**

Run: `make ci AI=1`

Expected: PASS.
