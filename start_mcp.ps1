# Start the MCP server (exposes infrastructure tools to Cursor AI)
# Run from the project root: .\start_mcp.ps1

$base   = $PSScriptRoot
$python = "C:\Users\m.mousatat\AppData\Local\miniconda3\envs\semanticsplat\python.exe"

if (-not (Test-Path $python)) {
    Write-Host "ERROR: semanticsplat conda env not found. Run:" -ForegroundColor Red
    Write-Host "  conda create -n semanticsplat python=3.11 -y" -ForegroundColor Yellow
    Write-Host "  pip install -r backend/requirements.txt"       -ForegroundColor Yellow
    exit 1
}

$env:PYTHONPATH = $base
Write-Host "Starting SemanticSplat MCP server on http://127.0.0.1:8001 ..." -ForegroundColor Cyan
Write-Host "(conda env: semanticsplat)" -ForegroundColor Cyan
& $python -m backend.mcp.server
