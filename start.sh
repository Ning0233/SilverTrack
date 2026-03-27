#!/usr/bin/env bash
# Start the SilverTrack backend (Flask) and frontend (React dev server).

set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"

echo "=== Starting SilverTrack Backend (Flask on :5000) ==="
cd "$ROOT/backend"
pip install -q -r requirements.txt
python app.py &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

echo ""
echo "=== Starting SilverTrack Frontend (React on :3000) ==="
cd "$ROOT/frontend"
npm install --silent
npm start &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

echo ""
echo "Backend:  http://localhost:5000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers."

wait
