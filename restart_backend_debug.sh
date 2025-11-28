#!/bin/bash

# Kill existing python agent processes
echo "Killing existing python agent processes..."
pkill -f "src.agent" || true

# Wait a moment
sleep 2

# Start the agent with logging
echo "Starting backend agent with debug logging..."
cd backend
nohup uv run python -m src.agent dev > ../backend_debug.log 2>&1 &

echo "Backend agent started. Logs are being written to backend_debug.log"
echo "Tail of the log:"
sleep 3
tail -n 20 ../backend_debug.log
