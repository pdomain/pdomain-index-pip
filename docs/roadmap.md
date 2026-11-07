---
Status: active
Owner: CT
Created: 2026-11-06
Last verified: 2026-11-06
Kind: process
Level: I1
---

# Remaining work

## Agent Index

- **Kind:** process
- **Status:** active
- **Level:** I1
- **Owner:** CT
- **Created:** 2026-11-06
- **Last verified:** 2026-11-06
- **Read when:** checking what is still unfinished in this repository.
- **Search terms:** remaining work, roadmap, open issues, open plans.

Open work is the list below. Each line is one unfinished item and the file
that holds it.

The generated index and the local publish path are shipped.

## Still open

- Resolve `gh` to an absolute path before `scripts/regen_index.py` starts it.
  Fail with a clear error when `gh` is missing. `gh_json()` still passes the
  bare name `gh`.
  [Issue](issues/2026-07-19-gh-021-resolve-gh-executable.md).
  [Plan](plans/2026-07-21-gh-executable-resolution.md).
- Apply the rename-cluster closeout, or pick another disposition. The issue
  resolution is still open. Every task in the closeout plan is unchecked.
  [Issue](issues/2026-07-19-gh-001-015-rename-sweep.md).
  [Plan](plans/2026-07-21-rename-cluster-supersession-closeout.md).
- Decide whether the dep-refresh branch issue still needs its prescribed fix.
  Commit `4a91b14` deleted `.github/workflows/dep-refresh.yml` on 2026-09-13.
  Leftover remote `dep-refresh/*` branches and `delete_branch_on_merge` are
  unverified.
  [Issue](issues/2026-08-08-dep-refresh-cannot-auto-land.md).
- Move pdomain distributions to PyPI.
  [Intent map](context/intent-map.md#deferred-work).
- Automate the check that live lint suppressions match the catalogue.
  [Intent map](context/intent-map.md#deferred-work).
- Replace or validate the space-delimited `RELEASE_VERSION_FILES` contract.
  [Intent map](context/intent-map.md#deferred-work).

## Shipped

The trust boundary, digest behavior, consumer setup, and local publish path
are in the
[release-asset index architecture](architecture/python-release-asset-index.md).
