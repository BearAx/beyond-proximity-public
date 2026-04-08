@echo off
setlocal
cd /d "%~dp0"

echo ========================================
echo  SemanticSplat — starting all services
echo ========================================
echo   API       http://127.0.0.1:8000
echo   MCP       http://127.0.0.1:8001
echo   Frontend  http://localhost:5173
echo ========================================
echo.

rem Separate windows so each process logs are visible; close a window to stop that service.
start "SemanticSplat API (8000)" cmd /k "%~dp0start_backend.cmd"
timeout /t 1 /nobreak >nul

start "SemanticSplat MCP (8001)" cmd /k "%~dp0start_mcp.cmd"
timeout /t 1 /nobreak >nul

start "SemanticSplat Frontend (5173)" cmd /k "%~dp0start_frontend.cmd"

echo Launched 3 windows. Close each window to stop that service.
echo.
pause
