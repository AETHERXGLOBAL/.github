"""F05-A01/A02 tests against original scanner with inert GitHub API.

The source guard is intentionally BLOCKING sensitive edits; a green check is
not a substitute for independently authenticated CODEOWNER/founder approval.
"""
from __future__ import annotations

import base64
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('execution_guard_under_test', ROOT/'profile/scripts/inspect_profile_pr.py')
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)
REPO='AETHERXGLOBAL/.github'
SHA='a'*40
BASE='1'*40


def inspect_changed(name: str, *extra: str):
    changed=(name,)+extra
    calls=[]
    def mock(path,token):
        if token != 'INERT_TEST_TOKEN':
            raise AssertionError('Unexpected real token')
        calls.append(path)
        if path.endswith('/pulls/29'):
            return {'base':{'repo':{'full_name':REPO},'ref':'main','sha':BASE},
                    'head':{'repo':{'full_name':REPO},'sha':SHA},
                    'changed_files':len(changed)}
        if '/pulls/29/files?' in path:
            page=int(path.split('page=')[-1]);
            return ([{'filename':x,'status':'modified'} for x in changed] if page==1 else [])
        for fp in guard.APPROVED_WORKFLOW_SHA256:
            if '/contents/'+fp+'?' in path:
                blob=(ROOT/fp).read_bytes()
                return {'type':'file','encoding':'base64','content':base64.b64encode(blob).decode()}
        raise AssertionError('Unexpected URL: '+path)
    with patch.object(guard,'_api_get',side_effect=mock):
        guard.inspect_pr(REPO,29,'INERT_TEST_TOKEN')
    return calls


class F05ExecutionClosure(unittest.TestCase):
    def test_f05_a01_four_original_false_greens_now_block(self):
        for path in (
            'profile/scripts/inspect_profile_pr.py',
            'profile/scripts/review_pr_lifecycle.sh',
            'profile/scripts/render_project_pulse.py',
            'profile/scripts/render_engineering_pulse.py',
        ):
            with self.subTest(path=path):
                with self.assertRaisesRegex(ValueError,'F05_PROTECTED_EXECUTABLE_CHANGE_REQUIRES_MANUAL_GATE'):
                    inspect_changed(path)

    def test_transitive_and_self_policy_changes_always_block(self):
        for path in ('profile/scripts/sanitize_project_pulse.py',
                     'profile/scripts/attacker.py','profile/scripts/new_dependency.sh',
                     '.github/actions/rogue/action.yml','pyproject.toml',
                     'profile/rogue.py', '.github/CODEOWNERS', 'profile/security/trust-policy.json'):
            with self.subTest(path=path):
                with self.assertRaisesRegex(ValueError,'F05_PROTECTED_EXECUTABLE_CHANGE_REQUIRES_MANUAL_GATE'):
                    inspect_changed(path)

    def test_modified_scanner_and_approved_workflow_do_not_self_authorize(self):
        with self.assertRaisesRegex(ValueError,'F05_PROTECTED_EXECUTABLE_CHANGE_REQUIRES_MANUAL_GATE'):
            inspect_changed('.github/workflows/update-project-pulse.yml',
                            'profile/scripts/inspect_profile_pr.py')

    def test_docs_and_nonexecuted_assets_pass_unchanged_workflow_contract(self):
        calls=inspect_changed('profile/docs/README.md','profile/assets/test.svg')
        self.assertTrue(any('/contents/.github/workflows/' in c for c in calls))

    def test_deleted_and_renamed_protected_scripts_block(self):
        self.assertTrue(guard.is_privileged_executable_path('profile/scripts/review_pr_lifecycle.sh'))
        self.assertTrue(guard.is_privileged_executable_path('profile/scripts/sneaky/new.json'))
        self.assertFalse(guard.is_privileged_executable_path('profile/assets/test.svg'))
        self.assertFalse(guard.is_privileged_executable_path('profile/tests/test_f05_execution_closure.py'))

    def test_f05_a02_edited_event_and_unfiltered_paths(self):
        workflow=(ROOT/'.github/workflows/inspect-profile-pr.yml').read_text()
        self.assertIn('pull_request_target:',workflow)
        self.assertIn('ready_for_review, edited]',workflow)
        self.assertNotIn('    paths:',workflow)
        self.assertIn('branches:\n      - main',workflow)
        self.assertIn('ref: main',workflow)
        self.assertIn('persist-credentials: false',workflow)
        self.assertNotIn('contents: write',workflow)
        self.assertNotIn('PROJECT_PULSE_READ_TOKEN',workflow)

    def test_pinned_new_workflow_bytes_match(self):
        import hashlib
        path='.github/workflows/inspect-profile-pr.yml'
        raw=(ROOT/path).read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),guard.APPROVED_WORKFLOW_SHA256[path])


if __name__=='__main__':
    unittest.main()
