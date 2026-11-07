---
Status: active
Owner: CT
Created: 2026-07-19
Last verified: 2026-11-07
Kind: reference
Level: I1
---

# GitHub issue deletion journal

## Agent Index

- **Kind:** reference
- **Status:** active
- **Level:** I1
- **Last verified:** 2026-11-07
- **Read when:** auditing which GitHub issues were permanently deleted, when,
  by whom, and where their content went.
- **Search terms:** deletion journal, issue deletion, audit trail, node ID,
  permanent deletion, cutover.

## What this records

**This journal is append-only.** It records the permanent deletion of GitHub
issues from `pdomain/pdomain-index-pip` after their content was migrated into
governed documentation. GitHub issue deletion cannot be undone.

Every row was written and pushed **before** the corresponding deletion ran, as
required by the
[migration runbook](../runbooks/github-issues-to-docgraph-migration.md).

- **Actor:** ConcaveTrillion (repository admin)
- **Authorized:** 2026-07-19 by the owner, after all cutover gates passed
- **Merged commit carrying every destination:** `3c9a4df`
- **Organization setting:** `members_can_delete_issues: true`

Former issue URLs all follow
`https://github.com/pdomain/pdomain-index-pip/issues/<N>`.

## Batch 1 — closed issues

| # | Node ID | Raw digest (SHA-256) | Destination | Deleted | Verified absent |
| --- | --- | --- | --- | --- | --- |
| 19 | `I_kwDOSWRi3c8AAAABDJFTFw` | `a22f958583a1d8716181309ac39efd5b12da93e85d70723ae5d381e0954edccb` | `docs/architecture/python-release-asset-index.md` | 2026-07-19T11:11Z | yes |

## Batch 2 — open issues #1–#10

| # | Node ID | Raw digest (SHA-256) | Destination | Deleted | Verified absent |
| --- | --- | --- | --- | --- | --- |
| 1 | `I_kwDOSWRi3c8AAAABCgbYgA` | `697b0ecd955ae94c033dfd75b783c569d4075c99341d60a8e3ae3af56cd1edaa` | `docs/issues/2026-07-19-gh-001-015-rename-sweep.md` | 2026-07-19T11:12Z | yes |
| 2 | `I_kwDOSWRi3c8AAAABCgbdvg` | `2bfda1f4704ad088891e8c67a5177e9cc687470b55e999ddf818126924a67b97` | `docs/issues/2026-07-19-gh-001-015-rename-sweep.md` | 2026-07-19T11:12Z | yes |
| 3 | `I_kwDOSWRi3c8AAAABCgbd0g` | `aabbf1d1aafc93be9a9b727da54d5024e4784fb786fef098cdc3f4c9e92c1437` | `docs/issues/2026-07-19-gh-001-015-rename-sweep.md` | 2026-07-19T11:12Z | yes |
| 4 | `I_kwDOSWRi3c8AAAABCgbd6g` | `cdf22341df0fb1709083070f81715dedcaedf6926d474f568701ee3ab536fcd3` | `docs/issues/2026-07-19-gh-001-015-rename-sweep.md` | 2026-07-19T11:12Z | yes |
| 5 | `I_kwDOSWRi3c8AAAABCgbeDQ` | `4a2c258f296ea405adccb36ecdec702bbd4cb6f56503fe1d5195f1f27bf36bc9` | `docs/issues/2026-07-19-gh-001-015-rename-sweep.md` | 2026-07-19T11:12Z | yes |
| 6 | `I_kwDOSWRi3c8AAAABCgbeFw` | `088b3dc22dcc37da8d0b6a211d7f23b4d4bd669ed660612a38f38e9ab9ccc216` | `docs/issues/2026-07-19-gh-001-015-rename-sweep.md` | 2026-07-19T11:12Z | yes |
| 7 | `I_kwDOSWRi3c8AAAABCgbeLA` | `808110d3f46edf4abe77a15e523c298c0843c59beb39f670acbcfc1ce1dbb709` | `docs/issues/2026-07-19-gh-001-015-rename-sweep.md` | 2026-07-19T11:12Z | yes |
| 8 | `I_kwDOSWRi3c8AAAABCgbeQA` | `fd9ee9c43909b607d97cc4e8384ce4c8d85ff55f58441c263fc230bce7cd9e77` | `docs/issues/2026-07-19-gh-001-015-rename-sweep.md` | 2026-07-19T11:12Z | yes |
| 9 | `I_kwDOSWRi3c8AAAABCgbeWQ` | `68ff2f20d669253b50e55e44608b61a28285eb11e684af33703edf4309ca7d90` | `docs/issues/2026-07-19-gh-001-015-rename-sweep.md` | 2026-07-19T11:12Z | yes |
| 10 | `I_kwDOSWRi3c8AAAABCgbecw` | `3407ccc25d37ea0c4a18d5ea262107a7c9759990de136a7c8233581bdf561dc5` | `docs/issues/2026-07-19-gh-001-015-rename-sweep.md` | 2026-07-19T11:12Z | yes |

