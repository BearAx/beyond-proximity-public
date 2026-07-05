@echo off
REM Rebuild main.pdf with figures. Run from papers\beyond-proximity or repo root.
setlocal
cd /d "%~dp0"
set REPO=%~dp0..\..
set PYTHONPATH=%REPO%

REM MiKTeX is often not on PATH until terminal restart — auto-detect.
if not defined MIKTEX_BIN (
  if exist "%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe" (
    set "MIKTEX_BIN=%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64"
  ) else if exist "%ProgramFiles%\MiKTeX\miktex\bin\x64\pdflatex.exe" (
    set "MIKTEX_BIN=%ProgramFiles%\MiKTeX\miktex\bin\x64"
  )
)
if defined MIKTEX_BIN set "PATH=%MIKTEX_BIN%;%PATH%"

echo [1/5] Export figures...
python -B "%REPO%\scripts\export_paper_figures.py"
if errorlevel 1 exit /b 1

where pdflatex >nul 2>&1
if errorlevel 1 (
  echo ERROR: pdflatex not found. Install MiKTeX: winget install MiKTeX.MiKTeX
  exit /b 1
)

echo [2/5] pdflatex pass 1...
pdflatex -interaction=nonstopmode main.tex
if errorlevel 1 exit /b 1
echo [3/5] bibtex...
bibtex main
echo [4/5] pdflatex pass 2...
pdflatex -interaction=nonstopmode main.tex
echo [5/5] pdflatex pass 3...
pdflatex -interaction=nonstopmode main.tex
echo Done: %CD%\main.pdf
endlocal
