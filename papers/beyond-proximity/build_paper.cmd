@echo off
REM Rebuild main.pdf with figures. Run from papers\beyond-proximity or repo root.
setlocal EnableDelayedExpansion
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

echo [1/6] Export evidence-backed table rows...
python -B "%REPO%\scripts\export_academic_tables.py" --out-dir "%CD%\tables"
if errorlevel 1 exit /b 1

echo [2/6] Export evidence-backed paper figures...
python -B "%REPO%\scripts\export_academic_figures.py" --out-dir "%CD%\figures"
if errorlevel 1 exit /b 1

where pdflatex >nul 2>&1
if errorlevel 1 (
  if not defined TECTONIC_EXE (
    for /r "%USERPROFILE%\.codex\plugins\cache\openai-bundled\latex" %%T in (tectonic.exe) do (
      if exist "%%T" set "TECTONIC_EXE=%%T"
    )
  )
  if not defined TECTONIC_EXE (
    echo ERROR: neither pdflatex nor bundled Tectonic was found.
    exit /b 1
  )
  echo [3/3] Compile with bundled Tectonic...
  "!TECTONIC_EXE!" -X compile --outdir . --outfmt pdf --untrusted main.tex
  if errorlevel 1 exit /b 1
  python -B "%REPO%\scripts\check_academic_paper.py"
  if errorlevel 1 exit /b 1
  echo Done: %CD%\main.pdf
  exit /b 0
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
