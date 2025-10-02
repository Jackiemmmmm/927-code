#!/bin/bash

# 停止所有微服务

echo "🛑 Stopping all services..."

# 停止占用端口的进程
for PORT in 8000 8001 8002; do
    PID=$(lsof -ti :$PORT)
    if [ -n "$PID" ]; then
        echo "   Stopping service on port $PORT (PID: $PID)"
        kill -9 $PID 2>/dev/null
    else
        echo "   No service running on port $PORT"
    fi
done

echo ""
echo "✅ All services stopped!"
echo ""
echo "To start again, run: ./start-gateway-architecture.sh"
