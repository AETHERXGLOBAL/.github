"""F05 source-level trust-boundary regression (no credentials, no network)."""
from __future__ import annotations

import base64
import importlib.util
import re
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "profile" / "scripts" / "inspect_profile_pr.py"
SPEC = importlib.util.spec_from_file_location("trusted_profile_inspection", SCRIPT)
inspect = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(inspect)
WORKFLOWS = {
    ".github/workflows/update-engineering-pulse.yml": ("push", "schedule"),
    ".github/workflows/update-project-pulse.yml": ("push", "schedule", "repository_dispatch"),
}


def source_for(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class WorkflowTrustBoundary(unittest.TestCase):
    def test_privileged_workflows_only_have_trusted_events(self):
        for path, allowed in WORKFLOWS.items():
            with self.subTest(path=path):
                inspect.verify_privileged_workflow(source_for(path), allowed)

    def test_pr_inspection_never_executes_head_or_receives_project_secrets(self):
        trusted = source_for(".github/workflows/inspect-profile-pr.yml")
        self.assertIn("pull_request_target:", trusted)
        self.assertIn("ref: main", trusted)
        self.assertIn("persist-credentials: false", trusted)
        self.assertIn("contents: read", trusted)
        self.assertIn("pull-requests: read", trusted)
        self.assertNotIn("contents: write", trusted)
        self.assertNotIn("PROJECT_PULSE_READ_TOKEN", trusted)
        self.assertNotIn("ref: ${{", trusted)
        self.assertNotIn("checkout@v4", trusted)
        self.assertIn("python3 -B profile/scripts/inspect_profile_pr.py", trusted)
        self.assertNotIn("gh pr checkout", trusted)

    def test_injected_pr_trigger_fails(self):
        for path, allowed in WORKFLOWS.items():
            with self.subTest(path=path):
                source = source_for(path)
                for event in ("pull_request", "workflow_dispatch", "pull_request_target", "workflow_run"):
                    changed = source.replace("\non:\n", f"\non:\n  {event}:\n", 1)
                    with self.assertRaises(ValueError, msg=event):
                        inspect.verify_privileged_workflow(changed, allowed)

    def test_fail_open_or_true_mutation_detected(self):
        for path, allowed in WORKFLOWS.items():
            with self.subTest(path=path):
                source = source_for(path)
                for injected in (
                    "github.ref == 'refs/heads/main' || true",
                    "github.ref != 'refs/heads/main'",
                    "github.ref == 'refs/heads/main' || github.event_name == 'pull_request'",
                    "github.ref == 'refs/heads/automation/public-github-activity-review'",
                ):
                    changed = source.replace("github.ref == 'refs/heads/main'", injected, 1)
                    with self.assertRaises(ValueError, msg=injected):
                        inspect.verify_privileged_workflow(changed, allowed)

    def test_permission_escalation_detected(self):
        for path, allowed in WORKFLOWS.items():
            with self.subTest(path=path):
                source = source_for(path)
                cases = (
                    source.replace("\npermissions:\n  contents: read", "\npermissions:\n  contents: write", 1),
                    source.replace("      pull-requests: write", "      actions: write\n      pull-requests: write", 1),
                    source.replace("    runs-on: ubuntu-latest", "    runs-on: self-hosted", 1),
                )
                for changed in cases:
                    with self.assertRaises(ValueError):
                        inspect.verify_privileged_workflow(changed, allowed)

    def test_extra_privileged_job_detected(self):
        for path, allowed in WORKFLOWS.items():
            source = source_for(path)
            with self.subTest(path=path):
                changed = source.replace("\njobs:\n", "\njobs:\n  malicious:\n    runs-on: ubuntu-latest\n", 1)
                with self.assertRaises(ValueError):
                    inspect.verify_privileged_workflow(changed, allowed)

    def test_credential_persistence_and_unpinned_checkout_detected(self):
        for path, allowed in WORKFLOWS.items():
            source = source_for(path)
            with self.subTest(path=path):
                for changed in (
                    source.replace("persist-credentials: false", "persist-credentials: true", 1),
                    source.replace(inspect.CHECKOUT, "actions/checkout@v4", 1),
                    source.replace("          ref: main", "          ref: automation/untrusted", 1),
                ):
                    with self.assertRaises(ValueError):
                        inspect.verify_privileged_workflow(changed, allowed)

    def test_closed_bytes_reject_appended_shell_action_and_secret(self):
        # The exact attack from AETHER SECURITY: formerly FALSE_GREEN.
        for path, allowed in WORKFLOWS.items():
            with self.subTest(file=path):
                original = source_for(path)
                mutations = (
                    original + "\n      - name: INERT_SECURITY_TEST\n        run: echo F05_INERT_CANARY\n",
                    original + "\n      - name: INERT_ACTION\n        uses: example/action@deadbeef\n",
                    original + "\n        env:\n          INERT: ${{ secrets.PROJECT_PULSE_READ_TOKEN }}\n",
                    original.replace("      - name: Checkout", "      - name: INERT\n        run: echo INERT\n      - name: Checkout", 1),
                    original.replace("        env:\n", "        env:\n          CANARY: ${{ secrets.OTHER_SECRET }}\n", 1),
                    original.replace("      - name: Validate", "      - name: INERT\n        uses: example/action@deadbeef\n      - name: Validate", 1),
                    original.replace("jobs:\n", "jobs:\n  sidecar:\n    runs-on: ubuntu-latest\n    steps:\n      - run: echo INERT\n", 1),
                    original.replace("  refresh:\n", "  refresh:\n    env:\n      CANARY: ${{ secrets.OTHER_SECRET }}\n", 1),
                    original.replace("jobs:\n", "jobs:\n  refresh:\n    if: true\n", 1),
                    original.replace("\non:\n", "\non:\n  schedule: [ { cron: '* * * * *' } ]\n", 1),
                    original.replace("permissions:\n", "permissions:\n  contents: write\n", 1),
                )
                for i, changed in enumerate(mutations):
                    with self.subTest(mutation=i), self.assertRaises(ValueError):
                        inspect.verify_privileged_workflow(changed, allowed)

    def test_inspector_workflow_is_immutably_pinned(self):
        path = ".github/workflows/inspect-profile-pr.yml"
        self.assertIn(path, inspect.APPROVED_WORKFLOW_SHA256)
        import hashlib
        self.assertEqual(hashlib.sha256(source_for(path).encode()).hexdigest(),
                         inspect.APPROVED_WORKFLOW_SHA256[path])
        self.assertEqual(set(inspect.APPROVED_WORKFLOW_SHA256), set(WORKFLOWS) | {path})

    def test_fake_api_reads_only_pr_head_as_data(self):
        calls = []
        sha = "a" * 40
        def fake_get(route, token):
            self.assertEqual(token, "TEST_INERT_TOKEN")
            calls.append(route)
            if route.endswith("/pulls/29"):
                return {
                    "base": {"repo": {"full_name": "AETHERXGLOBAL/.github"}, "ref": "main", "sha": "1" * 40},
                    "head": {"repo": {"full_name": "AETHERXGLOBAL/.github"}, "sha": sha},
                    "changed_files": 3,
                }
            if "/pulls/29/files?" in route:
                return ([{"filename": path, "status": "modified"} for path in inspect.APPROVED_WORKFLOW_SHA256]
                        if route.endswith("&page=1") else [])
            for path in inspect.APPROVED_WORKFLOW_SHA256:
                if path in route:
                    return {"type": "file", "encoding": "base64",
                            "content": base64.b64encode(source_for(path).encode()).decode()}
            raise AssertionError(route)
        with patch.object(inspect, "_api_get", side_effect=fake_get):
            inspect.inspect_pr("AETHERXGLOBAL/.github", 29, "TEST_INERT_TOKEN")
        self.assertEqual(len(calls), 7)
        self.assertTrue(all("/contents/" in route for route in calls[3:6]))
        self.assertTrue(all(f"?ref={sha}" in route for route in calls[3:6]))

    def test_new_workflow_file_fails_before_any_content_execution(self):
        sha = "a" * 40
        routes = []
        def fake_get(route, token):
            routes.append(route)
            if route.endswith("/pulls/29"):
                return {"base": {"repo": {"full_name": "AETHERXGLOBAL/.github"}, "ref": "main", "sha": "1" * 40},
                        "head": {"repo": {"full_name": "AETHERXGLOBAL/.github"}, "sha": sha},
                        "changed_files": 1}
            if "/files?" in route:
                return [{"filename": ".github/workflows/evil-new-workflow.yml", "status": "added"}]
            raise AssertionError("Should block before fetching content")
        with patch.object(inspect, "_api_get", side_effect=fake_get):
            with self.assertRaisesRegex(ValueError, "F05_NEW_UNREVIEWED_WORKFLOW"):
                inspect.inspect_pr("AETHERXGLOBAL/.github", 29, "TEST_INERT_TOKEN")
        self.assertEqual(len(routes), 2)

    def test_changed_workflow_bytes_fail_even_if_they_preserve_all_checked_fields(self):
        for path in inspect.APPROVED_WORKFLOW_SHA256:
            with self.subTest(path=path):
                original = source_for(path)
                import hashlib
                self.assertEqual(hashlib.sha256(original.encode()).hexdigest(),
                                 inspect.APPROVED_WORKFLOW_SHA256[path])
                self.assertNotEqual(hashlib.sha256((original + "\n#INERT\n").encode()).hexdigest(),
                                    inspect.APPROVED_WORKFLOW_SHA256[path])

    def test_mutated_api_workflow_is_rejected_end_to_end(self):
        sha = "a" * 40
        def fake_get(route, token):
            if route.endswith("/pulls/29"):
                return {"base": {"repo": {"full_name": "AETHERXGLOBAL/.github"}, "ref": "main", "sha": "1" * 40},
                        "head": {"repo": {"full_name": "AETHERXGLOBAL/.github"}, "sha": sha}, "changed_files": 3}
            if "/files?" in route:
                return ([{"filename": path, "status": "modified"} for path in inspect.APPROVED_WORKFLOW_SHA256]
                        if route.endswith("&page=1") else [])
            for path in inspect.APPROVED_WORKFLOW_SHA256:
                if path in route:
                    content = source_for(path)
                    if path.endswith("update-engineering-pulse.yml"):
                        content += "\n      - name: INERT_SECURITY_TEST\n        run: echo F05_INERT_CANARY\n"
                    return {"type": "file", "encoding": "base64",
                            "content": base64.b64encode(content.encode()).decode()}
            raise AssertionError(route)
        with patch.object(inspect, "_api_get", side_effect=fake_get):
            with self.assertRaisesRegex(ValueError, "F05_UNREVIEWED_WORKFLOW_BYTES"):
                inspect.inspect_pr("AETHERXGLOBAL/.github", 29, "TEST_INERT_TOKEN")

    def test_concurrent_pr_head_update_fails_closed(self):
        attempts = 0
        sha = "a" * 40
        def fake_get(route, token):
            nonlocal attempts
            if route.endswith("/pulls/29"):
                attempts += 1
                return {"base": {"repo": {"full_name": "AETHERXGLOBAL/.github"}, "ref": "main", "sha": "1" * 40},
                        "head": {"repo": {"full_name": "AETHERXGLOBAL/.github"},
                                 "sha": sha if attempts == 1 else "b" * 40}, "changed_files": 3}
            if "/files?" in route:
                return ([{"filename": path, "status": "modified"} for path in inspect.APPROVED_WORKFLOW_SHA256]
                        if route.endswith("&page=1") else [])
            for path in inspect.APPROVED_WORKFLOW_SHA256:
                if path in route:
                    return {"type": "file", "encoding": "base64",
                            "content": base64.b64encode(source_for(path).encode()).decode()}
            raise AssertionError(route)
        with patch.object(inspect, "_api_get", side_effect=fake_get):
            with self.assertRaisesRegex(ValueError, "F05_PR_HEAD_MOVED_RETRY_REQUIRED"):
                inspect.inspect_pr("AETHERXGLOBAL/.github", 29, "TEST_INERT_TOKEN")
        self.assertEqual(attempts, 2)

    def test_fake_api_refuses_mismatched_base(self):
        pr = {"base": {"ref": "untrusted", "repo": {"full_name": "AETHERXGLOBAL/.github"}},
              "head": {"sha": "a"*40, "repo": {"full_name": "AETHERXGLOBAL/.github"}}}
        with patch.object(inspect, "_api_get", return_value=pr):
            with self.assertRaises(ValueError):
                inspect.inspect_pr("AETHERXGLOBAL/.github", 29, "TEST_INERT_TOKEN")


if __name__ == "__main__":
    unittest.main()
