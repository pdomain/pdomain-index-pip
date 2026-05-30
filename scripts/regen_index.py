"""Regenerate the PEP 503 simple index from GitHub Releases.

Reads release-asset metadata via the `gh` CLI (which uses GITHUB_TOKEN in CI or
the user's local auth in dev) and emits static HTML under --out.

PEP 503 only requires `<a href>` links to wheel/sdist filenames. We point each
link directly at the GitHub Release asset's download URL so consumers fetch
from github.com release storage, not from this index host.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import TypedDict, cast
from urllib.parse import unquote, urlparse

ORG = "pdomain"
RELEASE_LIMIT = 1000

# Every pdomain repo that may publish Python distribution assets to GitHub
# Releases. Keep alphabetized. Append a new repo when it starts cutting releases;
# safe to list a repo with zero releases (renders an empty page).
REPOS: list[str] = [
    "pdomain-book-tools",
    "pdomain-ocr-cli",
    "pdomain-ocr-labeler-spa",
    "pdomain-ocr-simple-gui",
    "pdomain-ocr-synth",
    "pdomain-ocr-trainer-spa",
    "pdomain-ocr-training",
    "pdomain-ops",
    "pdomain-prep-for-pgdp",
]


class GitHubAsset(TypedDict, total=False):
    name: str
    url: str


class GitHubReleaseSummary(TypedDict, total=False):
    tagName: str
    isDraft: bool
    isPrerelease: bool
    publishedAt: str


class GitHubReleaseAssets(TypedDict, total=False):
    assets: list[GitHubAsset]


class IndexedRelease(TypedDict):
    tag: str
    is_prerelease: bool
    published_at: str
    assets: list[GitHubAsset]


class ParsedArgs(argparse.Namespace):
    out: Path = Path("_site/simple")


def normalize(name: str) -> str:
    """PEP 503 normalization: lowercase, runs of [-_.] collapse to a single -."""
    return re.sub(r"[-_.]+", "-", name).lower()


def gh_json(args: Sequence[str]) -> object:
    """Run `gh` with --json output and parse. Raise on non-zero."""
    proc = subprocess.run(["gh", *args], capture_output=True, text=True, check=True)
    return cast(object, json.loads(proc.stdout))


def is_repo_not_found_error(exc: subprocess.CalledProcessError) -> bool:
    stderr = cast(str | None, exc.stderr) or ""
    return "Could not resolve to a Repository" in stderr or "404" in stderr


def asset_download_url_is_safe(repo: str, url: str) -> bool:
    parsed = urlparse(url)
    decoded_path = unquote(parsed.path)
    expected_prefix = f"/{ORG}/{repo}/releases/download/"
    return (
        parsed.scheme == "https"
        and parsed.netloc == "github.com"
        and decoded_path.startswith(expected_prefix)
        and "/../" not in decoded_path
        and not decoded_path.endswith("/..")
    )


def fetch_releases(repo: str) -> list[IndexedRelease]:
    """Return non-draft releases for pdomain/<repo>, with assets.

    Returns [] if the repo doesn't exist or has no releases. Errors other than
    not-found are re-raised — we want the workflow to fail loudly on auth or
    rate-limit problems rather than silently emit a stale empty page.
    """
    try:
        rels = gh_json(
            [
                "release",
                "list",
                "--repo",
                f"{ORG}/{repo}",
                "--limit",
                str(RELEASE_LIMIT),
                "--json",
                "tagName,name,isDraft,isPrerelease,publishedAt",
            ]
        )
    except subprocess.CalledProcessError as e:
        if is_repo_not_found_error(e):
            print(f"  {repo}: repo not found, skipping", file=sys.stderr)
            return []
        raise

    out: list[IndexedRelease] = []
    release_summaries = cast(list[GitHubReleaseSummary], rels)
    if len(release_summaries) >= RELEASE_LIMIT:
        print(
            f"  {repo}: reached release limit {RELEASE_LIMIT}; older releases may be omitted",
            file=sys.stderr,
        )
    for rel in release_summaries:
        if rel.get("isDraft"):
            continue
        tag = rel.get("tagName", "")
        if not tag:
            print(f"  {repo}: release missing tagName, skipping", file=sys.stderr)
            continue
        try:
            view = gh_json(
                [
                    "release",
                    "view",
                    tag,
                    "--repo",
                    f"{ORG}/{repo}",
                    "--json",
                    "assets",
                ]
            )
        except subprocess.CalledProcessError as e:
            if is_repo_not_found_error(e):
                print(f"  {repo}@{tag}: release not found, skipping tag", file=sys.stderr)
                continue
            raise
        release_assets = cast(GitHubReleaseAssets, view)
        out.append(
            {
                "tag": tag,
                "is_prerelease": rel.get("isPrerelease", False),
                "published_at": rel.get("publishedAt", ""),
                "assets": release_assets.get("assets", []),
            }
        )
    return out


_DIST_SUFFIXES = (".whl", ".tar.gz", ".zip")


def render_project_page(repo: str, project_normalized: str, releases: list[IndexedRelease]) -> str:
    lines = [
        "<!DOCTYPE html>",
        "<html><head>",
        '<meta name="pypi:repository-version" content="1.0">',
        f"<title>Links for {html.escape(project_normalized)}</title>",
        "</head><body>",
        f"<h1>Links for {html.escape(project_normalized)}</h1>",
    ]
    seen: set[str] = set()
    sorted_rels = sorted(releases, key=lambda r: r.get("published_at", ""))
    for rel in sorted_rels:
        for a in rel["assets"]:
            fname = a.get("name", "")
            if not fname.endswith(_DIST_SUFFIXES):
                continue
            if fname in seen:
                continue
            url = a.get("url", "")
            if not url:
                continue
            if not asset_download_url_is_safe(repo, url):
                print(f"  {repo}: skipping unsafe asset URL for {fname}", file=sys.stderr)
                continue
            seen.add(fname)
            lines.append(f'<a href="{html.escape(url)}">{html.escape(fname)}</a><br>')
    lines.append("</body></html>")
    return "\n".join(lines) + "\n"


def render_root_page(repos: list[str]) -> str:
    lines = [
        "<!DOCTYPE html>",
        "<html><head>",
        '<meta name="pypi:repository-version" content="1.0">',
        "<title>Simple Index</title>",
        "</head><body>",
        "<h1>Simple Index</h1>",
    ]
    for repo in sorted(repos):
        n = normalize(repo)
        lines.append(f'<a href="{n}/">{html.escape(n)}</a><br>')
    lines.append("</body></html>")
    return "\n".join(lines) + "\n"


def parse_output_dir(argv: Sequence[str] | None = None) -> Path:
    ap = argparse.ArgumentParser(description=__doc__)
    _ = ap.add_argument(
        "--out",
        type=Path,
        default=Path("_site/simple"),
        help="Output dir for simple-index HTML (default: _site/simple)",
    )
    args = ap.parse_args(argv, namespace=ParsedArgs())
    return args.out


def main() -> int:
    out = parse_output_dir()
    out.mkdir(parents=True, exist_ok=True)

    total_assets = 0
    for repo in REPOS:
        n = normalize(repo)
        proj_dir = out / n
        proj_dir.mkdir(parents=True, exist_ok=True)
        releases = fetch_releases(repo)
        page = render_project_page(repo=repo, project_normalized=n, releases=releases)
        _ = (proj_dir / "index.html").write_text(page, encoding="utf-8")
        n_assets = sum(
            1 for r in releases for a in r["assets"] if a.get("name", "").endswith(_DIST_SUFFIXES)
        )
        total_assets += n_assets
        print(f"  {n}: {len(releases)} releases, {n_assets} dist assets")

    _ = (out / "index.html").write_text(render_root_page(REPOS), encoding="utf-8")
    print(f"wrote root index -> {out / 'index.html'}")
    print(f"total assets indexed: {total_assets}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
