"""F05 N01-CONSISTENCY-01 — six independent false-green regressions.

No network, credentials, checkout or execution of PR-head contents. All
GitHub REST responses are inert test fixtures and guarded through mocks.
"""
from __future__ import annotations

import base64
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("f05_consistency_inspector", ROOT / "profile/scripts/inspect_profile_pr.py")
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)
REPO = "AETHERXGLOBAL/.github"
SHA = "a" * 40
BASE = "1" * 40


def record(n: int):
    return {"filename": f"profile/docs/test_{n:04d}.md", "status": "modified"}


def fake_inspect(count: int, pages: dict[int, object], final_patch: dict | None = None):
    """Call actual inspector code with a complete mock REST transaction."""
    calls = []
    reads = 0

    def get(route, token):
        nonlocal reads
        if token != "INERT_TOKEN":
            raise AssertionError("Unexpected credential")
        calls.append(route)
        if route.endswith("/pulls/29"):
            reads += 1
            out = {
                "head": {"sha": SHA, "repo": {"full_name": REPO}},
                "base": {"sha": BASE, "ref": "main", "repo": {"full_name": REPO}},
                "changed_files": count,
            }
            if reads > 1 and final_patch:
                out.update(final_patch)
            return out
        if "/pulls/29/files?" in route:
            return pages.get(int(route.split("&page=")[-1]), [])
        for path in checker.APPROVED_WORKFLOW_SHA256:
            if f"/contents/{path}?" in route:
                raw = (ROOT / path).read_bytes()
                return {"type": "file", "encoding": "base64", "content": base64.b64encode(raw).decode()}
        raise AssertionError("Unexpected REST route")

    with patch.object(checker, "_api_get", side_effect=get):
        checker.inspect_pr(REPO, 29, "INERT_TOKEN")
    return calls, reads


class F05ConsistencyRegression(unittest.TestCase):
    def test_surplus_page_count_1_100_101_rejected(self):
        for count in (1, 100, 101):
            pages = {page: [record(i) for i in range((page - 1) * 100, min(page * 100, count))]
                     for page in range(1, (count + 99) // 100 + 1)}
            surplus_page = (count + 99) // 100 + 1
            pages[surplus_page] = [{"filename": ".github/workflows/attacker.yml", "status": "added"}]
            with self.subTest(count=count), self.assertRaisesRegex(ValueError, "F05_UNEXPECTED_PR_FILE_TRAILING_PAGE"):
                fake_inspect(count, pages)

    def test_same_head_changed_files_drift_rejected(self):
        with self.assertRaisesRegex(ValueError, "F05_PR_SNAPSHOT_CHANGED_RETRY_REQUIRED"):
            fake_inspect(1, {1: [record(0)]}, {"changed_files": 2})

    def test_same_head_base_sha_drift_rejected(self):
        with self.assertRaisesRegex(ValueError, "F05_PR_SNAPSHOT_CHANGED_RETRY_REQUIRED"):
            fake_inspect(1, {1: [record(0)]}, {"base": {"sha": "2" * 40, "ref": "main", "repo": {"full_name": REPO}}})

    def test_same_head_base_repo_ref_drift_rejected(self):
        with self.assertRaises(ValueError):
            fake_inspect(1, {1: [record(0)]}, {"base": {"sha": BASE, "ref": "evil", "repo": {"full_name": "other/other"}}})

    def test_same_head_head_repo_drift_rejected(self):
        with self.assertRaisesRegex(ValueError, "F05_PR_SNAPSHOT_CHANGED_RETRY_REQUIRED"):
            fake_inspect(1, {1: [record(0)]}, {"head": {"sha": SHA, "repo": {"full_name": "other/other"}}})

    def test_missing_final_base_sha_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "F05_INVALID_PR_SNAPSHOT"):
            fake_inspect(1, {1: [record(0)]}, {"base": {"ref": "main", "repo": {"full_name": REPO}}})

    def test_surplus_sentinel_invalid_type_rejected(self):
        with self.assertRaisesRegex(ValueError, "F05_UNEXPECTED_PR_FILE_TRAILING_PAGE"):
            fake_inspect(1, {1: [record(0)], 2: None})

    def test_surplus_sentinel_api_error_fails_closed(self):
        def fake_get(_route, _token):
            raise OSError("INERT_API_FAILURE")
        with patch.object(checker, "_api_get", side_effect=fake_get):
            with self.assertRaises(OSError):
                checker.inspect_pr(REPO, 29, "INERT_TOKEN")

    def test_complete_count_1_100_101_200_2999_passes(self):
        for count in (1, 100, 101, 200, 2999):
            pages = {page: [record(i) for i in range((page - 1) * 100, min(page * 100, count))]
                     for page in range(1, (count + 99) // 100 + 1)}
            with self.subTest(count=count):
                calls, reads = fake_inspect(count, pages)
                self.assertEqual(reads, 2)
                self.assertEqual(sum("/files?" in route for route in calls), (count + 99) // 100 + 1)


if __name__ == "__main__":
    unittest.main()
