---
Status: active
Owner: CT
Created: 2026-11-13
Last verified: 2026-11-13
Kind: architecture
---

# Governed documentation and issue evidence

## Agent Index

- **Status:** active
- **Owner:** CT
- **Created:** 2026-11-13
- **Last verified:** 2026-11-13
- **Kind:** architecture
- **Read when:** locating current issue evidence or auditing the completed tracker cutover.
- **Search terms:** documentation governance, issue migration, ledger, retirement, provenance.

Current work lives in governed repository documentation. GitHub Issues was
disabled after the 2026-07-19 tracker cutover. Deleting external tickets did
not resolve their unfinished work.

## Current sources of truth

The [roadmap](../roadmap.md) is the only remaining-work list. The
[intent map](../context/intent-map.md) classifies that work. Records under
[issues](../issues/README.md) retain evidence and unresolved owner questions.
Architecture records shipped behavior, rather than execution checklists.

The rename-cluster disposition and the remaining dep-refresh cleanup/settings
question are still open. The [roadmap](../roadmap.md#decide-before-building)
links their evidence and scope. Neither the completed tracker migration nor
this documentation migration approves those proposed changes.

## Cutover evidence stays separate from current work

The [migration ledger](../context/github-issue-migration-ledger.md) maps all
21 former issues to governed destinations. The
[deletion journal](../context/github-issue-deletion-journal.md) preserves
authorization, node IDs, raw SHA-256 digests, deletion times, and recorded
absence checks. Those audit records remain live references.

The original exported issue bodies were not committed, and deleted tickets
cannot be re-exported. The preserved digests and destination evidence therefore
matter independently of the retired execution procedure.

The historical runbook is recoverable from Git. Its obsolete readiness gates,
workflow commands, and batch instructions are not current operating guidance.
Its former path remains a short retirement tombstone because the append-only
deletion journal links to it.

## Tooling preserves retrievable documentation

[DOCGRAPH.md](../../DOCGRAPH.md) defines retrieval and lifecycle rules.
`docgraph.toml` scans root Markdown and `docs/` with declared metadata and
Agent Index fields. Workflow checks enforce touched-document metadata and
required sections. `just ci` ends with strict docgraph checks.

Markdown formatting uses `mdformat-frontmatter` so YAML metadata survives
formatting. Pre-commit hooks and the locked development toolchain are
configured in the repository. The initial frontmatter-formatting gap was
fixed before the tracker cutover.

Completed plans and specs retire only after their durable content is promoted
and inbound links are handled. Specs also require an actual recorded
adversarial review. Tombstones and append-only decisions retain provenance;
unfinished intent stays in the roadmap, issue evidence, and intent map.

## Evidence

- Configuration: `docgraph.toml`, `pyproject.toml`,
  `.pre-commit-config.yaml`, and `justfile`.
- Rules: [DOCGRAPH.md](../../DOCGRAPH.md) and the
  [issue process](../issues/README.md).
- Cutover: commit `e3d1b98` records completion; `3c9a4df` contains
  governed destinations; `b5a6858`, `095149d`, and `6666daf` record
  deletion batches.
- Audit records: the ledger and journal preserve the historical API results.
  This migration checks those local records; it does not repeat deletions.
- Verified: 2026-11-13 by source, configuration, and Git-history inspection.
  Read-only repository metadata also reported `has_issues: false`.
