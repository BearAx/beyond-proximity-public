# Benchmark + docs pipeline (PowerShell)
# Run from project root: .\run_all_docs.ps1

$base = $PSScriptRoot
$python = Join-Path $base ".venv\Scripts\python.exe"

if (-not (Test-Path $python)) {
    Write-Host "ERROR: .venv not found. Run:" -ForegroundColor Red
    Write-Host "  python -m venv .venv" -ForegroundColor Yellow
    Write-Host "  .\.venv\Scripts\pip install -r backend\requirements.txt" -ForegroundColor Yellow
    exit 1
}

$env:PYTHONPATH = $base
$env:MPLCONFIGDIR = Join-Path $base ".matplotlib"
New-Item -ItemType Directory -Force -Path $env:MPLCONFIGDIR | Out-Null

Write-Host "=============================================="
Write-Host "  SemanticSplat - full docs pipeline"
Write-Host "  Command: .\run_all_docs.ps1"
Write-Host "=============================================="
Write-Host ""

& $python (Join-Path $base "scripts\run_full_benchmark.py") @args
