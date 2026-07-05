# Start the Vite dev server for the frontend
# Run from the project root: .\start_frontend.ps1

$base = Join-Path $PSScriptRoot "frontend"

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: npm not found in PATH. Install Node.js 18+ and reopen the terminal." -ForegroundColor Red
    exit 1
}

if (-not (Test-Path (Join-Path $base "node_modules"))) {
    Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
    Push-Location $base
    npm install
    if ($LASTEXITCODE -ne 0) { Pop-Location; exit 1 }
    Pop-Location
}

Write-Host "Starting SemanticSplat frontend on http://localhost:5173 ..." -ForegroundColor Magenta
Set-Location $base
npm run dev
