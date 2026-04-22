@echo off
setlocal enabledelayedexpansion
pushd "%~dp0"
title Building AiSlop Orchestrator EXE

echo [1/3] Preparing environment...
if not exist "venv" (
    echo Creating virtual environment in %CD%...
    python -m venv venv
)
echo Installing/Updating dependencies...
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install -r requirements.txt

if %ERRORLEVEL% neq 0 (
    echo [ERROR] Failed to install dependencies!
    popd
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/3] Building Portable EXE...
echo This might take a minute...

if exist "PapatzisSpotter.spec" (
    venv\Scripts\python.exe -m PyInstaller --noconfirm PapatzisSpotter.spec
) else (
    venv\Scripts\python.exe -m PyInstaller --onefile --windowed --name "PapatzisSpotter" --icon=icon.ico main.py
)

if %ERRORLEVEL% neq 0 (
    echo [ERROR] Build failed!
    popd
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [3/3] Finalizing...
if exist "dist\PapatzisSpotter.exe" (
    echo Success! EXE is ready in launcher\dist\
    echo Copying to project root for easy access...
    copy /Y "dist\PapatzisSpotter.exe" "..\PapatzisSpotter.exe"
    echo Done! You can now run PapatzisSpotter.exe from the project root.
) else (
    echo [ERROR] Build succeeded but PapatzisSpotter.exe not found in dist folder!
)

popd
pause
