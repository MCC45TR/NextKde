#!/usr/bin/env bash
set -euo pipefail
sync_script=$(realpath "$(dirname "$0")/../sync-upstream.sh")
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

git init -q --initial-branch=main "$tmp/upstream"
git -C "$tmp/upstream" config user.name Fixture
git -C "$tmp/upstream" config user.email fixture@example.invalid
printf 'base\n' > "$tmp/upstream/shared"
git -C "$tmp/upstream" add shared
git -C "$tmp/upstream" commit -qm base
git clone -q --bare "$tmp/upstream" "$tmp/fork.git"
git clone -q "$tmp/fork.git" "$tmp/work"
cd "$tmp/work"
git config user.name Fixture
git config user.email fixture@example.invalid
printf 'downstream packaging\n' > packaging
git add packaging
git commit -qm packaging
git push -q origin main

printf 'new upstream source\n' > "$tmp/upstream/new-source"
git -C "$tmp/upstream" add new-source
git -C "$tmp/upstream" commit -qm update
bash "$sync_script" "$tmp/upstream" > "$tmp/sync.log" 2>&1
test -f new-source
grep -qx 'downstream packaging' packaging
test "$(git --git-dir="$tmp/fork.git" rev-parse main)" = "$(git rev-parse HEAD)"
bash "$sync_script" "$tmp/upstream" >> "$tmp/sync.log" 2>&1

printf 'downstream edit\n' > shared
git add shared
git commit -qm 'local patch'
git push -q origin main
before=$(git rev-parse HEAD)
printf 'upstream edit\n' > "$tmp/upstream/shared"
git -C "$tmp/upstream" add shared
git -C "$tmp/upstream" commit -qm conflict
if bash "$sync_script" "$tmp/upstream" >> "$tmp/sync.log" 2>&1; then
    echo 'A conflicting sync unexpectedly succeeded.' >&2
    exit 1
fi
test "$(git rev-parse HEAD)" = "$before"
test "$(git --git-dir="$tmp/fork.git" rev-parse main)" = "$before"
test -z "$(git status --porcelain)"
grep -qx 'downstream edit' shared
echo 'PASS: upstream merges preserve downstream files; conflicts leave the remote unchanged.'
