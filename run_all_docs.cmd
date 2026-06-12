@echo off
setlocal
cd /d "%~dp0"

set "PYTHON=%~dp0.venv\Scripts\python.exe"
if not exist "%PYTHON%" (
  echo ERROR: .venv not found.
  echo Run: python -m venv .venv
  echo Then: .venv\Scripts\pip install -r backend\requirements.txt
  exit /b 1
)

set "PYTHONPATH=%~dp0"
set "MPLCONFIGDIR=%~dp0.matplotlib"
if not exist "%MPLCONFIGDIR%" mkdir "%MPLCONFIGDIR%"

echo ==============================================
echo   SemanticSplat - full docs pipeline
echo   Command: run_all_docs.cmd
echo ==============================================
echo.

"%PYTHON%" scripts\run_full_benchmark.py %*
