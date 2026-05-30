from __future__ import annotations

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


def test_render_project_page_skips_duplicate_non_dist_and_unsafe_assets() -> None:
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
