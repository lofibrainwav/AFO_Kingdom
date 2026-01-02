#!/usr/bin/env bash
set -euo pipefail
DIR="${1:-}"
if [ -z "$DIR" ] || [ ! -d "$DIR" ]; then
  echo "usage: $0 <artifacts_dir>"
  exit 1
fi

(
  cd "$DIR"
  find . -type f ! -name "manifest.sha256" ! -name "manifest.rel.sha256" -print0 \
    | LC_ALL=C sort -z \
    | xargs -0 shasum -a 256 \
    > manifest.rel.sha256

  shasum -a 256 -c manifest.rel.sha256
)

echo "sealed(rel): $DIR/manifest.rel.sha256"
