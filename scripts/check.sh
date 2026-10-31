#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
export PYTHONDONTWRITEBYTECODE=1

python3 -m unittest discover -s "$root/tests" -p 'test_*.py'
node --test "$root/tests/landing_node_test.mjs"
"$root/tests/build_test.sh"