## Batch 3 — open issues #11–#21

| # | Node ID | Raw digest (SHA-256) | Destination | Deleted | Verified absent |
| --- | --- | --- | --- | --- | --- |
| 11 | `I_kwDOSWRi3c8AAAABCgbehg` | `341245624b9dc21625dbcb5aa27e473e999fafa386badd4b6898365c55f9fe55` | `docs/issues/2026-07-19-gh-001-015-rename-sweep.md` | 2026-07-19T11:13Z | yes |
| 12 | `I_kwDOSWRi3c8AAAABCgbeqQ` | `e5b607410bd95190c7a313280517414e3d4e2c6adb69086c71b1f8df7473596f` | `docs/issues/2026-07-19-gh-001-015-rename-sweep.md` | 2026-07-19T11:13Z | yes |
| 13 | `I_kwDOSWRi3c8AAAABCgbevQ` | `f24440c674e7188f708533145c6405ee089c23de4a6919264c6af6252108f57b` | `docs/issues/2026-07-19-gh-001-015-rename-sweep.md` | 2026-07-19T11:13Z | yes |
| 14 | `I_kwDOSWRi3c8AAAABCgbe0g` | `89543c7f35ca0e2a2725a65b61008868630b5fb136b27331fb4ddc52f37c1952` | `docs/issues/2026-07-19-gh-001-015-rename-sweep.md` | 2026-07-19T11:13Z | yes |
| 15 | `I_kwDOSWRi3c8AAAABCgbe8g` | `85fd2cba46d98906215e48bbdaba66878ff305f5c9053b713782b55c1a170e5f` | `docs/issues/2026-07-19-gh-001-015-rename-sweep.md` | 2026-07-19T11:13Z | yes |
| 16 | `I_kwDOSWRi3c8AAAABDJFSeQ` | `a3aa493d665be5696644025922350b000cba33f50d988381c416649a78ffc4fd` | `docs/architecture/python-release-asset-index.md` | 2026-07-19T11:13Z | yes |
| 17 | `I_kwDOSWRi3c8AAAABDJFStQ` | `f1c0fe6964b6ef9e60cd8541d7480bc7ad5c12c5bca3b45767e70a1d3257fe8b` | `docs/architecture/python-release-asset-index.md` | 2026-07-19T11:13Z | yes |
| 18 | `I_kwDOSWRi3c8AAAABDJFS5Q` | `1980705ce9748e771d6eaa3e8686fc80dd3abf7e86923b0d613a43fd7917097f` | `README.md` | 2026-07-19T11:13Z | yes |
| 20 | `I_kwDOSWRi3c8AAAABDJFTRQ` | `d3f25550dde98c6d1b726ca28673f1d45aaca1b9c683e9fc8f691f18d19a6251` | `docs/architecture/python-release-asset-index.md` | 2026-07-19T11:13Z | yes |
| 21 | `I_kwDOSWRi3c8AAAABDJFTgA` | `81420bbb78642fa6f4e7bb523a546d2a9ed2e5d2656c03c7c120b08ba3c2a3c4` | `docs/issues/2026-07-19-gh-021-resolve-gh-executable.md` | 2026-07-19T11:13Z | yes |

## Verification

After each batch, the former issue URL must stop resolving and the API must
report the issue absent. Results are recorded in the Verified absent column
above and pushed before the next batch begins.

## Related

- [Migration ledger](github-issue-migration-ledger.md)
- [Migration runbook](../runbooks/github-issues-to-docgraph-migration.md)

## Record validation on 2026-11-07

The 21 issue IDs and digests match the migration ledger and rename record.
Every destination path still exists. Git commits `b5a6858`, `095149d`, and
`6666daf` record the three completed deletion batches, and commit `3c9a4df`
contains the governed destinations. The deletion rows remain unchanged.
This check validates the local audit record; it does not repeat the historical
GitHub API checks or assert current organization settings.
