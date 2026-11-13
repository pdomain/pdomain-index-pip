<!--
Status: active
Owner: CT
Created: 2026-05-30
Last verified: 2026-11-07
Kind: process
-->

# Ignored Surfaces

## Agent Index

- **Status:** active
- **Owner:** CT
- **Created:** 2026-05-30
- **Last verified:** 2026-11-07
- **Kind:** process
- **Read when:** changing ignore rules, cleanup targets, or static-analysis scope.
- **Search terms:** ignored surfaces, generated output, local caches, agent state.

This repository keeps generated artifacts and local tool state out of version
control. Tool input scopes and cleanup targets independently cover the relevant
surfaces.

## Generated index output

- `_site/`: default local generator output. The source of truth is
  `scripts/regen_index.py` plus GitHub Release asset metadata. The local
  `scripts/publish-index.sh` builds in a temporary directory and pushes the
  generated site to `gh-pages`; it does not upload a workflow artifact.

## Local tool state

- `.venv/`: uv-managed development environment.
- `.pytest_cache/`: pytest cache.
- `.ruff_cache/`: ruff cache.
- `.basedpyright/`: basedpyright local state, if generated.
- `.ci-ai.log`: full `AI=1 just ...` command log.
- `.docgraph/`: local docgraph index state, excluded from docgraph's own input
  scope; `docgraph.toml` is the tracked configuration.
- `__pycache__/` and `*.pyc`: Python bytecode caches.

## Agent state

- `.claude/`: per-repo agent state is not repository source. Durable project
  context belongs in the tracked `docs/context/` files.
- `.codex/`: generated agent configuration is workspace state, excluded by
  `.gitignore` alongside `.claude/`.
