#!/usr/bin/env bash
# AETHER X GLOBAL - trusted-main-only automation, untrusted asset-branch isolation.
# Execution always originates in a clean canonical main checkout, never a bot branch.
set -euo pipefail

ACTION="${1:?prepare or publish required}"
MODE="${2:?engineering or portfolio required}"
case "$MODE" in
  engineering)
    BRANCH='automation/public-github-activity-review'
    FILE='profile/assets/aether-x-engineering-pulse.svg'
    TITLE='[REVIEW] Refresh public GitHub activity dashboard'
    BODY='Generated public-only activity telemetry. Requires human review and normal branch-protection checks before merge. No automatic publication or bypass.'
    ;;
  portfolio)
    BRANCH='automation/live-portfolio-pulse-review'
    FILE='profile/assets/aether-x-live-project-pulse.svg'
    TITLE='[REVIEW] Refresh governed live portfolio pulse'
    BODY='Governed-source candidate requiring independent confirmation of source accessibility and public disclosure markers. No automatic merge or direct main push.'
    ;;
  *) echo 'REVIEW_UNSUPPORTED_MODE' >&2; exit 2;;
esac

BASE="$(pwd -P)"
WORK_ROOT="${RUNNER_TEMP:-$(dirname "$BASE")/aether-profile-worktrees}"
WORKTREE="$WORK_ROOT/aether-review-$MODE"

# These controls run *before* touching a lower-trust branch.
trusted_main() {
  [[ "$(git -C "$BASE" branch --show-current)" == main ]] || {
    echo 'REVIEW_TRUSTED_MAIN_REQUIRED' >&2; exit 1;
  }
  [[ "$(git -C "$BASE" rev-parse HEAD)" == "$(git -C "$BASE" rev-parse refs/remotes/origin/main)" ]] || {
    echo 'REVIEW_MAIN_HEAD_CHANGED_STOP' >&2; exit 1;
  }
  [[ "$(git -C "$BASE" ls-tree HEAD -- "$FILE")" == '100644 blob '* ]] || {
    echo 'REVIEW_MAIN_ASSET_NOT_REGULAR_FILE' >&2; exit 1;
  }
  [[ "$(git -C "$BASE" ls-tree HEAD -- 'profile/scripts/review_pr_lifecycle.sh')" == '100644 blob '* ]] || {
    echo 'REVIEW_MAIN_HELPER_NOT_REGULAR_FILE' >&2; exit 1;
  }
}

# Exactly one regular asset file may differ from current main in the review branch.
# This excludes branch-controlled scripts, workflow definitions, symlinks and deletions.
validate_review_tree() {
  [[ -d "$WORKTREE" ]] || { echo 'REVIEW_WORKTREE_MISSING' >&2; exit 1; }
  local changed path record
  changed="$(git -C "$WORKTREE" diff --name-only refs/remotes/origin/main HEAD --)"
  if [[ -n "$changed" && "$changed" != "$FILE" ]]; then
    echo 'REVIEW_UNTRUSTED_BRANCH_CHANGE_BLOCKED' >&2; exit 1
  fi
  record="$(git -C "$WORKTREE" ls-tree HEAD -- "$FILE")"
  [[ "$record" == '100644 blob '* ]] || {
    echo 'REVIEW_UNTRUSTED_ASSET_TYPE_BLOCKED' >&2; exit 1;
  }
  [[ ! -L "$WORKTREE/$FILE" ]] || {
    echo 'REVIEW_UNTRUSTED_ASSET_SYMLINK_BLOCKED' >&2; exit 1;
  }
  changed="$(git -C "$WORKTREE" status --porcelain --untracked-files=all)"
  [[ -z "$changed" || "$changed" == " M $FILE" ]] || {
    echo 'REVIEW_UNEXPECTED_WORKTREE_CHANGES_BLOCKED' >&2; exit 1;
  }
}

