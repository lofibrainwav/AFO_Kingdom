#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mypy --config-file mypy_gate.ini .
