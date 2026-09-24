#!/usr/bin/env bash
# One-time IMGCODE setup for the cloud workspace. Runs automatically
# when the codespace is created. The v0.3 tree interface is pure
# stdlib Python, so nothing needs installing -- this just verifies it.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 --version
cd v03-tree-interface
python3 -c "import validate, compose, compile, market_match; print('tree interface imports OK')"
echo "IMGCODE ready."
echo "Run the loop:  cd v03-tree-interface && python3 run_loop.py tree-ir/visibility-audit-tree.json"