case "$ACTION" in
  prepare)
    [[ -z "$(git status --porcelain --untracked-files=all)" ]] || {
      echo 'REVIEW_PREPARE_DIRTY_TRUSTED_TREE' >&2; exit 1;
    }
    git fetch origin main
    trusted_main
    [[ ! -e "$WORKTREE" ]] || { echo 'REVIEW_PREPARE_WORKTREE_ALREADY_EXISTS' >&2; exit 1; }
    mkdir -p "$WORK_ROOT"
    if git ls-remote --exit-code --heads origin "$BRANCH" >/dev/null; then
      git fetch origin "refs/heads/$BRANCH:refs/remotes/origin/$BRANCH"
      git worktree add --detach "$WORKTREE" "refs/remotes/origin/$BRANCH"
      # Merge *inside the asset-only worktree*, never execute its tracked code.
      git -C "$WORKTREE" -c user.name='github-actions[bot]' \
        -c user.email='41898282+github-actions[bot]@users.noreply.github.com' \
        merge --no-edit refs/remotes/origin/main
    else
      git worktree add --detach "$WORKTREE" refs/remotes/origin/main
    fi
    validate_review_tree
    [[ "$(git rev-parse HEAD)" == "$(git rev-parse origin/main)" ]] || {
      echo 'REVIEW_MAIN_CODE_DRIFT_BLOCKED' >&2; exit 1;
    }
    echo 'REVIEW_BRANCH_PREPARED_TRUSTED_MAIN'
    ;;
  publish)
    trusted_main
    validate_review_tree
    [[ -f "$BASE/$FILE" && ! -L "$BASE/$FILE" ]] || {
      echo 'REVIEW_GENERATED_ASSET_INVALID' >&2; exit 1;
    }
    if ! cmp -s "$BASE/$FILE" "$WORKTREE/$FILE"; then
      cp -- "$BASE/$FILE" "$WORKTREE/$FILE"
      git -C "$WORKTREE" add -- "$FILE"
      git -C "$WORKTREE" -c user.name='github-actions[bot]' \
        -c user.email='41898282+github-actions[bot]@users.noreply.github.com' \
        commit -m "chore(profile): propose reviewed $MODE update"
    fi
    validate_review_tree
    if git -C "$WORKTREE" diff --quiet refs/remotes/origin/main HEAD -- "$FILE"; then
      echo 'REVIEW_NO_UNPUBLISHED_ASSET_DIFF'
      exit 0
    fi
    if [[ -n "${GH_TOKEN:-}" ]]; then
      gh auth setup-git
    fi
    git -C "$WORKTREE" push origin "HEAD:refs/heads/$BRANCH"
    : "${GITHUB_REPOSITORY:?required for bounded PR lookup}"
    current=$(gh pr list --repo "$GITHUB_REPOSITORY" --head "$BRANCH" --base main --state open --json number --jq '.[0].number // empty')
    if [[ -n "$current" ]]; then
      [[ "$current" =~ ^[0-9]+$ ]] || { echo 'REVIEW_AMBIGUOUS_PR_LOOKUP' >&2; exit 1; }
      echo "REVIEW_EXISTING_PR=$current"
      exit 0
    fi
    if gh pr create --repo "$GITHUB_REPOSITORY" --base main --head "$BRANCH" --title "$TITLE" --body "$BODY"; then
      echo 'REVIEW_PR_CREATED'
    else
      recovered=$(gh pr list --repo "$GITHUB_REPOSITORY" --head "$BRANCH" --base main --state open --json number --jq '.[0].number // empty')
      if [[ "$recovered" =~ ^[0-9]+$ ]]; then
        echo "REVIEW_PR_RECOVERED=$recovered"
      else
        echo 'REVIEW_PR_CREATION_FAILED_RETRY_ON_NEXT_RUN' >&2
        exit 1
      fi
    fi
    ;;
  *) echo 'REVIEW_UNSUPPORTED_ACTION' >&2; exit 2;;
esac
