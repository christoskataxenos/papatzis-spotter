#!/bin/bash

# AiSlop Orchestrator Loader for Linux/macOS
# -----------------------------------------

# Navigate to the project root (one level up from scripts/)
cd "$(dirname "$0")/.."

echo "[1/3] Checking Launcher Environment..."
if [ ! -d "launcher/venv" ]; then
    echo "Creating launcher virtual environment..."
    python3 -m venv launcher/venv
fi

echo "[2/3] Updating Launcher Dependencies..."
./launcher/venv/bin/pip install -q -r launcher/requirements.txt

echo "[3/3] Starting Orchestrator..."
# We run the python script. Note: PyQt5 requires an X11/Wayland display server.
./launcher/venv/bin/python3 launcher/main.py &

echo ""
echo "Orchestrator started! You can close this terminal."
sleep 3
exit
