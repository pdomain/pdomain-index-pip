---
Status: active
Owner: CT
Created: 2026-11-06
Last verified: 2026-11-12
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
- **Last verified:** 2026-11-12
- **Read when:** checking what is still unfinished in this repository.
- **Search terms:** remaining work, roadmap, open issues, open plans,
  separate repository.

This is the only remaining-work list. The intent map classifies items and
points here. Issue files keep the evidence. Shipped behavior is the
[release-asset index architecture](architecture/python-release-asset-index.md).

## Still to do in this repository

- Resolve `gh` to an absolute path before `scripts/regen_index.py` starts it.
  Fail with a clear error when `gh` is missing. `gh_json()` still passes the
  bare name `gh`.
  [Issue](issues/2026-07-19-gh-021-resolve-gh-executable.md).
  [Spec](specs/2026-07-21-gh-executable-resolution-design.md).
  [Plan](plans/2026-07-21-gh-executable-resolution.md).

## Decide before building

- Apply the rename-cluster closeout, or pick another disposition. The
  2026-05-16 plan those issues pointed at is still absent. The 2026-07-21
  spec and closeout plan say to close the cluster as superseded, and they say
  not to create a legacy-name sweep. Every task in the closeout plan is
  unchecked. The issue resolution is still open. This repository's own names
  are already `pdomain-*`.
  [Issue](issues/2026-07-19-gh-001-015-rename-sweep.md).
  [Spec](specs/2026-07-21-rename-cluster-supersession-design.md).
  [Plan](plans/2026-07-21-rename-cluster-supersession-closeout.md).
- Decide whether the dep-refresh branch issue still needs its prescribed fix.
  Commit `4a91b14` deleted `.github/workflows/dep-refresh.yml` on 2026-09-13,
  along with the other GitHub Actions workflows. Leftover remote
  `dep-refresh/*` branches and `delete_branch_on_merge` are unverified. Do
  not rebuild that workflow here unless that decision says to.
  [Issue](issues/2026-08-08-dep-refresh-cannot-auto-land.md).

## Deferred, and where it belongs

- Move pdomain distributions to PyPI. Each changed distribution needs a new
  version, because PyPI rejects a re-upload of the same version. Consumers
  can then remove their private-index source mappings. This is a publishing
  decision for each distribution. It is not a new repository, and it does not
  need a migration tool in this one.
  [Why not PyPI](../README.md#why-not-just-publish-to-pypi).
- Automate the check that live lint suppressions match the
  [suppression catalogue](conventions/lint-deviations.md). The migration
  verified the catalogue by hand. No drift gate exists. A checker is a shared
  lint tool, not index behavior. Build it in this repository only if this
  catalogue is the only one that needs it.

## Consider in another repository

These are considerations. None of them is scheduled work.

- One shared release driver. On 2026-11-12, thirteen of the repositories
  under `/mnt/work/projects/pdomain` had `scripts/release-common.sh`, and those
  copies had eight different SHA-256 hashes. This repository vendors its own
  copy and calls it with `RELEASE_BUILD=":"`. The helper trusts a
  maintainer-provided `RELEASE_VERSION_FILES` value: a space-delimited list of
  paths that cannot contain spaces. This repository uses tag-derived versions,
  so that list is not on the path it uses today. A fix only in this copy would
  drift from the others. A shared tool is the place to replace or validate
  the contract. This repository would keep a thin `scripts/do-release.sh`.
- Do not extract a generic Python index library yet. The generator's allowlist
  and PEP 503 pages are this repository.
  [pdomain-index-npm](https://github.com/pdomain/pdomain-index-npm) is already
  the npm sibling, and it is a separate repository. Extract a Python library
  only when a second Python index needs the same trust boundary.
- Do not bring dep-refresh back here as a product. Commit `4a91b14` removed
  GitHub Actions from this repository. The auto-land design lives in
  `pdomain-ui`. The same leftover-branch question is open in other pdomain
  repositories, including `pdomain-index-npm`, `pdomain-ops`, and
  `pdomain-ocr-training`. If that workflow returns, it belongs with the
  repositories that still run Actions.
- Do not start a workspace rename sweep from this repository. The closeout
  spec says not to invent one. Any later sweep needs a new workspace issue.
