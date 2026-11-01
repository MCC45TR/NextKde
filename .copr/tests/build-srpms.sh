#!/usr/bin/env bash
set -euo pipefail
packaging=$(cd -- "$(dirname "$0")/.." && pwd)
bash -n "$packaging/build-srpms.sh" "$packaging/sync-upstream.sh"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
cp "$packaging/build-srpms.sh" "$tmp/build-srpms.sh"
mkdir "$tmp/referances"
printf 'corrupt source\n' > "$tmp/referances/fixture.tar.gz"
checksum=$(printf 'expected source\n' | sha256sum | cut -d ' ' -f 1)
printf '%s\tfixture.tar.gz\thttps://invalid.example/unused\n' "$checksum" > "$tmp/sources.tsv"
if bash "$tmp/build-srpms.sh" > "$tmp/guard.log" 2>&1; then
    echo 'A corrupt archive was accepted.' >&2
    exit 1
fi
grep -q 'Checksum mismatch: fixture.tar.gz' "$tmp/guard.log"
grep -qx 'corrupt source' "$tmp/referances/fixture.tar.gz"
test -z "$(find "$tmp/build" -mindepth 1 -print -quit)"
echo 'PASS: source checksum mismatch stops before extraction or build.'
