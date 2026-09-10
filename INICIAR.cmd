@echo off
cd /d "%~dp0"
set "LAB_PYTHON=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if exist "%LAB_PYTHON%" (
  "%LAB_PYTHON%" -X utf8 iniciar.py
) else (
  py -3 -X utf8 iniciar.py
)
pause
