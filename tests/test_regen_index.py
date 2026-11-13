from __future__ import annotations

import shutil
import subprocess
from collections.abc import Sequence
from pathlib import Path

import pytest

import scripts.regen_index as regen_index

BOOK_TOOLS_WHEEL_URL = (
    "https://github.com/pdomain/pdomain-book-tools/releases/download/v1.2.3/"
    "pdomain_book_tools-1.2.3-py3-none-any.whl"
)
BOOK_TOOLS_LEGACY_ORG_WHEEL_URL = (
    "https://github.com/ConcaveTrillion/pdomain-book-tools/releases/download/v1.2.3/"
    "pdomain_book_tools-1.2.3-py3-none-any.whl"
)
BOOK_TOOLS_100_WHEEL_URL = (
    "https://github.com/pdomain/pdomain-book-tools/releases/download/"
    "v1.0.0/pdomain_book_tools-1.0.0-py3-none-any.whl"
)
BOOK_TOOLS_100_SDIST_URL = (
    "https://github.com/pdomain/pdomain-book-tools/releases/download/"
    "v1.0.0/pdomain_book_tools-1.0.0.tar.gz"
)
BOOK_TOOLS_100_README_URL = (
    "https://github.com/pdomain/pdomain-book-tools/releases/download/v1.0.0/README.md"
)


def test_repo_allowlist_uses_current_pdomain_names() -> None:
    assert regen_index.ORG == "pdomain"
    assert "pdomain-ops" in regen_index.REPOS
    assert "pdomain-ocr-ops" not in regen_index.REPOS
    assert not any(repo.startswith("pd-") for repo in regen_index.REPOS)


@pytest.mark.parametrize("repo", ["pdomain-pgdp-api-client", "pdomain-source-data"])
def test_repo_allowlist_includes_requested_packages(repo: str) -> None:
    assert repo in regen_index.REPOS
    assert sorted(set(regen_index.REPOS)) == regen_index.REPOS


def test_gh_json_fails_clearly_when_gh_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def gh_not_found(_name: str) -> str | None:
        return None

    def unexpected_run(*_args: object, **_kwargs: object) -> None:
        pytest.fail("subprocess.run must not be called when gh is missing")

    monkeypatch.setattr(shutil, "which", gh_not_found)
    monkeypatch.setattr(subprocess, "run", unexpected_run)
    with pytest.raises(RuntimeError, match=r"^gh executable not found on PATH$"):
        _ = regen_index.gh_json(["api", "rate_limit"])


def test_gh_json_runs_the_resolved_gh_path(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def gh_in_tools(name: str) -> str:
        return f"/tools/{name}"

    observed: dict[str, object] = {}

    def fake_run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        observed["command"] = command
        observed["kwargs"] = kwargs
        return subprocess.CompletedProcess(command, 0, stdout='{"ok": true}')

    monkeypatch.setattr(shutil, "which", gh_in_tools)
    monkeypatch.setattr(subprocess, "run", fake_run)
    assert regen_index.gh_json(["api", "rate_limit"]) == {"ok": True}
    assert observed == {
        "command": ["/tools/gh", "api", "rate_limit"],
        "kwargs": {"capture_output": True, "text": True, "check": True},
    }


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        (BOOK_TOOLS_WHEEL_URL, True),
        (BOOK_TOOLS_LEGACY_ORG_WHEEL_URL, False),
        ("http://github.com/pdomain/pdomain-book-tools/releases/download/v1.2.3/pkg.whl", False),
        ("https://example.com/pdomain/pdomain-book-tools/releases/download/v1.2.3/pkg.whl", False),
        ("file:///tmp/pkg.whl", False),
    ],
)
def test_asset_download_url_is_limited_to_repo_release_downloads(url: str, expected: bool) -> None:
    assert regen_index.asset_download_url_is_safe("pdomain-book-tools", url) is expected


@pytest.mark.parametrize(
    ("filename", "expected"),
    [
        ("pdomain_book_tools-1.0.0-py3-none-any.whl", "pdomain-book-tools"),
        ("pdomain_book_tools-1.0.0.tar.gz", "pdomain-book-tools"),
        ("pdomain_book_tools-1.0.0.zip", "pdomain-book-tools"),
        ("README.md", None),
    ],
)
def test_distribution_name_from_asset(filename: str, expected: str | None) -> None:
    assert regen_index.distribution_name_from_asset(filename) == expected


