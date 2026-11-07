#!/usr/bin/env bash
# AETHER X GLOBAL: protected-branch-safe, recoverable review proposal lifecycle.
# Usage: review_pr_lifecycle.sh prepare|publish engineering|portfolio
# Never writes to main, force-pushes, auto-merges, or weakens branch protection.
set -euo pipefail

ACTION="${1:?prepare or publish required}"
MODE="${2:?engineering or portfolio required}"
case "$MODE" in
  engineering)
    BRANCH="automation/public-github-activity-review"
    FILE="profile/assets/aether-x-engineering-pulse.svg"
    TITLE="[REVIEW] Refresh public GitHub activity dashboard"
    BODY="Generated public-only activity telemetry. Requires human review and normal branch-protection checks before merge. No automatic publication or bypass."
    ;;
  portfolio)
    BRANCH="automation/live-portfolio-pulse-review"
    FILE="profile/assets/aether-x-live-project-pulse.svg"
    TITLE="[REVIEW] Refresh governed live portfolio pulse"
    BODY="Governed-source candidate requiring independent confirmation of source accessibility and public disclosure markers. No automatic merge or direct main push."
    ;;
  *) echo "REVIEW_UNSUPPORTED_MODE" >&2; exit 2;;
esac

case "$ACTION" in
  prepare)
    test -z "$(git status --porcelain)" || { echo "REVIEW_PREPARE_DIRTY_TREE" >&2; exit 1; }
    git fetch origin main
    if git ls-remote --exit-code --heads origin "$BRANCH" >/dev/null; then
      git fetch origin "$BRANCH"
      git switch -C "$BRANCH" FETCH_HEAD
      git -c user.name='github-actions[bot]' -c user.email='41898282+github-actions[bot]@users.noreply.github.com' merge --no-edit origin/main
    else
      git switch -C "$BRANCH" origin/main
    fi
    echo "REVIEW_BRANCH_PREPARED"
    ;;
  publish)
    test "$(git branch --show-current)" = "$BRANCH" || { echo "REVIEW_WRONG_BRANCH" >&2; exit 1; }
    case "$(git remote get-url origin)" in
      *x-access-token:*|*github_pat_*|*ghp_*) echo "REVIEW_TOKEN_IN_REMOTE_BLOCKED" >&2; exit 1;;
    esac
    git config user.name 'github-actions[bot]'
    git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
    if ! git diff --quiet -- "$FILE" || [[ -n "$(git ls-files --others --exclude-standard -- "$FILE")" ]]; then
      git add -- "$FILE"
      git commit -m "chore(profile): propose reviewed $MODE update"
    fi
    # A previous run may have pushed a branch but failed PR creation. Never use
    # working-tree cleanliness as a reason to skip pending review reconciliation.
    if git diff --quiet origin/main HEAD -- "$FILE"; then
      echo "REVIEW_NO_UNPUBLISHED_ASSET_DIFF"
      exit 0
    fi
    # No token-bearing Git remote: scoped GitHub CLI credential helper on hosted runners.
    if [[ -n "${GH_TOKEN:-}" ]]; then
      gh auth setup-git
    fi
    git push origin "HEAD:refs/heads/$BRANCH"
    : "${GITHUB_REPOSITORY:?required for bounded PR lookup}"
    current=$(gh pr list --repo "$GITHUB_REPOSITORY" --head "$BRANCH" --base main --state open --json number --jq '.[0].number // empty')
    if [[ -n "$current" ]]; then
      [[ "$current" =~ ^[0-9]+$ ]] || { echo "REVIEW_AMBIGUOUS_PR_LOOKUP" >&2; exit 1; }
      echo "REVIEW_EXISTING_PR=$current"
      exit 0
    fi
    if gh pr create --repo "$GITHUB_REPOSITORY" --base main --head "$BRANCH" --title "$TITLE" --body "$BODY"; then
      echo "REVIEW_PR_CREATED"
    else
      # A concurrent actor could have created the PR after our initial lookup.
      recovered=$(gh pr list --repo "$GITHUB_REPOSITORY" --head "$BRANCH" --base main --state open --json number --jq '.[0].number // empty')
      if [[ "$recovered" =~ ^[0-9]+$ ]]; then
        echo "REVIEW_PR_RECOVERED=$recovered"
      else
        echo "REVIEW_PR_CREATION_FAILED_RETRY_ON_NEXT_RUN" >&2
        exit 1
      fi
    fi
    ;;
  *) echo "REVIEW_UNSUPPORTED_ACTION" >&2; exit 2;;
esac
