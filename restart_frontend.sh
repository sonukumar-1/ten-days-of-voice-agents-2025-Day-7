#!/bin/bash

# Kill existing next/node processes related to frontend (be careful not to kill vscode)
# echo "Killing existing frontend processes..."
# pkill -f "next-server" || true

# Start the frontend
echo "Starting frontend server..."
cd frontend
nohup pnpm dev > frontend_debug.log 2>&1 &

echo "Frontend server started. Logs are being written to frontend/frontend_debug.log"
echo "Tail of the log:"
sleep 5
tail -n 20 frontend_debug.log
