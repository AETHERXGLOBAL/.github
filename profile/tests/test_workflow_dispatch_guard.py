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

    def test_fake_api_reads_only_pr_head_as_data(self):
        calls = []
        sha = "a" * 40
        def fake_get(route, token):
            self.assertEqual(token, "TEST_INERT_TOKEN")
            calls.append(route)
            if route.endswith("/pulls/29"):
                return {
                    "base": {"repo": {"full_name": "AETHERXGLOBAL/.github"}, "ref": "main"},
                    "head": {"repo": {"full_name": "AETHERXGLOBAL/.github"}, "sha": sha},
                }
            for path in WORKFLOWS:
                if path in route:
                    return {"type": "file", "encoding": "base64",
                            "content": base64.b64encode(source_for(path).encode()).decode()}
            raise AssertionError(route)
        with patch.object(inspect, "_api_get", side_effect=fake_get):
            inspect.inspect_pr("AETHERXGLOBAL/.github", 29, "TEST_INERT_TOKEN")
        self.assertEqual(len(calls), 3)
        self.assertTrue(all("/contents/" in route for route in calls[1:]))
        self.assertTrue(all(f"?ref={sha}" in route for route in calls[1:]))

    def test_fake_api_refuses_mismatched_base(self):
        pr = {"base": {"ref": "untrusted", "repo": {"full_name": "AETHERXGLOBAL/.github"}},
              "head": {"sha": "a"*40, "repo": {"full_name": "AETHERXGLOBAL/.github"}}}
        with patch.object(inspect, "_api_get", return_value=pr):
            with self.assertRaises(ValueError):
                inspect.inspect_pr("AETHERXGLOBAL/.github", 29, "TEST_INERT_TOKEN")


if __name__ == "__main__":
    unittest.main()
