#!/usr/bin/env bash
set -euo pipefail
packaging=$(cd -- "$(dirname -- "$0")" && pwd)
sources="$packaging/referances"
build="$packaging/build"
mkdir -p "$sources" "$build"

while IFS=$'\t' read -r checksum filename url; do
    [[ -z "$checksum" || "$checksum" == \#* ]] && continue
    if [[ ! -f "$sources/$filename" ]]; then
        curl --fail --location --retry 3 --connect-timeout 20 "$url" -o "$sources/$filename.part"
        mv -- "$sources/$filename.part" "$sources/$filename"
    fi
    if ! printf '%s  %s\n' "$checksum" "$sources/$filename" | sha256sum --check --status; then
        echo "Checksum mismatch: $filename" >&2
        exit 1
    fi
done < "$packaging/sources.tsv"

tmp=$(mktemp -d "$build/vendor.XXXXXX")
trap 'rm -rf "$tmp"' EXIT
tar -xf "$sources/nextkde-2ca59a1fbe7cd8c4b9c0b9fd960edca6788425c5.tar.gz" -C "$tmp"
(
    cd "$tmp/NextKde-2ca59a1fbe7cd8c4b9c0b9fd960edca6788425c5/services/data-service"
    export GOPATH="$build/go" GOTOOLCHAIN=local GOPROXY=https://proxy.golang.org
    go mod vendor
    go mod verify
    tar --sort=name --mtime='UTC 2026-10-20' --owner=0 --group=0 --numeric-owner \
        -czf "$sources/nextkde-vendor.tar.gz.part" vendor
    mv -- "$sources/nextkde-vendor.tar.gz.part" "$sources/nextkde-vendor.tar.gz"
)
cp "$packaging/patches/"*.patch "$packaging/licenses/"* "$sources/"
for spec in "$packaging/"*.spec; do
    rpmbuild -bs "$spec" --define "_topdir $build/rpmbuild" \
        --define "_sourcedir $sources" --define '_buildhost localhost' --define 'dist .fc46'
done
