#!/usr/bin/env bash
# Runner for local progressive push automation
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$REPO_ROOT"
export PYTHONPATH="$REPO_ROOT:${PYTHONPATH:-}"
echo "=== Running MCP Agent Hub Daily Automation ==="
python3 automation/daily_push.py --ci
