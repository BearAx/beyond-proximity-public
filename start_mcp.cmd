@echo off
cd /d "%~dp0"
set "PYTHONPATH=%~dp0"
set "PYTHON=C:\Users\m.mousatat\AppData\Local\miniconda3\envs\semanticsplat\python.exe"

if not exist "%PYTHON%" (
  echo ERROR: semanticsplat conda env not found.
  echo Run: conda create -n semanticsplat python=3.11 -y
  echo Then: pip install -r backend\requirements.txt
  exit /b 1
)

echo Starting SemanticSplat MCP on http://127.0.0.1:8001 ^(conda: semanticsplat^)
"%PYTHON%" -m backend.mcp.server
