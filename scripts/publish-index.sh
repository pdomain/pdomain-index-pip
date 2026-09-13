#!/usr/bin/env bash
# Regenerate the simple index and publish it to the gh-pages branch.
#
# This replaces the regen workflow. GitHub Pages must be configured to serve
# from the gh-pages branch ("deploy from a branch"), not from a workflow
# artifact: the artifact API only accepts uploads from inside a GitHub Actions
# run, so it cannot be driven from a developer machine.
#
# Usage:
#   ./scripts/publish-index.sh            # regenerate and publish
#   DRY_RUN=1 ./scripts/publish-index.sh  # build and diff, push nothing
#
# Needs a GitHub token with read access to the org's releases, which is what
# the index is built from. `gh auth token` supplies it.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

DRY_RUN=${DRY_RUN:-0}
PAGES_BRANCH=${PAGES_BRANCH:-gh-pages}
WORKTREE="$(mktemp -d)"
SITE="$(mktemp -d)"
trap 'git worktree remove --force "$WORKTREE" 2>/dev/null || true; rm -rf "$SITE"' EXIT

if [ -z "${GH_TOKEN:-}" ]; then
    GH_TOKEN="$(gh auth token)"
    export GH_TOKEN
fi

echo "==> Regenerating the simple index"
make regen OUT="$SITE/simple"

cat > "$SITE/index.html" <<'HTML'
<!DOCTYPE html>
<html><head><title>pdomain-index-pip</title></head><body>
<h1>pdomain-index-pip</h1>
<p>Self-hosted PEP 503 simple Python package index for the
pdomain Python repos under
<a href="https://github.com/pdomain">pdomain</a>.</p>
<p>The index lives at <a href="simple/">simple/</a>.</p>
<p>Source: <a href="https://github.com/pdomain/pdomain-index-pip">github.com/pdomain/pdomain-index-pip</a></p>
</body></html>
HTML

# Pages serves exactly what the branch contains, and Jekyll would otherwise
# skip directories beginning with an underscore.
touch "$SITE/.nojekyll"

echo "==> Preparing the $PAGES_BRANCH worktree"
git fetch origin "$PAGES_BRANCH" --quiet 2>/dev/null || true
if git rev-parse --verify --quiet "origin/$PAGES_BRANCH" >/dev/null; then
    git worktree add --quiet "$WORKTREE" "origin/$PAGES_BRANCH" --detach
else
    echo "    $PAGES_BRANCH does not exist yet; creating it empty"
    git worktree add --quiet --detach "$WORKTREE"
    git -C "$WORKTREE" checkout --orphan "$PAGES_BRANCH"
    git -C "$WORKTREE" rm -rq --cached . 2>/dev/null || true
fi

find "$WORKTREE" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
cp -a "$SITE/." "$WORKTREE/"

cd "$WORKTREE"
git add -A
if git diff --cached --quiet; then
    echo "==> Index is unchanged; nothing to publish."
    exit 0
fi

echo "==> Changes to publish:"
git diff --cached --stat | tail -20

if [ "$DRY_RUN" = "1" ]; then
    echo "==> DRY_RUN=1; not committing or pushing."
    exit 0
fi

# The published branch carries only generated output and no pre-commit
# config, so the hook would abort the commit looking for one.
export PRE_COMMIT_ALLOW_NO_CONFIG=1
git commit -qm "chore(index): regenerate the simple index

Published from a developer machine by scripts/publish-index.sh. The
scheduled regen workflow was removed; this script is the whole path now."

git push --quiet origin "HEAD:$PAGES_BRANCH"
echo "==> Published to $PAGES_BRANCH."
echo "    https://pdomain.github.io/pdomain-index-pip/simple/"
