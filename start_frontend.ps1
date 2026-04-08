# Start the Vite dev server for the frontend
# Run from the project root: .\start_frontend.ps1

$base = $PSScriptRoot
$npm  = "C:\Users\m.mousatat\AppData\Local\miniconda3\envs\pcg\npm.cmd"
$pcgEnv = "C:\Users\m.mousatat\AppData\Local\miniconda3\envs\pcg"

# Add node to PATH so npm postinstall scripts can find it
$env:PATH = "$pcgEnv;$env:PATH"

if (-not (Test-Path $npm)) {
    Write-Host "ERROR: Node.js not found in pcg conda env ($pcgEnv)" -ForegroundColor Red
    exit 1
}

Write-Host "Starting SemanticSplat frontend on http://localhost:5173 ..." -ForegroundColor Magenta
Write-Host "(node from pcg conda env)" -ForegroundColor Cyan
Set-Location "$base\frontend"
& $npm run dev
