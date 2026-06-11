#!/usr/bin/env bash
# One command: benchmark + charts + MD report + project log + reasoning + demo video
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if [[ ! -d .venv ]]; then
  echo "Creating .venv…"
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate

export PYTHONPATH=.
export MPLCONFIGDIR="$ROOT/.matplotlib"
mkdir -p "$MPLCONFIGDIR"

echo "=============================================="
echo "  SemanticSplat — full docs pipeline"
echo "  Command: ./run_all_docs.sh"
echo "=============================================="
echo ""

python scripts/run_full_benchmark.py "$@"