def test_render_project_page_skips_duplicate_non_dist_unsafe_and_wrong_project_assets() -> None:
    releases: list[regen_index.IndexedRelease] = [
        {
            "tag": "v1.0.0",
            "is_prerelease": False,
            "published_at": "2026-01-01T00:00:00Z",
            "assets": [
                {
                    "name": "pdomain_book_tools-1.0.0-py3-none-any.whl",
                    "url": BOOK_TOOLS_100_WHEEL_URL,
                },
                {
                    "name": "pdomain_book_tools-1.0.0-py3-none-any.whl",
                    "url": BOOK_TOOLS_100_WHEEL_URL,
                },
                {
                    "name": "README.md",
                    "url": BOOK_TOOLS_100_README_URL,
                },
                {
                    "name": "evil-1.0.0.whl",
                    "url": "https://example.com/evil-1.0.0.whl",
                },
                {
                    "name": "pd_book_tools-1.0.0-py3-none-any.whl",
                    "url": (
                        "https://github.com/pdomain/pdomain-book-tools/releases/download/"
                        "v1.0.0/pd_book_tools-1.0.0-py3-none-any.whl"
                    ),
                },
            ],
        },
    ]

    page = regen_index.render_project_page(
        repo="pdomain-book-tools",
        project_normalized="pdomain-book-tools",
        releases=releases,
    )

    assert page.count("pdomain_book_tools-1.0.0-py3-none-any.whl") == 2
    assert "README.md" not in page
    assert "evil-1.0.0.whl" not in page
    assert "pd_book_tools-1.0.0-py3-none-any.whl" not in page


FAKE_SHA256 = "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890ab"


