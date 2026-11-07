"""Isolated end-to-end Git/gh simulations of the actual review PR helper.

All remotes are temporary local bare repositories; no GitHub network or tokens.
"""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

HELPER = Path(__file__).resolve().parents[1] / 'scripts' / 'review_pr_lifecycle.sh'
ASSET = {
    'engineering': 'profile/assets/aether-x-engineering-pulse.svg',
    'portfolio': 'profile/assets/aether-x-live-project-pulse.svg',
}
BRANCH = {
    'engineering': 'automation/public-github-activity-review',
    'portfolio': 'automation/live-portfolio-pulse-review',
}


class ReviewPRLifecycle(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.remote = self.root / 'remote.git'
        self.seed = self.root / 'seed'
        self.mock = self.root / 'mock'
        self.mock.mkdir()
        self.state = self.root / 'state'
        self.state.mkdir()
        self.env = os.environ.copy()
        self.env['PATH'] = str(self.mock) + os.pathsep + self.env['PATH']
        self.env['GH_MOCK_STATE'] = str(self.state)
        self.env['GITHUB_REPOSITORY'] = 'AETHERXGLOBAL/.github'
        self.env.pop('GH_TOKEN', None)
        script = '''#!/usr/bin/env bash
set -euo pipefail
BRANCH=""
for ((i=1;i<=$#;i++)); do
  if [[ "${!i}" == "--head" ]]; then j=$((i+1)); BRANCH="${!j}"; fi
done
KEY="${BRANCH//\\//_}"
case "$1:$2" in
 auth:setup-git) exit 0;;
 pr:list) [[ -f "$GH_MOCK_STATE/pr_$KEY" ]] && echo 101 || :;;
 pr:create)
   echo "attempt:$KEY" >> "$GH_MOCK_STATE/attempts"
   if [[ "${GH_MOCK_DENY:-0}" == '1' ]]; then echo '403: permission denied' >&2; exit 1; fi
   if [[ "${GH_MOCK_RACE:-0}" == '1' ]]; then touch "$GH_MOCK_STATE/pr_$KEY"; exit 1; fi
   touch "$GH_MOCK_STATE/pr_$KEY"; echo 'https://github.com/AETHERXGLOBAL/.github/pull/101';;
 *) echo "UNEXPECTED_GH_COMMAND: $*" >&2; exit 9;;
esac
'''
        gh = self.mock / 'gh'
        gh.write_text(script)
        gh.chmod(0o755)
        self.git(self.root, 'init', '--bare', '--initial-branch=main', str(self.remote))
        self.git(self.root, 'clone', str(self.remote), str(self.seed))
        self.git(self.seed, 'config', 'user.email', 'test@localhost')
        self.git(self.seed, 'config', 'user.name', 'local-test')
        for file in ASSET.values():
            p = self.seed / file
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text('BASE\n')
        helper_target = self.seed / 'profile/scripts/review_pr_lifecycle.sh'
        helper_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(HELPER, helper_target)
        (self.seed / 'README.md').write_text('BASE\n')
        self.git(self.seed, 'add', '.')
        self.git(self.seed, 'commit', '-m', 'initial')
        self.git(self.seed, 'push', 'origin', 'HEAD:main')
        self.iteration = 0

    def git(self, cwd, *args):
        p = subprocess.run(['git', *args], cwd=cwd, text=True, capture_output=True, env=self.env)
        if p.returncode:
            raise AssertionError(f'git {args}: {p.stderr}')
        return p.stdout.strip()

    def run_cycle(self, mode, value=None, expected=0):
        self.iteration += 1
        work = self.root / f'run_{self.iteration}'
        self.git(self.root, 'clone', '--branch', 'main', str(self.remote), str(work))
        proc = subprocess.run(['bash', 'profile/scripts/review_pr_lifecycle.sh', 'prepare', mode], cwd=work, env=self.env, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        if value is not None:
            (work / ASSET[mode]).write_text(value + '\n')
        proc = subprocess.run(['bash', 'profile/scripts/review_pr_lifecycle.sh', 'publish', mode], cwd=work, env=self.env, capture_output=True, text=True)
        self.assertEqual(proc.returncode, expected, f'{proc.stdout}\n{proc.stderr}')
        return proc

    def attempts(self):
        p = self.state / 'attempts'
        return len(p.read_text().splitlines()) if p.exists() else 0

    def pr_path(self, mode):
        return self.state / ('pr_' + BRANCH[mode].replace('/', '_'))

    def test_unchanged_baseline_does_not_propose(self):
        self.assertIn('REVIEW_NO_UNPUBLISHED_ASSET_DIFF', self.run_cycle('engineering').stdout)
        self.assertEqual(self.attempts(), 0)

    def test_first_and_second_run_remain_idempotent(self):
        self.assertIn('REVIEW_PR_CREATED', self.run_cycle('engineering', 'FIRST').stdout)
        self.assertIn('REVIEW_EXISTING_PR', self.run_cycle('engineering', 'FIRST').stdout)
        self.assertIn('REVIEW_EXISTING_PR', self.run_cycle('engineering', 'SECOND').stdout)
        self.assertEqual(self.attempts(), 1)
        self.assertEqual(self.git(self.seed, 'show', 'main:' + ASSET['engineering']), 'BASE')

    def test_denied_create_recovers_on_unchanged_rerun_for_both_modes(self):
        for mode in ASSET:
            with self.subTest(mode=mode):
                self.env['GH_MOCK_DENY'] = '1'
                self.assertIn('REVIEW_PR_CREATION_FAILED_RETRY_ON_NEXT_RUN', self.run_cycle(mode, 'FIRST', expected=1).stderr)
                self.assertFalse(self.pr_path(mode).exists())
                self.assertIn('REVIEW_PR_CREATION_FAILED_RETRY_ON_NEXT_RUN', self.run_cycle(mode, 'FIRST', expected=1).stderr)
                self.env.pop('GH_MOCK_DENY')
                self.assertIn('REVIEW_PR_CREATED', self.run_cycle(mode, 'FIRST').stdout)
                self.assertTrue(self.pr_path(mode).exists())

    def test_existing_review_branch_and_main_advance(self):
        self.run_cycle('engineering', 'FIRST')
        (self.seed / 'README.md').write_text('ADVANCED\n')
        self.git(self.seed, 'add', 'README.md')
        self.git(self.seed, 'commit', '-m', 'advance-main')
        self.git(self.seed, 'push', 'origin', 'HEAD:main')
        self.assertIn('REVIEW_EXISTING_PR', self.run_cycle('engineering', 'FIRST').stdout)
        main = self.git(self.seed, 'rev-parse', 'main')
        probe = self.root / 'probe'
        self.git(self.root, 'clone', str(self.remote), str(probe))
        self.git(probe, 'merge-base', '--is-ancestor', main, f'origin/{BRANCH["engineering"]}')
        self.assertEqual(self.attempts(), 1)

    def test_existing_closed_pr_is_not_ignored(self):
        self.run_cycle('portfolio', 'FIRST')
        self.pr_path('portfolio').unlink()
        self.assertIn('REVIEW_PR_CREATED', self.run_cycle('portfolio', 'FIRST').stdout)
        self.assertEqual(self.attempts(), 2)

    def test_concurrent_pr_creation_race_is_reconciled(self):
        self.env['GH_MOCK_RACE'] = '1'
        self.assertIn('REVIEW_PR_RECOVERED', self.run_cycle('engineering', 'FIRST').stdout)
        self.assertEqual(self.attempts(), 1)

    def test_push_denied_fails_without_attempting_pr(self):
        hook = self.remote / 'hooks/pre-receive'
        hook.write_text('#!/bin/sh\nwhile read old new ref; do case "$ref" in refs/heads/automation/live-portfolio-pulse-review) exit 1;; esac; done\n')
        hook.chmod(0o755)
        self.run_cycle('portfolio', 'FIRST', expected=1)
        self.assertEqual(self.attempts(), 0)
        hook.unlink()
        self.assertIn('REVIEW_PR_CREATED', self.run_cycle('portfolio', 'FIRST').stdout)

    def test_wrong_branch_fails_closed(self):
        self.iteration += 1
        work = self.root / 'wrong'
        self.git(self.root, 'clone', '--branch', 'main', str(self.remote), str(work))
        p = subprocess.run(['bash', 'profile/scripts/review_pr_lifecycle.sh', 'publish', 'engineering'], cwd=work, env=self.env, capture_output=True, text=True)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('REVIEW_WRONG_BRANCH', p.stderr)

if __name__ == '__main__':
    unittest.main()
