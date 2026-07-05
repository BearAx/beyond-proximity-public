@echo off
cd /d "%~dp0"
set "PYTHONPATH=%~dp0"
set "PYTHON=%~dp0.venv\Scripts\python.exe"

if not exist "%PYTHON%" (
  echo ERROR: .venv not found.
  echo Run: python -m venv .venv
  echo Then: .venv\Scripts\pip install -r backend\requirements.txt
  exit /b 1
)

echo Starting SemanticSplat API on http://127.0.0.1:8000
echo PLY files served at  http://127.0.0.1:8000/scenes/
echo.
"%PYTHON%" -m backend.api.server
