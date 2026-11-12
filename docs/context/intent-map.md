<!--
Status: active
Owner: CT
Created: 2026-07-14
Last verified: 2026-11-12
Kind: context
-->

# Intent map

## Agent Index

- **Status:** active
- **Owner:** CT
- **Created:** 2026-07-14
- **Last verified:** 2026-11-12
- **Kind:** context
- **Read when:** evaluating direction, deferred work, rejected approaches, or owner decisions.
- **Search terms:** active intent, deferred work, rejected direction, owner decision.

## Active bets

- **Active:** Keep the static release-asset index as the current distribution
  path. Evidence: [README](../../README.md) and the
  [current architecture](../architecture/python-release-asset-index.md).

## Deferred work

The [roadmap](../roadmap.md#deferred-and-where-it-belongs) holds the detail.
These items stay deferred:

- **Deferred:** Move pdomain distributions to PyPI. Each changed distribution
  needs a new version, then consumers can remove their private-index source
  mappings. This is not a new repository.
- **Deferred:** Automate the audit between live lint suppressions and the
  suppression catalogue. No automated drift gate exists.
- **Deferred:** Replace or validate the space-delimited `RELEASE_VERSION_FILES`
  contract. Consider a shared release driver rather than another local fix.
  [Consider in another repository](../roadmap.md#consider-in-another-repository).

## Rejected directions

- **Rejected:** Configure the pdomain index as an unrestricted one-off index.
  This can fall through to a same-named public package. Use explicit source
  mappings or a direct artifact requirement. Evidence:
  [private-index decision](../decisions/private-index-resolution.md).

## Blocked (waiting on)

None.

## Needs owner decision

The [roadmap](../roadmap.md#decide-before-building) holds the detail. Neither
decision has been made:

- **Needs owner decision:** What remains of the pd-index rename effort. The
  closeout that would mark the cluster superseded is not applied. Do not start
  a legacy-name sweep from this repository.
  [Rename sweep record](../issues/2026-07-19-gh-001-015-rename-sweep.md).
- **Needs owner decision:** Whether the dep-refresh branch issue still needs
  the reusable-branch fix. The workflow file is gone. Leftover remote branches
  and `delete_branch_on_merge` are unverified.
  [Dep-refresh issue](../issues/2026-08-08-dep-refresh-cannot-auto-land.md).

## Legacy-unverified sweep

The 2026-07-14 migration classified these files as still active:

- `AGENTS.md`
- `CLAUDE.md`
- `CONVENTIONS.md`
- `docs/conventions/ignored-surfaces.md`
- `docs/conventions/lint-deviations.md`
- `docs/process/writing-style.md`

The evidence is recorded in the
[2026-07-14 legacy-guidance decision](decisions.md#2026-07-14--verify-legacy-guidance-as-active).
