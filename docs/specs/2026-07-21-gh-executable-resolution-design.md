---
Status: active
Owner: CT
Created: 2026-07-21
Last verified: 2026-07-21
Kind: spec
---

# Resolve the GitHub CLI before index regeneration

## Agent Index

- **Kind:** spec
- **Status:** active
- **Owner:** CT
- **Created:** 2026-07-21
- **Last verified:** 2026-07-21
- **Read when:** implementing or reviewing GitHub CLI invocation in the index generator.
- **Search terms:** gh executable, shutil.which, subprocess, PATH, index regeneration.
- **Relates to:** [active issue](../issues/2026-07-19-gh-021-resolve-gh-executable.md)
- **Implementation plan:** [GitHub CLI executable resolution](../plans/2026-07-21-gh-executable-resolution.md)

## The generator will resolve `gh` before every invocation

`gh_json()` will call `shutil.which("gh")` before it starts a subprocess and pass the returned path as argument zero. This follows `scripts/update_github_actions.py`.

The helper will raise `RuntimeError("gh executable not found on PATH")` when resolution fails. The failure occurs before subprocess creation.

## The change stays inside the existing helper

No new abstraction is needed. `gh_json()` is the only GitHub CLI boundary in `scripts/regen_index.py`, and `shutil` is already imported. The argument list, JSON parsing, `check=True`, and `shell=False` behavior stay unchanged.

This work does not validate the executable's contents or defend an already compromised executable directory.

## Tests prove failure and invocation behavior

Focused tests will prove that a missing executable raises the exact error without starting a subprocess. A second test will prove that the resolved path becomes argument zero while all subprocess options stay unchanged.

The obsolete Ruff `S607` exception and its suppression-catalog row will be removed. The repository-wide `S603` exception remains.

## Acceptance criteria

1. `gh_json()` never passes bare `gh` to `subprocess.run`.
1. Missing `gh` fails with `gh executable not found on PATH`.
1. Tests cover missing and resolved executables.
1. `make ci AI=1` passes.

## Adversarial Review

The design rejects shell invocation, binary-content attestation, and a shared
resolver abstraction. Tests must prove both the missing-tool failure and the
exact argument vector, because either omission would leave the issue partly open.
