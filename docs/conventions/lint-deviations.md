# Lint Deviations

This file records persistent lint and static-check deviations that remain in
repository configuration.

## Ruff

| Rule | Location | Justification |
| --- | --- | --- |
| `ANN401` | `pyproject.toml` | `scripts/regen_index.py` decodes JSON from the GitHub CLI. Keeping this as `object` plus typed casts is clearer than pretending the raw JSON boundary is statically typed. |
| `T201` for `scripts/*.py` | `pyproject.toml` | The index generator is a command-line maintenance script; stdout/stderr progress is its user interface. |
| `S603` and `S607` for `scripts/*.py` | `pyproject.toml` | `scripts/regen_index.py` invokes a fixed `gh` executable with an argument vector, not shell-expanded user input. Repository names come from the checked-in allowlist. |
| `S101` for `tests/**/*.py` | `pyproject.toml` | pytest assertions are the test idiom. |

## ShellCheck

| Rule | Location | Justification |
| --- | --- | --- |
| `SC2086` | `scripts/release-common.sh` | `RELEASE_VERSION_FILES` follows the shared pdomain release-common convention: a repo-local, space-delimited file list for `git add` when `RELEASE_VERSION_SOURCE=uv`. This repo uses tag-derived versions today, but keeps the shared helper behavior intact. |
