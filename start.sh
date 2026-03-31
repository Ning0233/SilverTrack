#!/usr/bin/env bash
# Start the SilverTrack backend (Flask) and frontend (React dev server).

set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"

port_in_use() {
	lsof -nP -iTCP:"$1" -sTCP:LISTEN >/dev/null 2>&1
}

pick_backend_port() {
	local preferred=5001
	local candidate

	if ! port_in_use "$preferred"; then
		echo "$preferred"
		return 0
	fi

	for candidate in $(seq 5002 5010); do
		if ! port_in_use "$candidate"; then
			echo "$candidate"
			return 0
		fi
	done

	return 1
}

pick_frontend_port() {
	local preferred=3000
	local candidate

	if ! port_in_use "$preferred"; then
		echo "$preferred"
		return 0
	fi

	for candidate in $(seq 3001 3010); do
		if ! port_in_use "$candidate"; then
			echo "$candidate"
			return 0
		fi
	done

	return 1
}

cleanup() {
	echo ""
	echo "Stopping SilverTrack services..."

	if [ -n "${FRONTEND_PID:-}" ] && kill -0 "$FRONTEND_PID" 2>/dev/null; then
		kill "$FRONTEND_PID" 2>/dev/null || true
	fi

	if [ -n "${BACKEND_PID:-}" ] && kill -0 "$BACKEND_PID" 2>/dev/null; then
		kill "$BACKEND_PID" 2>/dev/null || true
	fi
}

BACKEND_PORT="$(pick_backend_port)" || {
	echo "No available backend port found in range 5001-5010."
	exit 1
}

FRONTEND_PORT="$(pick_frontend_port)" || {
	echo "No available frontend port found in range 3000-3010."
	exit 1
}

if [ "$BACKEND_PORT" != "5001" ]; then
	echo "Port 5001 is busy. Using backend port :$BACKEND_PORT instead."
fi

if [ "$FRONTEND_PORT" != "3000" ]; then
	echo "Port 3000 is busy. Using frontend port :$FRONTEND_PORT instead."
fi

trap cleanup INT TERM EXIT

echo "=== Starting SilverTrack Backend (Flask on :$BACKEND_PORT) ==="
cd "$ROOT/backend"
if [ ! -d ".venv" ]; then
	python3 -m venv .venv
fi

source .venv/bin/activate
python3 -m pip install -q --upgrade pip
python3 -m pip install -q -r requirements.txt
PORT="$BACKEND_PORT" python3 app.py &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

echo ""
echo "=== Starting SilverTrack Frontend (React on :$FRONTEND_PORT) ==="
cd "$ROOT/frontend"
npm install --silent
PORT="$FRONTEND_PORT" REACT_APP_API_PROXY_TARGET="http://localhost:$BACKEND_PORT" npm start &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

echo ""
echo "Backend:  http://localhost:$BACKEND_PORT"
echo "Frontend: http://localhost:$FRONTEND_PORT"
echo ""
echo "Press Ctrl+C to stop both servers."

wait
