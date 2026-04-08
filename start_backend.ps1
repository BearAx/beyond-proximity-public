# Start the FastAPI backend server
# Run from the project root: .\start_backend.ps1

$base    = $PSScriptRoot
$conda   = "C:\Users\m.mousatat\AppData\Local\miniconda3\Scripts\conda.exe"
$python  = "C:\Users\m.mousatat\AppData\Local\miniconda3\envs\semanticsplat\python.exe"

if (-not (Test-Path $python)) {
    Write-Host "ERROR: semanticsplat conda env not found. Run:" -ForegroundColor Red
    Write-Host "  conda create -n semanticsplat python=3.11 -y" -ForegroundColor Yellow
    Write-Host "  pip install -r backend/requirements.txt"       -ForegroundColor Yellow
    exit 1
}

$env:PYTHONPATH = $base
Write-Host "Starting SemanticSplat API server on http://127.0.0.1:8000 ..." -ForegroundColor Green
Write-Host "PLY files served at  http://127.0.0.1:8000/scenes/" -ForegroundColor Green
Write-Host "(conda env: semanticsplat)" -ForegroundColor Cyan
& $python -m backend.api.server
