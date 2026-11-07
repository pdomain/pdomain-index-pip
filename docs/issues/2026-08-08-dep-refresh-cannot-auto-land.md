---
Status: active
Owner: CT
Created: 2026-08-08
Last verified: 2026-11-07
Kind: issue
Level: I1
---

# Weekly dep-refresh cannot fully auto-land: branches accumulate and are never deleted

## Agent Index

- **Kind:** issue
- **Status:** active
- **Level:** I1
- **Last verified:** 2026-11-07
- **Resolution:** Open
- **Severity:** Low - branch-list noise only; dependency updates are landing
- **Affected version:** `.github/workflows/dep-refresh.yml` at commit `d0c2cc6`
- **Read when:** hardening `dep-refresh.yml`, changing repo merge settings, or
  investigating stray `dep-refresh/*` branches.
- **Search terms:** dep-refresh, stray branches, delete_branch_on_merge,
  auto-merge, branch accumulation, dated branch name.
- **Relates to:** pdomain-ui `docs/specs/2026-07-16-dep-refresh-auto-land-design.md`
  (different repository, cited as the authority for the fix; read-only here).

## Summary

Local verification on 2026-11-07: commit `4a91b14` removed
`.github/workflows/dep-refresh.yml` and the other workflows on 2026-09-13.
The scheduled branch producer no longer exists in this checkout. Remote
branch counts, protection, and `delete_branch_on_merge` were not rechecked.
The owner still needs to decide whether any cleanup or settings change is
wanted. The observations below describe the 2026-08-08 snapshot, not current
GitHub state.

**The weekly `dep-refresh` workflow opens a new dated branch every run and
never deletes it, so branches accumulate.** As of 2026-08-08 there are 7 stray
`dep-refresh/*` branches on `origin` and 0 open pull requests. Dependency
updates are landing: the three most recent scheduled runs (2026-07-19,
2026-07-26, 2026-08-02) each opened a PR that auto-merged cleanly. The defect
is that neither a merged nor an abandoned run's branch is ever cleaned up, so
the branch list grows without bound.

This repository does **not** have the broken-required-context defect that
`pdomain-ops` and `pdomain-ocr-training` have. Branch protection on `master`
requires exactly two contexts, `static-check` and `test`
(`gh api repos/pdomain/pdomain-index-pip/branches/master/protection --jq '.required_status_checks.contexts'` → `["static-check","test"]`), and
`.github/workflows/ci.yml` defines jobs named exactly `static-check` and
`test` that report those contexts (`app_id: 15368` on both, not `null`). The
required contexts are satisfiable, and current evidence shows they are being
satisfied.

## Impact

- Anyone browsing branches on `pdomain/pdomain-index-pip` sees 7 stale
  `dep-refresh/*` branches with no open PR behind them.
- No functional impact on dependency landing: the auto-merge path works when
  the branch protection gate is satisfiable, and the last three scheduled
  runs merged without human action.
- A milder failure than peers where refresh PRs also pile up **open** and
  unmerged (that is the `pdomain-ops` / `pdomain-ocr-training` pattern, caused
  by a required context that can never be satisfied). Here the pile-up is
  branches only, not open PRs — confirmed by `gh pr list --repo pdomain/pdomain-index-pip --state all --limit 20` returning 0 rows with
  `state: OPEN`.

## Environment / versions

- Workflow: `.github/workflows/dep-refresh.yml`, current at commit `d0c2cc6`
  (`git log --oneline -- .github/workflows/dep-refresh.yml`).
- Repository setting: `delete_branch_on_merge: false`
  (`gh api repos/pdomain/pdomain-index-pip --jq '{delete_branch_on_merge, default_branch}'` → `{"default_branch":"master", "delete_branch_on_merge":false}`).
- Branch protection: `master` requires `["static-check","test"]`, both with
  non-null `app_id: 15368` (`gh api repos/pdomain/pdomain-index-pip/branches/master/protection --jq '.required_status_checks'`).
- CI: `.github/workflows/ci.yml` defines jobs `static-check` (line 15) and
  `test` (line 25) — the exact names branch protection requires.

## Evidence

Observations, verified 2026-08-08 against current source and the GitHub API:

- `.github/workflows/dep-refresh.yml` builds a per-run dated branch name:
  `BRANCH="dep-refresh/$(date +%Y-%m-%d)-$GITHUB_RUN_ID"`, then always runs
  `git checkout -b "$BRANCH"` and `gh pr create ... --head "$BRANCH"`
  unconditionally — there is no check for an existing open PR before creating
  a new branch.
