# Start the FastAPI backend server
# Run from the project root: .\start_backend.ps1

$base = $PSScriptRoot
$python = Join-Path $base ".venv\Scripts\python.exe"

if (-not (Test-Path $python)) {
    Write-Host "ERROR: .venv not found. Run:" -ForegroundColor Red
    Write-Host "  python -m venv .venv" -ForegroundColor Yellow
    Write-Host "  .\.venv\Scripts\pip install -r backend\requirements.txt" -ForegroundColor Yellow
    exit 1
}

$env:PYTHONPATH = $base
Write-Host "Starting SemanticSplat API server on http://127.0.0.1:8000 ..." -ForegroundColor Green
Write-Host "PLY files served at  http://127.0.0.1:8000/scenes/" -ForegroundColor Green
& $python -m backend.api.server
