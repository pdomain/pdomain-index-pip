# pdomain-index-pip

Self-hosted [PEP 503](https://peps.python.org/pep-0503/) simple Python package index for pdomain Python repos under [github.com/pdomain](https://github.com/pdomain).

Wheels themselves live as **GitHub Release assets** in each individual repo. This repo just publishes a static HTML index that hyperlinks to those release assets, so [`uv`](https://docs.astral.sh/uv/) / `pip` can resolve cross-repo pdomain dependencies without needing the names to exist on PyPI.

## URL

Once GitHub Pages is enabled on this repo, the index will be live at:

```
https://pdomain.github.io/pdomain-index-pip/simple/
```

## How consumers use it

Add `--extra-index-url https://pdomain.github.io/pdomain-index-pip/simple/` to whatever invocation installs a pdomain wheel. For example, the `pdomain-ocr-cli/install.sh` script can:

```sh
uv tool install --reinstall ./pdomain_ocr_cli-X.Y.Z-py3-none-any.whl \
    --extra-index-url https://pdomain.github.io/pdomain-index-pip/simple/
```

For a project's `pyproject.toml` (declarative form):

```toml
[[tool.uv.index]]
name = "pdomain-index-pip"
url = "https://pdomain.github.io/pdomain-index-pip/simple/"
explicit = false
```

## How it stays up to date

`.github/workflows/regen.yml` runs daily and on `workflow_dispatch` / `repository_dispatch`. It:

1. Calls `scripts/regen_index.py`, which uses the GitHub API (read-only, public, no PAT required) to enumerate every release asset across the configured pdomain repos.
1. Renders PEP 503 simple-index HTML into `_site/simple/`.
1. Deploys `_site/` via [`actions/deploy-pages`](https://github.com/actions/deploy-pages) — no commits are made to `main` from CI.

The generator only indexes distribution assets whose normalized package name
matches the generated simple-index project page. Historical `pd_*` assets in
renamed repos are intentionally skipped rather than published under the new
`pdomain-*` package names.

To trigger an immediate rebuild without waiting for cron, individual release workflows can dispatch a `pdomain-release-published` event to this repo (one HTTP call with a fine-grained PAT). The daily cron is the safety net.

## Repos covered

The list lives in `scripts/regen_index.py` (`REPOS`). Adding a new Python-distribution repo: append it there, push, and run `regen-and-deploy` manually if the daily cron is too slow.

## Why not just publish to PyPI?

Eventually we may. This index is a stepping stone: it speaks the same protocol PyPI does, so migrating later is a matter of `uv publish` + dropping the `--extra-index-url` flag. No wheel changes, no metadata changes.

The pdomain Python repos already follow a few habits to keep that door open:

- Plain version-pinned dep specifiers in `pyproject.toml` (no PEP 508 direct-URL deps that PyPI would reject).
- Release versions are immutable (no asset overwrites — PyPI rejects re-uploads of the same version).
- PEP 440-clean version strings.

## Local dry-run

```sh
gh auth status              # any GitHub auth is fine; only public reads
uv run python scripts/regen_index.py --out /tmp/pdomain-index-pip-out/simple
ls /tmp/pdomain-index-pip-out/simple/
```

## Development

```sh
make setup
make ci
make smoke-regen
```

Releases are repo-code releases only. Use `make release-patch`,
`make release-minor`, or `make release-major`; the script runs `make ci`,
pushes the exact tag, and dispatches `.github/workflows/release.yml`.
