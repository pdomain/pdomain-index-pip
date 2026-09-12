---
Status: active
Owner: CT
Created: 2026-07-21
Last verified: 2026-07-21
Kind: spec
---

# Close the obsolete pd-index rename cluster as superseded

## Agent Index

- **Kind:** spec
- **Status:** active
- **Owner:** CT
- **Created:** 2026-07-21
- **Last verified:** 2026-07-21
- **Read when:** resolving the migrated pd-index rename cluster.
- **Search terms:** pd-index rename, superseded, disposition, legacy names.
- **Relates to:** [rename cluster issue](../issues/2026-07-19-gh-001-015-rename-sweep.md)
- **Closeout plan:** [Rename cluster supersession](../plans/2026-07-21-rename-cluster-supersession-closeout.md)

## The missing rename plan will not be reconstructed

The fifteen-record cluster will close as superseded. This repository already uses `pdomain-index-pip`, while the missing plan targeted the obsolete `pd-index-pip` stage. Reconstructing it would not define valid work for current repositories.

Remaining `pd-*` text does not justify a blind rewrite. The audit found current names, generated files, and historical records. Any future cleanup needs a new workspace issue with explicit owners and exclusions.

## Closeout changes documentation state only

The closeout will use the docgraph retirement workflow. It will resolve the issue and remove it from current-state and intent-map open-work lists. It will not edit source, other repositories, historical records, or generated files.

## Acceptance criteria

1. The issue no longer presents open implementation work.
1. Its resolution records supersession by the current rename.
1. Context docs no longer list an owner decision.
1. No legacy-name sweep is created.
1. Strict docgraph checks pass.

## Adversarial Review

The main failure mode is turning historical string matches into an unauthorized
workspace rewrite. The closeout therefore preserves evidence, changes only
governed issue state, and requires a new scoped issue for any future cleanup.
