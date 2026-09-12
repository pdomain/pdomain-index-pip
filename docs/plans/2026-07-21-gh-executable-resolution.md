---
Status: active
Owner: CT
Created: 2026-07-21
Last verified: 2026-07-21
Kind: plan
---

# GitHub CLI Executable Resolution Implementation Plan

## Agent Index

- **Kind:** plan
- **Status:** active
- **Owner:** CT
- **Created:** 2026-07-21
- **Last verified:** 2026-07-21
- **Read when:** implementing the GitHub CLI executable-resolution issue.
- **Search terms:** gh executable, implementation plan, shutil.which, S607.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Resolve the GitHub CLI to an explicit path before index-regeneration subprocess calls.

**Architecture:** Keep resolution inside `gh_json()`, the generator's single GitHub CLI boundary. Test missing and successful resolution, then remove the obsolete Ruff `S607` exception.

**Tech Stack:** Python 3.12+, `shutil.which`, `subprocess`, pytest, Ruff, basedpyright

**Spec:** [Resolve the GitHub CLI before index regeneration](../specs/2026-07-21-gh-executable-resolution-design.md)

______________________________________________________________________

## Goal

Resolve `gh` before subprocess invocation and fail clearly when it is absent.

## Architecture

Keep resolution inside `gh_json()` and remove the obsolete `S607` exception.

## Tech Stack

Python 3.12+, pytest, Ruff, basedpyright, and `shutil.which`.

## Global Constraints

- Preserve argument-list execution with `shell=False`.
- Keep the repository-wide `S603` exception.
- Use make targets and run `make ci AI=1` before completion.

### Task 1: Specify and implement executable resolution

**Files:**

- Modify: `tests/test_regen_index.py`

- Modify: `scripts/regen_index.py`

- [ ] **Step 1: Write the failing missing-executable test**

Add after `test_repo_allowlist_uses_current_pdomain_names`:

```python
def test_gh_json_fails_clearly_when_gh_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(regen_index.shutil, "which", lambda _name: None)

    def unexpected_run(*_args: object, **_kwargs: object) -> None:
        pytest.fail("subprocess.run must not be called when gh is missing")

    monkeypatch.setattr(regen_index.subprocess, "run", unexpected_run)
    with pytest.raises(RuntimeError, match="^gh executable not found on PATH$"):
        _ = regen_index.gh_json(["api", "rate_limit"])
```

- [ ] **Step 2: Run the test and confirm the defect**

Run: `make test-single TEST='tests/test_regen_index.py::test_gh_json_fails_clearly_when_gh_is_missing' AI=1`

Expected: FAIL because the current helper starts `subprocess.run`.

- [ ] **Step 3: Write the failing resolved-path test**

```python
def test_gh_json_runs_the_resolved_gh_path(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(regen_index.shutil, "which", lambda name: f"/tools/{name}")
    observed: dict[str, object] = {}

    def fake_run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        observed["command"] = command
        observed["kwargs"] = kwargs
        return subprocess.CompletedProcess(command, 0, stdout='{"ok": true}')

    monkeypatch.setattr(regen_index.subprocess, "run", fake_run)
    assert regen_index.gh_json(["api", "rate_limit"]) == {"ok": True}
    assert observed == {
        "command": ["/tools/gh", "api", "rate_limit"],
        "kwargs": {"capture_output": True, "text": True, "check": True},
    }
```

- [ ] **Step 4: Run both tests**

Run: `make test-k K='gh_json' AI=1`

Expected: FAIL because argument zero is bare `gh`.

- [ ] **Step 5: Implement the minimal resolution**

Replace `gh_json()` with:

```python
def gh_json(args: Sequence[str]) -> object:
    """Run `gh` with --json output and parse. Raise on non-zero."""
    executable = shutil.which("gh")
    if executable is None:
        raise RuntimeError("gh executable not found on PATH")
    proc = subprocess.run([executable, *args], capture_output=True, text=True, check=True)
    return cast(object, json.loads(proc.stdout))
```

- [ ] **Step 6: Run the focused tests**

Run: `make test-k K='gh_json' AI=1`

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add scripts/regen_index.py tests/test_regen_index.py
git commit -m "fix: resolve gh before index regeneration"
```

### Task 2: Remove the obsolete Ruff exception

**Files:**

- Modify: `pyproject.toml`

- Modify: `docs/conventions/lint-deviations.md`

- [ ] **Step 1: Delete the `S607` exception**

Delete from `[tool.ruff.lint.per-file-ignores]`:

```toml
    # S607: regen_index intentionally resolves the trusted gh CLI from PATH.
    "S607",
```

- [ ] **Step 2: Delete the `S607` row from the catalogue**

Remove only the `S607` row from `docs/conventions/lint-deviations.md`. Keep `S603`.

- [ ] **Step 3: Run static checks**

Run: `make static-check AI=1`

Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add pyproject.toml docs/conventions/lint-deviations.md
git commit -m "chore: remove resolved partial-path exception"
```

### Task 3: Verify the repository gate

**Files:**

- Verify: `scripts/regen_index.py`

- Verify: `tests/test_regen_index.py`

- Verify: `pyproject.toml`

- Verify: `docs/conventions/lint-deviations.md`

- [ ] **Step 1: Run the full gate**

Run: `make ci AI=1`

Expected: PASS.

- [ ] **Step 2: Inspect the scoped diff**

Run: `git diff HEAD~2 -- scripts/regen_index.py tests/test_regen_index.py pyproject.toml docs/conventions/lint-deviations.md`

Expected: only executable resolution, two tests, and removal of the `S607` exception and row.