@pytest.mark.parametrize(
    ("repo", "distribution", "other_distribution"),
    [
        ("pdomain-pgdp-api-client", "pdomain_pgdp_api_client", "pdomain_source_data"),
        ("pdomain-source-data", "pdomain_source_data", "pdomain_pgdp_api_client"),
    ],
)
def test_main_indexes_requested_packages_from_release_metadata_only(
    repo: str,
    distribution: str,
    other_distribution: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    wheel = f"{distribution}-1.2.3-py3-none-any.whl"
    sdist = f"{distribution}-1.2.3.tar.gz"
    wrong_wheel = f"{other_distribution}-1.2.3-py3-none-any.whl"
    wrong_sdist = f"{other_distribution}-1.2.3.tar.gz"
    release_url = f"https://github.com/pdomain/{repo}/releases/download/v1.2.3/"
    sdist_digest = "1234567890abcdef" * 4
    assets: list[regen_index.GitHubAsset] = [
        {"name": wheel, "url": release_url + wheel, "digest": f"sha256:{FAKE_SHA256}"},
        {"name": sdist, "url": release_url + sdist, "digest": f"sha256:{sdist_digest}"},
        {"name": wrong_wheel, "url": release_url + wrong_wheel},
        {"name": wrong_sdist, "url": release_url + wrong_sdist},
    ]
    observed_commands: list[list[str]] = []

    def fake_gh_json(args: Sequence[str]) -> object:
        observed_commands.append(list(args))
        if list(args[:2]) == ["release", "list"]:
            requested_repo = args[args.index("--repo") + 1]
            assert list(args) == [
                "release",
                "list",
                "--repo",
                requested_repo,
                "--limit",
                str(regen_index.RELEASE_LIMIT),
                "--json",
                "tagName,name,isDraft,isPrerelease,publishedAt",
            ]
            if requested_repo == f"pdomain/{repo}":
                return [
                    {
                        "tagName": "v1.2.3",
                        "isDraft": False,
                        "isPrerelease": False,
                        "publishedAt": "2026-11-13T00:00:00Z",
                    }
                ]
            return []
        assert list(args) == [
            "release",
            "view",
            "v1.2.3",
            "--repo",
            f"pdomain/{repo}",
            "--json",
            "assets",
        ]
        return {"assets": assets}

    def unexpected_run(*_args: object, **_kwargs: object) -> None:
        pytest.fail("index generation must use release metadata without downloading package bytes")

    out = tmp_path / "simple"
    monkeypatch.setattr(regen_index, "gh_json", fake_gh_json)
    monkeypatch.setattr(subprocess, "run", unexpected_run)
    monkeypatch.setattr("sys.argv", ["regen_index.py", "--out", str(out)])

    assert regen_index.main() == 0

    root_page = (out / "index.html").read_text(encoding="utf-8")
    assert f'<a href="{repo}/">{repo}</a><br>' in root_page
    project_page = (out / repo / "index.html").read_text(encoding="utf-8")
    assert f"<h1>Links for {repo}</h1>" in project_page
    assert f'<a href="{release_url}{wheel}#sha256={FAKE_SHA256}">{wheel}</a><br>' in project_page
    assert f'<a href="{release_url}{sdist}#sha256={sdist_digest}">{sdist}</a><br>' in project_page
    assert project_page.count("<a href=") == 2
    assert wrong_wheel not in project_page
    assert wrong_sdist not in project_page
    empty_project = regen_index.normalize(other_distribution)
    empty_page = (out / empty_project / "index.html").read_text(encoding="utf-8")
    assert f"<h1>Links for {empty_project}</h1>" in empty_page
    assert "<a href=" not in empty_page
    assert len(observed_commands) == len(regen_index.REPOS) + 1
    generated_files = {path.relative_to(out) for path in out.rglob("*") if path.is_file()}
    assert generated_files == {
        Path("index.html"),
        *(Path(name) / "index.html" for name in regen_index.REPOS),
    }


def test_render_project_page_includes_sha256_fragment_when_digest_present() -> None:
    releases: list[regen_index.IndexedRelease] = [
        {
            "tag": "v1.0.0",
            "is_prerelease": False,
            "published_at": "2026-01-01T00:00:00Z",
            "assets": [
                {
                    "name": "pdomain_book_tools-1.0.0-py3-none-any.whl",
                    "url": BOOK_TOOLS_100_WHEEL_URL,
                    "digest": f"sha256:{FAKE_SHA256}",
                },
            ],
        },
    ]
    page = regen_index.render_project_page(
        repo="pdomain-book-tools",
        project_normalized="pdomain-book-tools",
        releases=releases,
    )
    assert f"#sha256={FAKE_SHA256}" in page


def test_render_project_page_no_fragment_when_digest_absent() -> None:
    releases: list[regen_index.IndexedRelease] = [
        {
            "tag": "v1.0.0",
            "is_prerelease": False,
            "published_at": "2026-01-01T00:00:00Z",
            "assets": [
                {
                    "name": "pdomain_book_tools-1.0.0-py3-none-any.whl",
                    "url": BOOK_TOOLS_100_WHEEL_URL,
                },
            ],
        },
    ]
    page = regen_index.render_project_page(
        repo="pdomain-book-tools",
        project_normalized="pdomain-book-tools",
        releases=releases,
    )
    assert "#sha256=" not in page
    assert BOOK_TOOLS_100_WHEEL_URL in page


def test_render_project_page_no_fragment_when_digest_not_sha256() -> None:
    releases: list[regen_index.IndexedRelease] = [
        {
            "tag": "v1.0.0",
            "is_prerelease": False,
            "published_at": "2026-01-01T00:00:00Z",
            "assets": [
                {
                    "name": "pdomain_book_tools-1.0.0-py3-none-any.whl",
                    "url": BOOK_TOOLS_100_WHEEL_URL,
                    "digest": "md5:abc123",
                },
            ],
        },
    ]
    page = regen_index.render_project_page(
        repo="pdomain-book-tools",
        project_normalized="pdomain-book-tools",
        releases=releases,
    )
    assert "#sha256=" not in page
    assert BOOK_TOOLS_100_WHEEL_URL in page


def test_fetch_releases_fails_for_configured_repo_not_found(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_gh_json(_args: Sequence[str]) -> object:
        raise subprocess.CalledProcessError(
            returncode=1,
            cmd=["gh"],
            stderr="Could not resolve to a Repository",
        )

    monkeypatch.setattr(regen_index, "gh_json", fake_gh_json)

    with pytest.raises(RuntimeError, match="configured repo not found"):
        _ = regen_index.fetch_releases("pdomain-missing")


def test_fetch_releases_fails_at_release_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_gh_json(_args: Sequence[str]) -> object:
        return [
            {
                "tagName": "v1.0.0",
                "isDraft": False,
                "isPrerelease": False,
                "publishedAt": "2026-01-01T00:00:00Z",
            }
        ]

    monkeypatch.setattr(regen_index, "RELEASE_LIMIT", 1)
    monkeypatch.setattr(regen_index, "gh_json", fake_gh_json)

    with pytest.raises(RuntimeError, match="release limit"):
        _ = regen_index.fetch_releases("pdomain-book-tools")


def test_main_writes_simple_index_with_mocked_release_fetch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repos = ["pdomain-book-tools"]

    def fake_fetch_releases(repo: str) -> list[regen_index.IndexedRelease]:
        assert repo == "pdomain-book-tools"
        return [
            {
                "tag": "v1.0.0",
                "is_prerelease": False,
                "published_at": "2026-01-01T00:00:00Z",
                "assets": [
                    {
                        "name": "pdomain_book_tools-1.0.0.tar.gz",
                        "url": BOOK_TOOLS_100_SDIST_URL,
                    },
                ],
            },
        ]

    monkeypatch.setattr(regen_index, "REPOS", repos)
    monkeypatch.setattr(regen_index, "fetch_releases", fake_fetch_releases)
    monkeypatch.setattr("sys.argv", ["regen_index.py", "--out", str(tmp_path / "simple")])

    assert regen_index.main() == 0

    root = (tmp_path / "simple" / "index.html").read_text(encoding="utf-8")
    project = (tmp_path / "simple" / "pdomain-book-tools" / "index.html").read_text(
        encoding="utf-8"
    )
    assert '<a href="pdomain-book-tools/">pdomain-book-tools</a><br>' in root
    assert "pdomain_book_tools-1.0.0.tar.gz" in project


def test_main_replaces_existing_output_tree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    out = tmp_path / "simple"
    stale = out / "pdomain-old"
    stale.mkdir(parents=True)
    _ = (stale / "index.html").write_text("stale", encoding="utf-8")

    def fake_fetch_releases(_repo: str) -> list[regen_index.IndexedRelease]:
        return []

    monkeypatch.setattr(regen_index, "REPOS", ["pdomain-book-tools"])
    monkeypatch.setattr(regen_index, "fetch_releases", fake_fetch_releases)
    monkeypatch.setattr("sys.argv", ["regen_index.py", "--out", str(out)])

    assert regen_index.main() == 0
    assert not stale.exists()
    assert (out / "index.html").exists()
