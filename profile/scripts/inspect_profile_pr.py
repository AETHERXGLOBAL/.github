"""F05: read-only static inspection of *data* from a PR head.

IMPORTANT: The GitHub Actions caller must be a trusted base-branch
pull_request_target workflow. It checks out only base main, with
contents:read/pull-requests:read. This script never executes PR head
code, downloads arbitrary dependencies, or reads project secrets.
It is a source guard, not an authorization boundary for all possible
workflows on other same-repository branches.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import re
from urllib.parse import quote
from urllib.request import Request, urlopen

API = "https://api.github.com"
CHECKOUT = "actions/checkout@11d5960a326750d5838078e36cf38b85af677262"
PATHS = {
    ".github/workflows/update-engineering-pulse.yml": ("push", "schedule"),
    ".github/workflows/update-project-pulse.yml": ("push", "schedule", "repository_dispatch"),
}

# Immutable byte-level policy approved as a deliberate candidate. No YAML parser
# ambiguity, duplicate-key trick, extra shell/action step, env/secret insertion,
# or unreviewed edit can pass. Every new template version requires an independent
# source review and explicit re-pinning. This is NOT a substitute for GitHub
# branch protection or checking all other workflow permissions.
APPROVED_WORKFLOW_SHA256 = {
    ".github/workflows/update-engineering-pulse.yml": "c14fac6d9f9e8a30d08ab2f553e2dcda9843546f304ee6e1369e2a9cb5e4a9a8",
    ".github/workflows/update-project-pulse.yml": "9e73d38e43b5ee3b5cd5ebf7920180297f1cd89c5aa0b15064c6f3a064a86931",
    ".github/workflows/inspect-profile-pr.yml": "b43770512253733626258a4e802b67033956debaa4b554fd28c636477c3ff9d2",
}

# Runtime source is executed by privileged refresh on the protected base.
# This policy is enforced by the *base-branch* scanner, never by candidate PR
# code. Do not allow a candidate to approve its own modified scanner/policy.
# If any protected source changes, block automated acceptance and require
# independently authenticated review and enforced branch protection.
PRIVILEGED_RUNTIME_PATHS = frozenset({
    "profile/scripts/inspect_profile_pr.py",  # security decision engine itself
    "profile/scripts/review_pr_lifecycle.sh",
    "profile/scripts/render_engineering_pulse.py",
    "profile/scripts/render_project_pulse.py",
    "profile/scripts/sanitize_project_pulse.py",
})


def is_privileged_executable_path(path: str) -> bool:
    # Deny by directory scope, not only filename. A changed script cannot
    # smuggle its new local dependency into an otherwise clean PR.
    return (
        path in PRIVILEGED_RUNTIME_PATHS
        or path.startswith("profile/scripts/")
        or path.startswith(".github/actions/")
        or path in ("pyproject.toml", "setup.py", "setup.cfg", "requirements.txt",
                    "CODEOWNERS", ".github/CODEOWNERS", "docs/CODEOWNERS",
                    "AGENTS.md", ".github/AGENTS.md")
        or path.startswith("profile/security/")
        or (path.startswith("profile/") and not path.startswith("profile/tests/")
            and path.endswith((".py", ".sh", ".bash", ".js", ".mjs", ".cjs")))
    )


EXPECTED_SHA256_BY_EVENTS = {
    tuple(events): APPROVED_WORKFLOW_SHA256[path]
    for path, events in PATHS.items()
}



def verify_privileged_workflow(source: str, allowed: tuple[str, ...]) -> None:
    """Fail closed on unexpected triggers or changed privileged job contract."""
    if not source.startswith("name: ") or source.count("\non:\n") != 1:
        raise ValueError("F05_INVALID_WORKFLOW_STRUCTURE")
    if source.count("\npermissions:\n") != 1 or source.count("\njobs:\n") != 1:
        raise ValueError("F05_DUPLICATE_WORKFLOW_KEYS")
    triggers = source.split("\non:\n", 1)[1].split("\npermissions:\n", 1)[0]
    keys = re.findall(r"^  ([a-z_]+):", triggers, flags=re.M)
    if keys != list(allowed):
        raise ValueError("F05_UNTRUSTED_ENTRYPOINT")
    if re.search(r"(?m)^  (pull_request|pull_request_target|workflow_dispatch|workflow_run):", triggers):
        raise ValueError("F05_PR_EVENT_ON_PRIVILEGED_WORKFLOW")
    root_permissions = source.split("\npermissions:\n", 1)[1].split("\nconcurrency:\n", 1)[0]
    if root_permissions.strip() != "contents: read":
        raise ValueError("F05_WORKFLOW_PERMISSION_DRIFT")
    jobs = source.split("\njobs:\n", 1)[1]
    if re.findall(r"(?m)^  ([\w-]+):\s*$", jobs) != ["refresh"]:
        raise ValueError("F05_UNEXPECTED_PRIVILEGED_JOB")
    event_condition = " || ".join("github.event_name == '" + name + "'" for name in allowed)
    exact_guard = (
        "    if: >-\n"
        "      (" + event_condition + ") &&\n"
        "      github.ref == 'refs/heads/main'\n"
    )
    if jobs.split("    permissions:\n", 1)[0].split("  refresh:\n", 1)[1] != exact_guard:
        # Caller may have comments between job declaration and if guard.
        raise ValueError("F05_FAIL_OPEN_OR_MUTATED_GUARD")
    permissions = re.split(r"(?m)^    runs-on: ", jobs.split("    permissions:\n", 1)[1], maxsplit=1)[0]
    if permissions != "      contents: write\n      pull-requests: write\n":
        raise ValueError("F05_PRIVILEGED_PERMISSION_DRIFT")
    if jobs.count("    runs-on: ubuntu-latest") != 1:
        raise ValueError("F05_RUNNER_DRIFT")
    if jobs.count("persist-credentials: false") != 1:
        raise ValueError("F05_TOKEN_PERSISTENCE_DRIFT")
    if jobs.count(CHECKOUT) != 1 or "          ref: main\n" not in jobs:
        raise ValueError("F05_UNPINNED_OR_UNTRUSTED_CHECKOUT")
    if "profile/scripts/review_pr_lifecycle.sh prepare" not in jobs or "profile/scripts/review_pr_lifecycle.sh publish" not in jobs:
        raise ValueError("F05_REVIEW_ONLY_LIFECYCLE_MISSING")
    # Full-byte integrity follows structured/bounded semantic guards. This is
    # the critical F05-R2 fix: reject *all* unauthorised executable additions.
    expected = EXPECTED_SHA256_BY_EVENTS.get(tuple(allowed))
    if expected is None or hashlib.sha256(source.encode("utf-8")).hexdigest() != expected:
        raise ValueError("F05_UNREVIEWED_WORKFLOW_BYTES")


def _api_get(path: str, token: str):
    req = Request(
        API + path,
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "AETHER-PR-METADATA-INSPECTION",
            "Authorization": "Bearer " + token,
        },
    )
    with urlopen(req, timeout=20) as response:
        return json.load(response)


def inspect_pr(repository: str, number: int, token: str) -> None:
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        raise ValueError("F05_INVALID_REPOSITORY")
    if not 1 <= number <= 1_000_000_000 or not token:
        raise ValueError("F05_INVALID_PR_CONTEXT")
    pr = _api_get(f"/repos/{repository}/pulls/{number}", token)
    if pr.get("base", {}).get("repo", {}).get("full_name") != repository:
        raise ValueError("F05_BASE_REPOSITORY_MISMATCH")
    if pr.get("base", {}).get("ref") != "main":
        raise ValueError("F05_NOT_MAIN_BASE")
    head = pr.get("head", {})
    head_sha = head.get("sha", "")
    head_repo = head.get("repo") or {}
    head_full_name = head_repo.get("full_name", "")
    if not re.fullmatch(r"[a-fA-F0-9]{40}", head_sha):
        raise ValueError("F05_INVALID_HEAD_SHA")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", head_full_name):
        raise ValueError("F05_INVALID_HEAD_REPOSITORY")
    # GitHub's changed_files is the authoritative number of changed entries.
    # A short/empty/duplicate/malformed page must NEVER mean "no more changes".
    expected_count = pr.get("changed_files")
    if type(expected_count) is not int or not 1 <= expected_count < 3000:
        raise ValueError("F05_INVALID_PR_CHANGED_FILES_COUNT")

    def valid_path(value: object) -> bool:
        if not isinstance(value, str) or not value or any(ch in value for ch in "\\\x00\r\n"):
            return False
        if value.startswith("/") or any(piece in ("", ".", "..") for piece in value.split("/")):
            return False
        return True

    seen_names: set[str] = set()
    seen_previous: set[str] = set()
    listed = 0
    pages = (expected_count + 99) // 100
    for page in range(1, pages + 1):
        files = _api_get(f"/repos/{repository}/pulls/{number}/files?per_page=100&page={page}", token)
        required_this_page = min(100, expected_count - listed)
        if not isinstance(files, list) or len(files) != required_this_page:
            raise ValueError("F05_PR_FILES_INCOMPLETE_OR_OVERFLOW")
        for entry in files:
            if not isinstance(entry, dict):
                raise ValueError("F05_INVALID_PR_FILE_ENTRY")
            name = entry.get("filename")
            status = entry.get("status")
            old = entry.get("previous_filename")
            if not valid_path(name) or name in seen_names:
                raise ValueError("F05_INVALID_OR_DUPLICATE_FILENAME")
            if status not in ("added", "modified", "removed", "renamed", "copied", "changed"):
                raise ValueError("F05_INVALID_PR_FILE_STATUS")
            if status == "renamed":
                if not valid_path(old) or old == name or old in seen_previous:
                    raise ValueError("F05_INVALID_OR_DUPLICATE_RENAME_SOURCE")
                seen_previous.add(old)
            elif old is not None:
                raise ValueError("F05_UNEXPECTED_PREVIOUS_FILENAME")
            seen_names.add(name)
            for candidate in (name, old):
                if candidate is None:
                    continue
                # Do not mistake a same-PR modification to the scanner or
                # privileged runtime helpers for validated workflow source.
                # There is deliberately no bypass flag in candidate code.
                if is_privileged_executable_path(candidate):
                    raise ValueError("F05_PROTECTED_EXECUTABLE_CHANGE_REQUIRES_MANUAL_GATE")
                if (candidate == ".github/workflows" or
                        candidate.startswith(".github/workflows/")):
                    if candidate not in APPROVED_WORKFLOW_SHA256:
                        raise ValueError("F05_NEW_UNREVIEWED_WORKFLOW")
        listed += len(files)
    if listed != expected_count or len(seen_names) != expected_count:
        raise ValueError("F05_PR_FILE_COUNT_MISMATCH")

    # Explicit end-of-list probe. Do not assume the API has no extra entries
    # merely because changed_files predicted a given last page. A nonempty,
    # missing, or malformed sentinel page fails closed (including >3000 cases).
    trailing = _api_get(
        f"/repos/{repository}/pulls/{number}/files?per_page=100&page={pages + 1}",
        token,
    )
    if not isinstance(trailing, list) or trailing:
        raise ValueError("F05_UNEXPECTED_PR_FILE_TRAILING_PAGE")

    # Pinned by immutable PR-head SHA; do not checkout or run any PR content.
    for path, expected in APPROVED_WORKFLOW_SHA256.items():
        data = _api_get(
            f"/repos/{head_full_name}/contents/{quote(path, safe='/')}?ref={head_sha}",
            token,
        )
        if data.get("type") != "file" or data.get("encoding") != "base64":
            raise ValueError("F05_MISSING_WORKFLOW_SOURCE")
        encoded = data.get("content", "")
        if not isinstance(encoded, str) or len(encoded) > 90000:
            raise ValueError("F05_INVALID_BASE64_WORKFLOW")
        raw = base64.b64decode("".join(encoded.split()), validate=True)
        if len(raw) > 65536:
            raise ValueError("F05_OVERSIZED_WORKFLOW_SOURCE")
        if hashlib.sha256(raw).hexdigest() != expected:
            raise ValueError("F05_UNREVIEWED_WORKFLOW_BYTES")
        if path in PATHS:
            verify_privileged_workflow(raw.decode("utf-8", errors="strict"), PATHS[path])

    # Bind all security-relevant PR metadata to one snapshot, not just HEAD.
    # The candidate SHA is immutable, but its PR base/count may change while
    # this read-only inspection is underway. Missing fields fail closed.
    def snapshot(value: object) -> tuple[str, str, str, str, str, int]:
        if not isinstance(value, dict):
            raise ValueError("F05_INVALID_PR_SNAPSHOT")
        head_value = value.get("head")
        base_value = value.get("base")
        if not isinstance(head_value, dict) or not isinstance(base_value, dict):
            raise ValueError("F05_INVALID_PR_SNAPSHOT")
        head_repo_value = head_value.get("repo")
        base_repo_value = base_value.get("repo")
        if not isinstance(head_repo_value, dict) or not isinstance(base_repo_value, dict):
            raise ValueError("F05_INVALID_PR_SNAPSHOT")
        h_sha = head_value.get("sha")
        h_repo = head_repo_value.get("full_name")
        b_sha = base_value.get("sha")
        b_repo = base_repo_value.get("full_name")
        b_ref = base_value.get("ref")
        count = value.get("changed_files")
        if not isinstance(h_sha, str) or not re.fullmatch(r"[a-fA-F0-9]{40}", h_sha):
            raise ValueError("F05_INVALID_PR_SNAPSHOT")
        if not isinstance(b_sha, str) or not re.fullmatch(r"[a-fA-F0-9]{40}", b_sha):
            raise ValueError("F05_INVALID_PR_SNAPSHOT")
        if not isinstance(h_repo, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", h_repo):
            raise ValueError("F05_INVALID_PR_SNAPSHOT")
        if b_repo != repository or b_ref != "main":
            raise ValueError("F05_INVALID_PR_SNAPSHOT")
        if type(count) is not int or not 1 <= count < 3000:
            raise ValueError("F05_INVALID_PR_SNAPSHOT")
        return h_sha, h_repo, b_sha, b_ref, b_repo, count

    # Parse the initial snapshot now too (and reject an absent base commit).
    original_snapshot = snapshot(pr)
    latest = _api_get(f"/repos/{repository}/pulls/{number}", token)
    # Preserve a specific reason for HEAD motion; all other inconsistencies
    # are snapshot drift and also require a new independent run.
    latest_snapshot = snapshot(latest)
    if latest_snapshot[0] != original_snapshot[0]:
        raise ValueError("F05_PR_HEAD_MOVED_RETRY_REQUIRED")
    if latest_snapshot != original_snapshot:
        raise ValueError("F05_PR_SNAPSHOT_CHANGED_RETRY_REQUIRED")
    print("F05_TRUSTED_PR_SOURCE_INSPECTION_PASS — read-only static source contract")


def main() -> int:
    try:
        inspect_pr(
            os.environ.get("GITHUB_REPOSITORY", ""),
            int(os.environ.get("PR_NUMBER", "0")),
            os.environ.get("GH_TOKEN", ""),
        )
    except Exception as exc:
        # Do not print user-controlled exception text or untrusted source data.
        print("F05_PR_SOURCE_INSPECTION_BLOCKED: " + type(exc).__name__)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
