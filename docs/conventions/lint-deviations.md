<!--
Status: active
Owner: CT
Created: 2026-05-30
Last verified: 2026-11-07
Kind: process
-->

# Lint Deviations

## Agent Index

- **Status:** active
- **Owner:** CT
- **Created:** 2026-05-30
- **Last verified:** 2026-11-07
- **Kind:** process
- **Read when:** adding, removing, or auditing lint and type suppressions.
- **Search terms:** Ruff ignore, ShellCheck disable, pyright suppression, lint audit.

This file records persistent lint and static-check deviations that remain in
repository configuration.

## Ruff

| Rule | Location | Justification |
| --- | --- | --- |
| `T201` for `scripts/*.py` | `pyproject.toml` | The maintenance scripts use stdout for their command-line progress and results. |
| `S603` for `scripts/*.py` | `pyproject.toml` | `regen_index.py` invokes `gh` with argument lists constructed from the checked-in allowlist and returned release tags. The call uses no shell expansion. |
| `S607` for `scripts/*.py` | `pyproject.toml` | `regen_index.py` passes bare `gh` to `subprocess.run`, which resolves it through `PATH`. Repository names come from the checked-in allowlist. Explicit executable resolution remains open work. |
| `S101` for `tests/**/*.py` | `pyproject.toml` | pytest assertions are the test idiom. |

## ShellCheck

| Rule | Location | Justification |
| --- | --- | --- |
| `SC2086` | `scripts/release-common.sh` | Intentional word splitting implements a trusted-maintainer contract: `RELEASE_VERSION_FILES` must be a space-delimited list of paths with no spaces. The helper does not validate that environment value. This repo uses tag-derived versions today but keeps the shared behavior intact. |
| `SC2086` | `scripts/release-common.sh` | The `gh release create` call intentionally splits the list of existing `dist/*.whl`, `dist/*.tar.gz`, and `dist/*.tgz` assets. The list assumes artifact paths contain no spaces; the helper does not validate that assumption. |
