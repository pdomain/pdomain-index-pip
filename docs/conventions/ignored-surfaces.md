# Ignored Surfaces

This repository keeps generated artifacts and local tool state out of static
analysis and formatting checks.

## Generated index output

- `_site/`: local and CI static-site output for GitHub Pages artifact
  deployment. The source of truth is `scripts/regen_index.py` plus GitHub
  Release asset metadata.

## Local tool state

- `.venv/`: uv-managed development environment.
- `.pytest_cache/`: pytest cache.
- `.ruff_cache/`: ruff cache.
- `.basedpyright/`: basedpyright local state, if generated.
- `.ci-ai.log`: compact `make AI=1 ...` command log.
- `__pycache__/` and `*.pyc`: Python bytecode caches.

## Agent state

- `.claude/`: per-repo agent state is not source. Canonical memory belongs
  under the workspace-level `/workspaces/ocr-container/.claude/agent-memory/`.
