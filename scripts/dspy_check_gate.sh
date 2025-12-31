#!/usr/bin/env bash
set -euo pipefail

# Run the Gate Check
poetry run python scripts/dspy_mipro_training_gate.py
