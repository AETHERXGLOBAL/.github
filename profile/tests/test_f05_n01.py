"""F05-R2-F1-N01: fail-closed GitHub pull-file metadata (offline fixtures)."""
from __future__ import annotations
import base64
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("n01_inspector", ROOT / "profile/scripts/inspect_profile_pr.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
REPO = "AETHERXGLOBAL/.github"
SHA = "a" * 40


def simulate(count, pages, *, allow_files=False):
    """Run actual Python inspect_pr, never network/credentials/PR head code."""
    calls = []
    def mock_api(route, token):
        assert token == "INERT_TEST_TOKEN"
        calls.append(route)
        if route.endswith("/pulls/29"):
            result = {"base": {"repo": {"full_name": REPO}, "ref": "main", "sha": "1" * 40},
                      "head": {"sha": SHA, "repo": {"full_name": REPO}}}
            if count is not None:
                result["changed_files"] = count
            return result
        if "/files?" in route:
            page = int(route.split("&page=")[-1])
            return pages.get(page, [])
        if allow_files:
            for filename in checker.APPROVED_WORKFLOW_SHA256:
                if filename in route:
                    raw = (ROOT / filename).read_bytes()
                    return {"type": "file", "encoding": "base64",
                            "content": base64.b64encode(raw).decode()}
        raise AssertionError("UNEXPECTED_CONTENT_FETCH")
    with patch.object(checker, "_api_get", side_effect=mock_api):
        checker.inspect_pr(REPO, 29, "INERT_TEST_TOKEN")
    return calls


class F05R2F1N01(unittest.TestCase):
    def test_eight_original_false_greens_now_fail_closed(self):
        file_a = {"filename": "profile/a.md", "status": "modified"}
        scenarios = {
            "empty_list_vs_eleven": (11, {1: []}),
            "short_list_vs_eleven": (11, {1: [file_a]}),
            "missing_filename": (1, {1: [{"status": "modified"}]}),
            "null_filename": (1, {1: [{"filename": None, "status": "modified"}]}),
            "missing_status": (1, {1: [{"filename": "profile/a.md"}]}),
            "rename_missing_previous": (1, {1: [{"filename": "profile/b.md", "status": "renamed"}]}),
            "duplicate_filename": (2, {1: [file_a, dict(file_a)]}),
            "duplicate_rename_source": (2, {1: [
                {"filename": "profile/b.md", "status": "renamed", "previous_filename": "profile/a.md"},
                {"filename": "profile/c.md", "status": "renamed", "previous_filename": "profile/a.md"}]})
        }
        for label, (count, pages) in scenarios.items():
            with self.subTest(label=label), self.assertRaises(ValueError):
                simulate(count, pages)

    def test_invalid_or_overflow_metadata_also_fails_closed(self):
        invalid = [
            (None, {1: [{"filename": "profile/a.md", "status": "modified"}]}),
            (True, {1: [{"filename": "profile/a.md", "status": "modified"}]}),
            (3000, {1: [{"filename": "profile/a.md", "status": "modified"}]}),
            (1, {1: [{"filename": "../.github/workflows/evil.yml", "status": "added"}]}),
            (1, {1: [{"filename": "profile/a.md", "status": "modified", "previous_filename": "profile/b.md"}]}),
            (1, {1: [{"filename": "profile/a.md", "status": "renamed", "previous_filename": "profile/a.md"}]}),
            (1, {1: [{"filename": "profile/a.md", "status": "unknown"}]}),
            (1, {1: [None]}),
            (1, {1: [{"filename": ".github/workflows/new.yml", "status": "added"}]}),
            (1, {1: [{"filename": "profile/a.md", "status": "modified"},
                    {"filename": "profile/b.md", "status": "modified"}]})
        ]
        for count, pages in invalid:
            with self.subTest(count=count, pages=pages), self.assertRaises(ValueError):
                simulate(count, pages)

    def test_complete_101_files_and_actual_workflow_bytes_are_accepted(self):
        pages = {1: [{"filename": f"profile/docs/{i:03}.md", "status": "modified"} for i in range(100)],
                 2: [{"filename": "profile/docs/100.md", "status": "modified"}]}
        calls = simulate(101, pages, allow_files=True)
        self.assertEqual(sum("/files?" in route for route in calls), 3)
        self.assertEqual(sum("/contents/" in route for route in calls), 3)
        self.assertEqual(len(calls), 8)

    def test_second_page_missing_is_not_end_of_list(self):
        page_one = [{"filename": f"profile/docs/{i:03}.md", "status": "modified"} for i in range(100)]
        with self.assertRaisesRegex(ValueError, "F05_PR_FILES_INCOMPLETE_OR_OVERFLOW"):
            simulate(101, {1: page_one, 2: []})

if __name__ == "__main__":
    unittest.main()