- `gh api repos/pdomain/pdomain-index-pip/branches?per_page=100 --jq '.[].name'` lists 7 `dep-refresh/*` branches plus `master`:
  `dep-refresh/2026-06-21-27896611011`, `dep-refresh/2026-06-28-28313829985`,
  `dep-refresh/2026-07-05-28731654495`, `dep-refresh/2026-07-12-29181398267`,
  `dep-refresh/2026-07-19-29674926200`, `dep-refresh/2026-07-26-30189720964`,
  `dep-refresh/2026-08-02-30734360326`.
- `gh pr list --repo pdomain/pdomain-index-pip --state all --limit 20` shows 7
  `chore: weekly dep refresh` pull requests (#22–#28), 0 currently open:
  - #26, #27, #28 (weeks of 2026-07-19, 2026-07-26, 2026-08-02): `MERGED`.
    Their branches remain on `origin` only because `delete_branch_on_merge`
    is `false` — auto-merge itself worked.
  - #22, #23, #24, #25 (weeks of 2026-06-21 through 2026-07-12): `CLOSED`
    with `mergedAt: null`, all closed within the same minute
    (`2026-07-12T10:09:50–51Z`, confirmed via `gh pr view <n> --json state, mergedAt,closedAt`) — a manual batch-close, not an auto-merge. This
    timestamp coincides with the batch-close event the cited pdomain-ui spec
    describes for its own four stuck PRs (`#57`–`#60`, closed
    2026-07-12), consistent with the same red-week cleanup sweep touching
    multiple repos rather than a defect specific to this repo's required
    checks.
- No corresponding defect exists here for what closed #22–#25: this repo's
  required contexts (`static-check`, `test`) are real, reporting checks (see
  Environment / versions), unlike `pdomain-ui`'s `unit-test` context, which
  had `app_id: null` and could never be satisfied. #22–#25 were most likely
  genuinely red dependency-bump weeks with nothing to auto-clean them up, the
  same "Bug 2" failure mode the cited spec describes — not the "Bug 1"
  broken-context failure mode.

## Root-cause hypotheses

1. `dep-refresh.yml` derives its branch name from the run date and run ID
   (`dep-refresh/$(date +%Y-%m-%d)-$GITHUB_RUN_ID`), so every scheduled run
   creates a brand-new branch instead of reusing one. Confirmed directly from
   the workflow source — no runtime investigation needed.
1. `delete_branch_on_merge` is `false` at the repository level, so even a
   fully successful, auto-merged run leaves its branch behind. Confirmed via
   the GitHub API repo-settings call above.
1. The workflow never checks for an existing open PR before creating a new
   branch/PR, so a red week has no way to be reused by the following week's
   run — each red (or manually closed) week's branch is permanent dead
   weight. Confirmed by reading the "Create branch, commit, and open PR" step,
   which runs unconditionally on `steps.changes.outputs.changed == 'true'`
   with no existing-PR lookup.

## Defects to fix

1. `dep-refresh.yml` names its branch `dep-refresh/<date>-<run-id>`, so no run
   ever reuses a previous run's branch.
1. `delete_branch_on_merge` is `false` on `pdomain/pdomain-index-pip`, so
   merged `dep-refresh` branches are never cleaned up automatically.
1. `dep-refresh.yml` does not check for an existing open PR before creating a
   new branch and PR, so a red week's branch/PR is abandoned rather than
   reused by the next run.

## Next steps

First decide whether the remaining remote-branch cleanup or repository setting
still needs action. Verify live branch and merge settings before proposing
changes. Do not recreate the deleted workflow to apply the old prescription.

The original proposal below applies only if dependency-refresh automation is
deliberately restored:

The pdomain-ui spec at `docs/specs/2026-07-16-dep-refresh-auto-land-design.md`
(in the `pdomain-ui` repository, read-only from here) is the design authority
for this fix. Its Design section B and C apply directly to this repo:

1. Replace the dated branch name with one reusable `dep-refresh` branch,
   force-pushed from a fresh `master` on every run (spec Design B).
1. Open a pull request only when no open PR already exists for that branch,
   then re-arm `gh pr merge --auto --rebase` (spec Design B).
1. Set `delete_branch_on_merge: true` on `pdomain/pdomain-index-pip` (spec
   Design C).
1. Note the scope difference from the spec's home repo: this repo does not
   need the spec's Design A (`ci.yml` `unit-test` aggregation job) — its
   required contexts already report correctly. For this repo, enabling
   delete-on-merge alone (step 3) would resolve the currently observed
   symptom (7 stray branches); the reusable-branch change (steps 1–2) is the
   structural fix that also prevents a run of red weeks from piling up
   branches the way #22–#25 did on 2026-07-12.

## Resolution

Open for owner disposition after workflow removal. The local code review did
not verify or authorize deletion of any remote branch or a settings change.
