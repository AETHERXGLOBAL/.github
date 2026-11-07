"""F05: static regression checks for privileged GitHub workflow entrypoints.

This checks the reviewed workflow files, not the GitHub organization's
effective permissions. It is defense-in-depth, not a substitute for
independent assurance or a hosted authorization test.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = {
    "update-engineering-pulse.yml": {"pull_request", "push", "schedule"},
    "update-project-pulse.yml": {"pull_request", "push", "schedule", "repository_dispatch"},
}


def check_trusted_refresh_contract(source: str, expected_events: set[str]) -> None:
    if not source.startswith("name: "):
        raise AssertionError("Workflow name header absent")
    if "\non:\n" not in source:
        raise AssertionError("Top-level trigger block absent")
    on_block = "\n" + source.split("\non:\n", 1)[1].split("\npermissions:\n", 1)[0]
    found_events = set(re.findall(r"^  ([a-z_]+):", on_block, re.MULTILINE))
    if found_events != expected_events:
        raise AssertionError(f"Unexpected event triggers: {found_events}")
    if "workflow_dispatch" in source or "pull_request_target" in source:
        raise AssertionError("Untrusted branch-selectable / privileged trigger")
    if source.count("  refresh:\n") != 1 or source.count("  validate:\n") != 1:
        raise AssertionError("Unexpected privileged or validation job structure")
    refresh = source.split("\n  refresh:\n", 1)[1]
    if not refresh.startswith("    if: >-\n"):
        raise AssertionError("Positive refresh event gate required")
    guard = refresh.split("\n    permissions:\n", 1)[0]
    if "github.ref == 'refs/heads/main'" not in guard:
        raise AssertionError("Default branch guard absent")
    allowed = expected_events - {"pull_request"}
    actual = set(re.findall(r"github\.event_name == '([a-z_]+)'", guard))
    if actual != allowed:
        raise AssertionError(f"Privileged event allowlist changed: {actual}")
    if "!= 'pull_request'" in guard or "workflow_dispatch" in guard:
        raise AssertionError("Fail-open event gate")
    if "      contents: write\n" not in refresh or "      pull-requests: write\n" not in refresh:
        raise AssertionError("Expected bounded refresh permissions absent")
    validate = source.split("\n  validate:\n", 1)[1].split("\n  refresh:\n", 1)[0]
    if "github.event_name == 'pull_request'" not in validate:
        raise AssertionError("PR validation trigger absent")
    if "      contents: read\n" not in validate or "persist-credentials: false" not in validate:
        raise AssertionError("Read-only PR checkout was weakened")
    if source.count("actions/checkout@11d5960a326750d5838078e36cf38b85af677262") < 2:
        raise AssertionError("Unpinned checkout")
    if "  contents: read\n" not in source.split("\njobs:\n", 1)[0]:
        raise AssertionError("Workflow top-level read-only default absent")


class WorkflowEntrypointGuard(unittest.TestCase):
    def test_both_privileged_workflows_are_default_branch_bound(self):
        for file, expected in WORKFLOWS.items():
            with self.subTest(file=file):
                source = (ROOT / ".github" / "workflows" / file).read_text()
                check_trusted_refresh_contract(source, expected)

    def test_injected_dispatch_fails_contract(self):
        for file, expected in WORKFLOWS.items():
            with self.subTest(file=file):
                source = (ROOT / ".github" / "workflows" / file).read_text()
                altered = source.replace("\non:\n", "\non:\n  workflow_dispatch:\n", 1)
                with self.assertRaises(AssertionError):
                    check_trusted_refresh_contract(altered, expected)

    def test_removed_default_branch_gate_fails_contract(self):
        for file, expected in WORKFLOWS.items():
            with self.subTest(file=file):
                source = (ROOT / ".github" / "workflows" / file).read_text()
                altered = source.replace("github.ref == 'refs/heads/main'", "github.ref != 'refs/heads/main'", 1)
                # Exact positive guard required; merely checking for substring
                # would produce a false pass on this negative fixture.
                with self.assertRaises(AssertionError):
                    check_trusted_refresh_contract(altered, expected)

    def test_added_privileged_event_fails_contract(self):
        for file, expected in WORKFLOWS.items():
            with self.subTest(file=file):
                source = (ROOT / ".github" / "workflows" / file).read_text()
                altered = source.replace("github.event_name == 'push'", "github.event_name == 'workflow_dispatch'", 1)
                with self.assertRaises(AssertionError):
                    check_trusted_refresh_contract(altered, expected)


if __name__ == "__main__":
    unittest.main()
