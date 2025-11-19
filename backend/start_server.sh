#!/bin/bash

# Start the FastAPI backend server with auto-reload

echo "Starting AI CodeDoc Studio Backend Server..."
echo "=============================================="

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Error: Virtual environment not found at .venv"
    echo "Please create it first with: python3 -m venv .venv"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Check if required packages are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Start the server
echo "Starting uvicorn on http://0.0.0.0:8000"
echo "Press Ctrl+C to stop"
echo ""

uvicorn app.server:app --host 0.0.0.0 --port 8000 --reload
