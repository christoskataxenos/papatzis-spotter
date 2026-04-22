@echo off
setlocal
title AiSlop Orchestrator Loader

echo [1/3] Checking Launcher Environment...
if not exist "launcher\venv" (
    echo Creating launcher virtual environment...
    python -m venv launcher\venv
)

echo [2/3] Updating Launcher Dependencies...
launcher\venv\Scripts\python.exe -m pip install -q -r launcher\requirements.txt

echo [3/3] Starting Orchestrator...
start /b launcher\venv\Scripts\pythonw.exe launcher\main.py

echo.
echo Orchestrator started! You can close this window.
timeout /t 3 > nul
exit
