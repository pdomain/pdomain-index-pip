---
Status: active
Owner: CT
Created: 2026-07-13
Last verified: 2026-11-12
Kind: architecture
---

# Python release-asset index

## Agent Index

- **Status:** active
- **Owner:** CT
- **Created:** 2026-07-13
- **Last verified:** 2026-11-12
- **Kind:** architecture

The index is a generated PEP 503 view over Python distributions attached to
allowlisted pdomain GitHub Releases.

GitHub Pages stores only HTML. Package bytes remain in each publisher
repository.

## Trust boundary

`scripts/regen_index.py` is the only writer. It enumerates a fixed repository
allowlist. It accepts assets only when all of these conditions hold:

- the filename is a wheel, source archive, or zip distribution;
- the normalized distribution name matches the allowlisted repository page;
- the URL is HTTPS on `github.com` under that repository's release-download
  path; and
- the decoded path does not traverse above that boundary.

The generator skips wrong-project, non-distribution, and unsafe assets.

The generator sorts releases by `published_at` ascending. An empty date sorts
first.

When two assets share a filename, the generator keeps the first and skips the
later duplicate.

The generator omits draft releases and releases with no `tagName`. It indexes
prereleases.

A successful run still replaces the output tree.

A missing allowlisted repository, a disappearing release, or a GitHub API
failure stops regeneration. So `scripts/publish-index.sh` does not replace the
previous Pages deployment with an incomplete index.

Fetch failures fail closed by design. `is_repo_not_found_error` matches only a
not-found response and converts it to a named `RuntimeError`. Every other
`CalledProcessError` is re-raised unchanged. Transient authentication, rate
limit, and network failures therefore abort the run rather than silently
dropping a release's files from the published index.

Enumeration also aborts when a repository reaches `RELEASE_LIMIT`, so
pagination must be raised before a truncated index can be published.

## Allowlist

`REPOS` in `scripts/regen_index.py` is the fixed list. The organization is
`pdomain`. A repository that is not on the list is never indexed. A listed
repository with no releases is allowed.

Each listed repository gets one project page. The page name is the normalized
repository name. An asset is linked only when the distribution name in its
filename normalizes to that same page. The generator does not rename files. A
historical `pd_*` asset in a renamed repository is skipped.

## GitHub CLI invocation

`gh_json()` in `scripts/regen_index.py` starts `gh` by bare name, with
`shell=False` and a fixed argument list. The process `PATH` chooses the
binary. A missing `gh` shows up as a subprocess failure.

