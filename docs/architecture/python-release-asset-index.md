---
Status: active
Owner: CT
Created: 2026-07-13
Last verified: 2026-11-13
Kind: architecture
---

# Python release-asset index

## Agent Index

- **Status:** active
- **Owner:** CT
- **Created:** 2026-07-13
- **Last verified:** 2026-11-13
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

## Output replacement and permissions

The generator writes every project page and the root page into a UUID-named
sibling of the requested output directory. Fetch or rendering failures remove
that staging directory and leave the previous output tree in place.

After generation succeeds, it removes the previous output and renames the
staging directory into place. This replacement is not atomic: removal happens
before the rename.

The staging directory uses mode `0777` subject to the process umask. A setgid
parent passes its group behavior down. This avoids the owner-only `0700`
mode of `mkdtemp`, which would survive a rename and prevent other users from
reading the published tree.

## Allowlist

`REPOS` in `scripts/regen_index.py` is the fixed list. The organization is
`pdomain`. A repository that is not on the list is never indexed. A listed
repository with no releases is allowed.

The allowlist includes `pdomain-source-data` and
`pdomain-pgdp-api-client`. Their distribution names normalize to those
same project pages, so correctly named wheels and sdists need no special
matching rule.

Each listed repository gets one project page. The page name is the normalized
repository name. An asset is linked only when the distribution name in its
filename normalizes to that same page. The generator does not rename files. A
historical `pd_*` asset in a renamed repository is skipped.

## GitHub CLI invocation

`gh_json()` in `scripts/regen_index.py` resolves `gh` with `shutil.which("gh")`
before it starts a subprocess. It passes the returned path as argument zero,
with `shell=False` and a fixed argument list.

When `gh` is not on `PATH`, `gh_json()` raises
`RuntimeError("gh executable not found on PATH")` and starts no subprocess.
Regeneration stops and leaves the previous output in place.

`PATH` still chooses the binary. The generator does not check the binary's
contents, so a compromised `PATH` directory can still supply a different `gh`.

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

## Private release assets

The index contains HTML metadata, not package bytes. Public Pages can reveal
repository and package names, versions, filenames, download URLs, and supplied
digests. A link to a private GitHub asset does not grant access to its bytes.
No credential is embedded in the generated HTML.

The builder's `gh` identity must be able to read every private repository
on the allowlist. Missing access fails regeneration rather than publishing a
partial index. Both newly allowlisted package repositories are private.

The generator invokes the resolved `gh` executable, so it does not inherit
an account-selecting shell function. Supply an authorized `GH_TOKEN` when
the executable's active login lacks access. A successful interactive shell
query alone does not prove the generator has the same credentials.

`scripts/publish-index.sh` preserves a supplied `GH_TOKEN`. If it is unset,
the script obtains `gh auth token`, which uses the active CLI login. That
login must have the required private-repository access. Select a token for
the authorized account explicitly when several accounts are configured;
do not change global account state or embed credentials in URLs or HTML.

A signed-in `gh` session does not authenticate a separate `uv` or `pip`
HTTP request. Direct private browser-download URL installation has not been
verified here. Configure and verify artifact-host authentication separately,
or download an exact release asset through authenticated `gh` and install
the local wheel.

For that fallback, select a fixed published tag and its exact wheel filename.
Use a fresh directory and compare the file's SHA-256 with the publisher's
recorded digest when one is supplied. The example below selects an asset
with a recorded SHA-256 and refuses installation if it does not match. Replace
the version, expected digest, and target-environment placeholders:

```sh
release_tag='vX.Y.Z'
wheel='pdomain_source_data-X.Y.Z-py3-none-any.whl'
expected_sha256='REPLACE_WITH_PUBLISHER_SHA256'
download_dir="$(mktemp -d)"
gh release view "$release_tag" --repo pdomain/pdomain-source-data --json assets
gh release download "$release_tag" --repo pdomain/pdomain-source-data \
    --pattern "$wheel" --dir "$download_dir"
printf '%s  %s\n' "$expected_sha256" "$download_dir/$wheel" |
    sha256sum --check --status &&
    uv pip install --python /path/to/venv/bin/python "$download_dir/$wheel"
```

The generator still lists assets without digests; it does not invent hashes.
The example selects the top-level wheel only. Supply any required private
dependencies as additional verified local wheel arguments in this install
command. Downloading one wheel does not authenticate its dependencies. Public
transitive dependencies can still resolve from PyPI. Project installs can use
separately verified explicit per-package source bindings with project commands.

For the API client, use `--repo pdomain/pdomain-pgdp-api-client` and its
published `pdomain_pgdp_api_client` wheel name. Respect each package's
Python range and dependency pins. No private assets were downloaded or installed
during the documentation migration because these two releases had no assets
when checked on 2026-11-13.

