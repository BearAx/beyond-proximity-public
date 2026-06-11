#!/usr/bin/env bash
# SemanticSplat — запуск всех сервисов на macOS/Linux
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if [[ ! -d .venv ]]; then
  echo "Создаю Python-окружение..."
  python3 -m venv .venv
fi

source .venv/bin/activate
export PYTHONPATH=.

if ! python -c "import fastapi" 2>/dev/null; then
  echo "Устанавливаю Python-зависимости..."
  pip install -r backend/requirements.txt
fi

if [[ ! -d frontend/node_modules ]]; then
  echo "Устанавливаю frontend-зависимости..."
  (cd frontend && npm install)
fi

mkdir -p scenes

# Подхватить .ply из scenes/input-data/ (если пользователь распаковал туда)
if compgen -G "scenes/input-data/*.ply" > /dev/null; then
  cp -n scenes/input-data/*.ply scenes/ 2>/dev/null || true
fi

echo "Запускаю Backend API (8000), MCP (8001), Frontend (5173)..."
python -m backend.api.server &
BACKEND_PID=$!
python -m backend.mcp.server &
MCP_PID=$!
(cd frontend && npm run dev) &
FRONTEND_PID=$!

cleanup() {
  echo "Останавливаю сервисы..."
  kill "$BACKEND_PID" "$MCP_PID" "$FRONTEND_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

PLY_COUNT=$(find scenes -maxdepth 1 -name '*.ply' 2>/dev/null | wc -l | tr -d ' ')

echo ""
echo "=============================================="
echo "  SemanticSplat запущен"
echo "=============================================="
echo ""
echo "  ОТКРОЙ В БРАУЗЕРЕ (главный адрес):"
echo "  -> http://localhost:5173"
echo ""
echo "  В интерфейсе:"
echo "    Scene ID: default  ->  Set"
echo "    PLY URL:  /scenes/ConferenceHall.ply  ->  Load"
echo ""
if [[ "$PLY_COUNT" -gt 0 ]]; then
  echo "  3D-сцены найдены: $PLY_COUNT файл(ов) в scenes/"
else
  echo "  ВНИМАНИЕ: нет .ply в scenes/ — 3D будет пустым"
  echo "  Положи файлы в scenes/ или scenes/input-data/"
fi
echo ""
echo "  Служебные адреса (не для браузера):"
echo "    Backend health: http://127.0.0.1:8000/api/health"
echo "    MCP (только Cursor): http://127.0.0.1:8001/mcp"
echo ""
echo "  Benchmark + docs (one command — prints links at the end):"
echo "    ./run_all_docs.sh"
echo ""
echo "  Docs (after ./run_all_docs.sh — START HERE):"
echo "    file://$ROOT/docs/README.md"
echo ""
echo "  Ctrl+C — остановить все сервисы"
echo "=============================================="
echo ""

# На macOS сразу открыть интерфейс в браузере
if [[ "$(uname -s)" == "Darwin" ]] && command -v open >/dev/null; then
  sleep 2
  open "http://localhost:5173" 2>/dev/null || true
fi

wait
