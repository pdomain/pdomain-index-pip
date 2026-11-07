<!--
Status: active
Owner: CT
Created: 2026-07-14
Last verified: 2026-11-06
Kind: context
-->

# Intent map

## Agent Index

- **Status:** active
- **Owner:** CT
- **Created:** 2026-07-14
- **Last verified:** 2026-11-06
- **Kind:** context
- **Read when:** evaluating direction, deferred work, rejected approaches, or owner decisions.
- **Search terms:** active intent, deferred work, rejected direction, owner decision.

## Active bets

- **Active:** Keep the static release-asset index as the current distribution
  path. Evidence: [README](../../README.md) and the
  [current architecture](../architecture/python-release-asset-index.md).

## Deferred work

- **Deferred:** Move pdomain distributions to PyPI. Each changed distribution
  needs a new version, then consumers can remove their private-index source
  mappings. Evidence: [README](../../README.md#why-not-just-publish-to-pypi).
- **Deferred:** Automate the audit between live lint suppressions and the
  [suppression catalogue](../conventions/lint-deviations.md). The migration
  verified the catalogue manually. No automated drift gate exists.
- **Deferred:** Replace or validate the space-delimited `RELEASE_VERSION_FILES`
  contract in `scripts/release-common.sh`. The current helper trusts a
  maintainer-provided environment value. It cannot represent paths with spaces.

## Rejected directions

- **Rejected:** Configure the pdomain index as an unrestricted one-off index.
  This can fall through to a same-named public package. Use explicit source
  mappings or a direct artifact requirement. Evidence:
  [private-index decision](../decisions/private-index-resolution.md).

## Blocked (waiting on)

None.

## Needs owner decision

- **Needs owner decision:** What remains of the pd-index rename effort. The
  2026-05-16 plan those issues pointed at is still absent. A 2026-07-21 spec
  and closeout plan say to close the cluster as superseded. They also say not
  to create a legacy-name sweep. Every task in that plan is unchecked. The
  issue resolution is still open. Evidence:
  [rename sweep record](../issues/2026-07-19-gh-001-015-rename-sweep.md),
  [closeout spec](../specs/2026-07-21-rename-cluster-supersession-design.md),
  [closeout plan](../plans/2026-07-21-rename-cluster-supersession-closeout.md).
- **Needs owner decision:** Whether the dep-refresh branch issue still needs
  the reusable-branch fix. Commit `4a91b14` (2026-09-13) deleted
  `.github/workflows/dep-refresh.yml` with the other GitHub Actions workflows.
  Leftover remote `dep-refresh/*` branches and `delete_branch_on_merge` are
  unverified. Evidence:
  [dep-refresh issue](../issues/2026-08-08-dep-refresh-cannot-auto-land.md).

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
