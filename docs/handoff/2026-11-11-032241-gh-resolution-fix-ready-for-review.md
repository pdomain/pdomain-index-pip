---
kind: handoff
status: "active"
created: "2026-11-11"
created_at: "2026-11-11T03:22:38Z"
owner: "CT"
branch: "worktree-fix-gh-executable-resolution"
scope: "gh-executable-resolution"
worktree: "/mnt/work/projects/pdomain/pdomain-index-pip/.claude/worktrees/fix-gh-executable-resolution"
base_commit: "efbe9c8486118f7a302123eea7aab05f89e40636"
supersedes: ""
handoff_reason: "user_requested"
host: "claude-code"
---

# gh resolution fix ready for review

## Goal

Resolve `gh` to an absolute path before `scripts/regen_index.py` starts it, and fail clearly when it is missing.

## Done

- `scripts/regen_index.py` resolves `gh` first and fails with `gh executable not found on PATH` (`65c9a6f`).
- The S607 exception and its catalogue row are removed (`18e8079`). The issue, plan and spec are retired (`6fc197f`, `efbe9c8`).
- `make ci AI=1` passed with 20 tests and the strict docgraph check reports no issues. With no `gh` on PATH the script exits 1 and writes no output. One independent review ran.

## Not done

- The branch is not merged and no publish ran.
- The readability pass did not run, because it rewrites whole files and `decisions.md` is append-only. New text was written to the standard by hand.

## Failed approaches

- The plan's test code failed the type and lint checks. The tests were rewritten with direct imports, typed fakes and a raw match pattern. The tombstone records the change.

## Decisions

- PATH still chooses which `gh` runs, so the fix does not protect against a compromised PATH. The spec excluded that on purpose.

## State

Worktree clean. The owner paused this work on 2026-11-10 and the session's herdr tab is closed. Nothing was pushed, merged, tagged, released or deployed. All work ran on CPU with the GPU hidden. The session's last terminal output is saved in `/mnt/work/projects/pdomain/.artifacts/handoff-20261110/session-output/`. `/tmp` is a shared tmpfs that ran out of quota several times on 2026-11-10 while ten sessions ran gates. If a gate fails with a quota error, point `TMPDIR` at the work drive and rerun before suspecting the code.

## Pointers

- `docs/roadmap.md`
- `docs/context/decisions.md`
- `docs/architecture/python-release-asset-index.md`

## Resume steps

1. Review `git log master..HEAD`.
2. Merge when the owner asks.
