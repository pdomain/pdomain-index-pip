---
Status: active
Owner: CT
Created: 2026-07-19
Last verified: 2026-11-07
Kind: issue
Level: I1
---

# The gh executable is resolved through PATH at subprocess invocation

## Agent Index

- **Kind:** issue
- **Status:** active
- **Level:** I1
- **Last verified:** 2026-11-07
- **Resolution:** Open
- **Severity:** Low - implicit executable resolution and unclear missing-tool failure
- **Affected version:** `scripts/regen_index.py` at commit `e2244e1`
- **Read when:** hardening `scripts/regen_index.py` subprocess calls, or
  responding to bandit B404/B603/B607 findings.
- **Search terms:** gh executable, PATH hijacking, shutil.which, subprocess,
  bandit B607, regen_index.
- **Relates to:**
  [release-asset index architecture](../architecture/python-release-asset-index.md)

## Summary

`gh_json()` invokes `gh` by bare name, so the executable is resolved through
`PATH` at call time. The planned change makes the executable path explicit and
adds a clear missing-tool error. It does not establish trust in a binary found
on a compromised `PATH`. Filed from the deep review and security
scan report `reports/security-review-2026-05-22/pd-index-pip.md`, and confirmed
still present in `scripts/regen_index.py` on 2026-11-07.

## Impact

- Anyone running `scripts/regen_index.py` in an environment where `PATH` can be
  influenced.
- Severity is low. The call passes `shell=False` with static, internal
  arguments, so command injection is not the concern. The residual risk is that
  a compromised `PATH` supplies a different `gh` binary.

## Environment / versions

Applies to local `make regen` and `scripts/publish-index.sh`, which calls it.
The GitHub Actions workflows were removed in commit `4a91b14`. The project
declares Python `>=3.12`; the defect is independent of Python version.

## Evidence

Observations, verified 2026-11-07 against current source:

- `scripts/regen_index.py:82` calls
  `subprocess.run(["gh", *args], capture_output=True, text=True, check=True)`.
- `scripts/regen_index.py:17` imports `shutil`, but only for `shutil.rmtree` at
  lines 292 and 299. Nothing in this module resolves an executable.
- Commit `23ffe01` removed `scripts/update_github_actions.py`, which the
  original issue cited as a `shutil.which` example.
- `tests/test_regen_index.py` has no test for `gh_json()` executable resolution
  or its missing-tool failure.

The original report cited bandit `B404` at `scripts/regen_index.py:17`, and
`B607` and `B603` at `scripts/regen_index.py:47-49`. Line numbers have shifted
since filing; the current call site is line 82.

## Root-cause hypotheses

1. The helper still relies on subprocess executable lookup. Its exact
   missing-tool behavior is not covered by a focused test. The source shows
   that no explicit resolution or named missing-tool error has been added.

## Defects to fix

1. `gh_json()` in `scripts/regen_index.py` passes an unresolved executable name
   to `subprocess.run`.
1. There is no explicit, clear failure when `gh` is absent from `PATH`.

## Next steps

1. Resolve `gh` with `shutil.which("gh")` and fail with a clear error when it
   returns `None`.
1. Pass the resolved absolute path to `subprocess.run`, keeping `shell=False`.
1. Follow the [executable-resolution plan](../plans/2026-07-21-gh-executable-resolution.md).
1. Add a test covering the missing-`gh` failure path.

## Resolution

Open.

## Provenance

Migrated from GitHub issue #21.

- **Node ID:** `I_kwDOSWRi3c8AAAABDJFTgA`
- **URL:** `https://github.com/pdomain/pdomain-index-pip/issues/21`
- **State:** OPEN
- **Author:** ConcaveTrillion
- **Created:** 2026-05-22
- **Labels:** `kind:chore`, `effort:S`, `model:sonnet`, `model-effort:low`,
  `status:backlog`
- **Milestone:** none
- **Comments:** none
- **Raw digest (SHA-256):**
  `81420bbb78642fa6f4e7bb523a546d2a9ed2e5d2656c03c7c120b08ba3c2a3c4`

## Related

- [Migration ledger](../context/github-issue-migration-ledger.md)
- [Migration runbook](../runbooks/github-issues-to-docgraph-migration.md)