GitHub documents the authenticated
[release-asset endpoint](https://docs.github.com/en/rest/releases/assets#get-a-release-asset).
The CLI provides
[`gh release download`](https://cli.github.com/manual/gh_release_download).
uv documents [HTTP credential sources](https://docs.astral.sh/uv/concepts/authentication/http/)
separately from its [local package install support](https://docs.astral.sh/uv/pip/packages/).

## Publication flow

A maintainer publishes the index from a local checkout.
`scripts/publish-index.sh` runs `just regen`. It writes a short landing page
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

## Local task runner

The repository owns its `justfile`; it imports no taskfile from a sibling.
The default recipe is `ci`. There is no Makefile.

`setup` installs the development lock with `uv sync --locked --group dev`.
Hook installation skips linked worktrees and a checkout with `core.hooksPath`
set. Other checkouts reinstall pre-commit and commit-message hooks.

CI runs setup, pre-commit, read-only Ruff checks, basedpyright, actionlint,
ShellCheck, Markdown formatting checks, pytest, and index regeneration, in
that order. It ends with `docgraph check --strict`. Actionlint skips when no
workflow files exist. Tests run with `uv run pytest -n auto tests -q`.
There are no separate slow checks; `ci-slow` calls `ci`.

`build` calls `regen`; it creates no wheel or source distribution.
An unset or empty `OUT` selects `_site/simple`. An environment prefix such as
`OUT=/tmp/index/simple just regen` selects another directory. Regeneration
reads live GitHub release metadata through the signed-in `gh` session or its
configured token, so the full gate needs access to every allowlisted repo.

Every public recipe supports `AI=1`. The wrapper runs the recipe with AI
unset, writes the full output to `.ci-ai.log`, and prints one pass line on
success. On failure it prints a failure line and the log tail, or uses
`scripts/ai_filter_log.py` if that file exists. It returns a nonzero result.
The current repository has no filter script.

## Tooling releases

This repository publishes the index. It does not publish a Python distribution
of its own.

`scripts/do-release.sh` sets `RELEASE_REPO` to `pdomain/pdomain-index-pip`,
`RELEASE_BUILD` to `:`, and `RELEASE_PREFLIGHT` to `just ci`. It then runs
`scripts/release-common.sh`.

`just release-patch`, `just release-minor`, and `just release-major` call that
script. The next version comes from existing `vN.N.N` git tags.
`RELEASE_BUILD=":"` skips the separate release-artifact build. The GitHub Release is the tag alone,
unless files are already present under `dist/`. The helper attaches matching
`.whl`, `.tar.gz`, and `.tgz` files when they are there. GitHub-generated
release notes are the notes for these tooling releases.

Release preflight runs `just ci`, which regenerates local `_site/simple`.
A tooling release does not publish that tree or push `gh-pages`. Package
versions that installers see come from the publisher repositories' release
assets.

The release helper fetches the release branch and tags, then checks the
checkout is clean, on the release branch, and not behind or diverged from
its remote. A local branch ahead of its remote is allowed. `FORCE=1` skips
those state guards but still runs preflight.

After preflight succeeds, the helper creates an annotated tag, pushes the
release branch and that exact tag, and creates the GitHub Release. A failure
after tagging can leave a pushed tag without a completed release.
`SKIP_PUSH=1` returns after local tagging, before pushes or release creation.
The recipe does not install packages, update consumers, or restart services.

`scripts/release-common.sh` is a vendored copy of the shared pdomain release
driver. This repository uses tag-derived versions, so the space-delimited
`RELEASE_VERSION_FILES` list is not on the path it uses today. The helper
still contains that contract. Whether to replace it is on the
[roadmap](../roadmap.md#consider-in-another-repository).

## Evidence

- Code: `scripts/regen_index.py`, `scripts/publish-index.sh`, `justfile`,
  `scripts/do-release.sh`, `scripts/release-common.sh`

- Tests: `tests/test_regen_index.py` — 20 passed on 2026-11-12
  (`test_repo_allowlist_uses_current_pdomain_names`,
  `test_gh_json_fails_clearly_when_gh_is_missing`,
  `test_gh_json_runs_the_resolved_gh_path`,
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

- Fail-closed handling: `scripts/regen_index.py:89-91,126-129,133-136,156-159`

- Integrity fragments: `scripts/regen_index.py:226-228`

- `gh` resolution and missing-tool error: `scripts/regen_index.py:80-86`

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

- Verified: 2026-11-12 with `uv run pytest tests/test_regen_index.py`
  (20 passed) after the `gh` resolution merge.

- Verified: 2026-11-12 by reading `scripts/regen_index.py`,
  `scripts/publish-index.sh`, `scripts/do-release.sh`, and
  `scripts/release-common.sh`.

- Staged output and permissions: `scripts/regen_index.py` (`main`),
  `test_main_replaces_existing_output_tree`; rationale in commit `7717d55`.

- Task runner: commits `2ef728b` and `bb3983a`; CI and release ordering
  verified by source inspection on 2026-11-13.

- Source/API allowlist: `scripts/regen_index.py` and the parameterized
  new-repository tests in `tests/test_regen_index.py` cover matching wheel
  and sdist links, retained digests, empty-release pages, and HTML-only output.

- Baseline verification: 2026-11-13 with `just test` in the migration
  worktree (20 passed). Release and publication scripts were not executed.

## Provenance

Five migrated GitHub issues are represented above rather than in
`docs/issues/`. Four were already implemented when the issue tracker was
migrated on 2026-07-19. Issue #21 was implemented on 2026-11-10:

| Issue | Behavior | Section |
| --- | --- | --- |
| #16 | Explicit index and per-package source mapping | Consumer resolution boundary |
| #17 | Fail-closed on unexpected fetch failures | Trust boundary |
| #19 | PEP 503 `#sha256=` fragments | Integrity metadata |
| #20 | Generator test coverage | Evidence |
| #21 | Resolve `gh` before subprocess invocation | GitHub CLI invocation |

Full provenance, including node IDs and raw digests, is in the
[migration ledger](../context/github-issue-migration-ledger.md).