An absolute path and a dedicated missing-tool error are still open on the
[roadmap](../roadmap.md#still-to-do-in-this-repository).

## Integrity metadata

When GitHub supplies a `sha256:` digest, the generated link includes a PEP 503
`#sha256=` fragment copied from that string. The generator does not hash the
asset.

Assets with any other digest, or with none, stay installable and have no
fragment.

## Consumer resolution boundary

The generated project page is both an index endpoint and a source of direct
artifact links.

One-off installs use the selected wheel or sdist URL as a direct package
requirement. Keep the `#sha256=` fragment when the link has one. Authenticate
to the artifact host when required. This pins the pdomain distribution without
replacing PyPI for public transitive dependencies.

Repeatable project configuration declares this index with `explicit = true` and
maps each pdomain distribution through `[tool.uv.sources]`.

Passing the index as an unrestricted one-off `--index` does not establish the
same package-to-source binding. A missing project can fall through to another
index by package name.

## Publication flow

A maintainer publishes the index from a local checkout.
`scripts/publish-index.sh` runs `make regen`. It writes a short landing page
and `.nojekyll`, then commits that tree to the `gh-pages` branch. GitHub Pages
serves the branch.

`DRY_RUN=1` builds the tree and does not commit or push.

If the tree is unchanged, the script exits before any diff. When the tree has
changed, the script prints at most 20 lines of `git diff --cached --stat`.
Under `DRY_RUN=1` it then exits. A normal run commits that tree and pushes it
to `gh-pages`.

No workflow in this repository publishes the index. Commit `4a91b14` on
2026-09-13 removed the GitHub Actions workflows for CI, dep-refresh, release,
and index regeneration. A release stays invisible to installers until someone
runs `./scripts/publish-index.sh`.

The script needs `GH_TOKEN`, or a signed-in `gh` session. When `GH_TOKEN` is
unset, the script runs `gh auth token` and exports the result. That token must
be able to read the allowlisted repositories' releases. The push to `gh-pages`
also needs Git push access to this repository.

GitHub Pages must serve the `gh-pages` branch directly. The script writes
`.nojekyll` so Pages does not run Jekyll on that branch. It builds in a
temporary directory. It does not publish the local `_site` tree.

## Tooling releases

This repository publishes the index. It does not publish a Python distribution
of its own.

`scripts/do-release.sh` sets `RELEASE_REPO` to `pdomain/pdomain-index-pip`,
`RELEASE_BUILD` to `:`, and `RELEASE_PREFLIGHT` to `make ci`. It then runs
`scripts/release-common.sh`.

`make release-patch`, `make release-minor`, and `make release-major` call that
script. The next version comes from existing `vN.N.N` git tags.
`RELEASE_BUILD=":"` skips the build. The GitHub Release is the tag alone,
unless files are already present under `dist/`. The helper attaches matching
`.whl`, `.tar.gz`, and `.tgz` files when they are there. GitHub-generated
release notes are the notes for these tooling releases.

A tooling release does not regenerate the index and does not push `gh-pages`.
Package versions that installers see come from the publisher repositories'
release assets.

`scripts/release-common.sh` is a vendored copy of the shared pdomain release
driver. This repository uses tag-derived versions, so the space-delimited
`RELEASE_VERSION_FILES` list is not on the path it uses today. The helper
still contains that contract. Whether to replace it is on the
[roadmap](../roadmap.md#consider-in-another-repository).

## Evidence

- Code: `scripts/regen_index.py`, `scripts/publish-index.sh`
- Tests: `tests/test_regen_index.py` — 18 passed on 2026-11-06
  (`test_repo_allowlist_uses_current_pdomain_names`,
  `test_asset_download_url_is_limited_to_repo_release_downloads`,
  `test_distribution_name_from_asset`,
  `test_render_project_page_skips_duplicate_non_dist_unsafe_and_wrong_project_assets`,
  `test_render_project_page_includes_sha256_fragment_when_digest_present`,
  `test_render_project_page_no_fragment_when_digest_absent`,
  `test_render_project_page_no_fragment_when_digest_not_sha256`,
  `test_fetch_releases_fails_for_configured_repo_not_found`,
  `test_fetch_releases_fails_at_release_limit`,
  `test_main_writes_simple_index_with_mocked_release_fetch`,
  `test_main_replaces_existing_output_tree`)
- Fail-closed handling: `scripts/regen_index.py:86-88,123-126,130-133,153-156`
- Integrity fragments: `scripts/regen_index.py:223-225`
- Bare `gh` invocation: `scripts/regen_index.py:80-83`
- Publish path: `scripts/publish-index.sh`. Workflows removed in commit
  `4a91b14` (2026-09-13).
- Allowlist and name match: `scripts/regen_index.py` (`REPOS`,
  `distribution_name_from_asset`, the project-name check in
  `render_project_page`)
- Publish authentication and `.nojekyll`: `scripts/publish-index.sh`
- Tooling release: `scripts/do-release.sh`, `scripts/release-common.sh`
  (`RELEASE_BUILD`)
- Verified: 2026-11-06 with `uv run pytest tests/test_regen_index.py`
  (18 passed) and a read of the generator and publish script.
- Verified: 2026-11-12 by reading `scripts/regen_index.py`,
  `scripts/publish-index.sh`, `scripts/do-release.sh`, and
  `scripts/release-common.sh`.

## Provenance

Four migrated GitHub issues are represented above rather than in
`docs/issues/`, because each was already implemented when the issue tracker was
migrated on 2026-07-19:

| Issue | Behavior | Section |
| --- | --- | --- |
| #16 | Explicit index and per-package source mapping | Consumer resolution boundary |
| #17 | Fail-closed on unexpected fetch failures | Trust boundary |
| #19 | PEP 503 `#sha256=` fragments | Integrity metadata |
| #20 | Generator test coverage | Evidence |

Full provenance, including node IDs and raw digests, is in the
[migration ledger](../context/github-issue-migration-ledger.md).
