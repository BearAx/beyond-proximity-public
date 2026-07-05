# Start the MCP server (exposes infrastructure tools to Cursor AI)
# Run from the project root: .\start_mcp.ps1

$base = $PSScriptRoot
$python = Join-Path $base ".venv\Scripts\python.exe"

if (-not (Test-Path $python)) {
    Write-Host "ERROR: .venv not found. Run:" -ForegroundColor Red
    Write-Host "  python -m venv .venv" -ForegroundColor Yellow
    Write-Host "  .\.venv\Scripts\pip install -r backend\requirements.txt" -ForegroundColor Yellow
    exit 1
}

$env:PYTHONPATH = $base
Write-Host "Starting SemanticSplat MCP server on http://127.0.0.1:8001 ..." -ForegroundColor Cyan
& $python -m backend.mcp.server
