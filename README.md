<!--
Status: active
Owner: CT
Created: 2026-05-06
Last verified: 2026-07-14
Kind: usage
-->

# pdomain-index-pip

## Agent Index

- **Status:** active
- **Owner:** CT
- **Created:** 2026-05-06
- **Last verified:** 2026-07-14
- **Kind:** usage
- **Read when:** using, operating, or developing the package index.
- **Search terms:** pip index, uv index, release assets, local development.

Self-hosted [PEP 503](https://peps.python.org/pep-0503/) simple Python package index for pdomain Python repos under [github.com/pdomain](https://github.com/pdomain).

Wheels themselves live as **GitHub Release assets** in each individual repo. This repo just publishes a static HTML index that hyperlinks to those release assets, so [`uv`](https://docs.astral.sh/uv/) / `pip` can resolve cross-repo pdomain dependencies without needing the names to exist on PyPI.

## URL

Once GitHub Pages is enabled on this repo, the index will be live at:

```text
https://pdomain.github.io/pdomain-index-pip/simple/
```

## How consumers use it

For a one-off install, pin the pdomain distribution to its direct release-asset
URL. Copy the wheel link from the generated project page so its `#sha256=`
fragment is retained when GitHub provides a digest:

```sh
uv tool install \
    'pdomain-ocr-cli @ https://github.com/pdomain/pdomain-ocr-cli/releases/download/vX.Y.Z/pdomain_ocr_cli-X.Y.Z-py3-none-any.whl#sha256=<sha256>'
```

Configure authentication for the artifact host when the release is private;
do not put credentials in the recorded command. The direct requirement pins
the target distribution, while its public transitive dependencies still resolve
from PyPI.

For a project's `pyproject.toml`, make the index explicit and map each pdomain
distribution to it. This prevents fallback to a same-named public package:

```toml
[[tool.uv.index]]
name = "pdomain-index-pip"
url = "https://pdomain.github.io/pdomain-index-pip/simple/"
explicit = true

[tool.uv.sources]
pdomain-ops = { index = "pdomain-index-pip" }
pdomain-book-tools = { index = "pdomain-index-pip" }
```

An unrestricted `--index` or `--extra-index-url` one-off command is not a
package-to-source pin: if the private index has no matching project, resolution
can continue by package name on another index. See
[the private-index decision](docs/decisions/private-index-resolution.md) for
the full rationale. A direct local wheel path needs no index option.

## How it stays up to date

`.github/workflows/regen.yml` runs daily and on `workflow_dispatch` / `repository_dispatch`. It:

1. Calls `scripts/regen_index.py`, which uses the GitHub API (read-only, public, no PAT required) to enumerate every release asset across the configured pdomain repos.
1. Renders PEP 503 simple-index HTML into `_site/simple/`.
1. Deploys `_site/` via [`actions/deploy-pages`](https://github.com/actions/deploy-pages) — no commits are made to `master` from CI.

The generator only indexes distribution assets whose normalized package name
matches the generated simple-index project page. Historical `pd_*` assets in
renamed repos are intentionally skipped rather than published under the new
`pdomain-*` package names.

The complete trust boundary, fail-closed behavior, and digest handling are
documented in the
[release-asset index architecture](docs/architecture/python-release-asset-index.md).

To trigger an immediate rebuild without waiting for cron, individual release workflows can dispatch a `pdomain-release-published` event to this repo (one HTTP call with a fine-grained PAT). The daily cron is the safety net.

## Repos covered

The list lives in `scripts/regen_index.py` (`REPOS`). Adding a new Python-distribution repo: append it there, push, and run `regen-and-deploy` manually if the daily cron is too slow.

## Tooling Releases

This repo's own releases are tag-only tooling releases. Package versions indexed by
this repo come from publisher GitHub Release assets, not this repo's metadata version.
GitHub-generated release notes are canonical for tooling releases.

## Why not just publish to PyPI?

Eventually we may. This index is a stepping stone: it speaks the same protocol
PyPI does, so migration means publishing with `uv publish`, removing each
package's `[tool.uv.sources]` mapping, and replacing direct artifact requirements
with normal PyPI package requirements. No wheel or package metadata changes are
required.

The pdomain Python repos already follow a few habits to keep that door open:

- Plain version-pinned dep specifiers in `pyproject.toml` (no PEP 508 direct-URL deps that PyPI would reject).
- A PyPI migration must use a new version for every changed distribution because
  PyPI rejects re-uploads of the same version.
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

Repository contributors and assistants start with [AGENTS.md](AGENTS.md).
