---
Status: active
Owner: CT
Created: 2026-07-21
Last verified: 2026-11-07
Kind: spec
---

# Close the obsolete pd-index rename cluster as superseded

## Agent Index

- **Kind:** spec
- **Status:** active
- **Owner:** CT
- **Created:** 2026-07-21
- **Last verified:** 2026-11-07
- **Read when:** resolving the migrated pd-index rename cluster.
- **Search terms:** pd-index rename, superseded, disposition, legacy names.
- **Relates to:** [rename cluster issue](../issues/2026-07-19-gh-001-015-rename-sweep.md)
- **Closeout plan:** [Rename cluster supersession](../plans/2026-07-21-rename-cluster-supersession-closeout.md)

## The missing rename plan will not be reconstructed

Checked against the issue and authored context on 2026-11-07: the cluster is
still `needs-owner-decision`. This closeout remains a proposal requiring the
owner's disposition; it has not been applied.

The fifteen-record cluster will close as superseded. This repository already uses `pdomain-index-pip`, while the missing plan targeted the obsolete `pd-index-pip` stage. Reconstructing it would not define valid work for current repositories.

Remaining `pd-*` text does not justify a blind rewrite. The audit found current names, generated files, and historical records. Any future cleanup needs a new workspace issue with explicit owners and exclusions.

## Closeout changes documentation state only

The closeout will use the docgraph retirement workflow. It will resolve the
issue and remove only the rename entries from the intent map and roadmap.
Current-state will keep its roadmap pointer. Other open work stays intact.
The closeout will append its disposition to the decision log. It will not edit
source, other repositories, existing historical records, or generated files.

## Acceptance criteria

1. The issue no longer presents open implementation work.
1. Its resolution records supersession by the current rename.
1. Context docs no longer list the rename owner decision. Other open decisions
   remain intact.
1. No legacy-name sweep is created.
1. Strict docgraph checks pass.

## Adversarial Review

The main failure mode is turning historical string matches into an unauthorized
workspace rewrite. The closeout therefore preserves evidence, changes only
governed issue state, and requires a new scoped issue for any future cleanup.
