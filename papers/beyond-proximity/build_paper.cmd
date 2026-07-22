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

echo [1/6] Export metric figures...
python -B "%REPO%\scripts\export_paper_figures.py" --out-dir "%CD%\figures"
if errorlevel 1 exit /b 1

echo [2/6] Export method and evidence figures...
python -B "%REPO%\scripts\export_academic_figures.py" --out-dir "%CD%\figures"
if errorlevel 1 exit /b 1

where pdflatex >nul 2>&1
if errorlevel 1 (
  echo ERROR: pdflatex not found. Install MiKTeX: winget install MiKTeX.MiKTeX
  exit /b 1
)

echo [3/6] pdflatex pass 1...
pdflatex -interaction=nonstopmode main.tex
if errorlevel 1 exit /b 1
echo [4/6] bibtex...
bibtex main
echo [5/6] pdflatex pass 2...
pdflatex -interaction=nonstopmode main.tex
echo [6/6] pdflatex pass 3...
pdflatex -interaction=nonstopmode main.tex
python -B "%REPO%\scripts\check_academic_paper.py"
if errorlevel 1 exit /b 1
echo Done: %CD%\main.pdf
endlocal
