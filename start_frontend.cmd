@echo off
cd /d "%~dp0frontend"

where npm >nul 2>&1
if errorlevel 1 (
  echo ERROR: npm not found in PATH. Install Node.js 18+ and reopen the terminal.
  exit /b 1
)

if not exist "node_modules\" (
  echo Installing frontend dependencies...
  call npm install
  if errorlevel 1 exit /b 1
)

echo Starting SemanticSplat frontend on http://localhost:5173
call npm run dev
