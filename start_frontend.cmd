@echo off
cd /d "%~dp0frontend"
set "PATH=C:\Users\m.mousatat\AppData\Local\miniconda3\envs\pcg;%PATH%"

if not exist "C:\Users\m.mousatat\AppData\Local\miniconda3\envs\pcg\node.exe" (
  echo ERROR: Node.js not found in pcg conda env.
  exit /b 1
)

echo Starting SemanticSplat frontend on http://localhost:5173 ^(node from pcg env^)
call npm run dev
