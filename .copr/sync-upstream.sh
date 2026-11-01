#!/usr/bin/env bash
set -euo pipefail

[[ $(git branch --show-current) == main ]] || { echo 'Check out main first.' >&2; exit 1; }
git diff --quiet
git diff --cached --quiet
before=$(git rev-parse HEAD)
git fetch --no-tags "${1:-https://github.com/NextKde/NextKde.git}" refs/heads/main
if ! git merge --no-edit FETCH_HEAD; then
    git merge --abort
    echo 'Upstream conflicts with downstream changes; nothing was pushed.' >&2
    exit 1
fi
git diff --check "$before" HEAD
git push origin HEAD:main
