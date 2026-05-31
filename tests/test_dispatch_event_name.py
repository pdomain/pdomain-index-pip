from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_active_docs_and_workflow_use_pdomain_release_dispatch_event() -> None:
    for relative_path in (".github/workflows/regen.yml", "README.md"):
        text = (ROOT / relative_path).read_text()
        assert "pd-release-published" not in text
        assert "pdomain-release-published" in text
