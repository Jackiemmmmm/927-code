#!/bin/bash

# 启动 API Gateway 架构
# 包括：API Gateway (8000) + Appointments Service (8001) + Items Service (8002)

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON="$SCRIPT_DIR/.venv/bin/python"

echo "🚀 Starting Microservices Architecture with API Gateway..."
echo ""

# 启动 Appointments Service
echo "📦 Starting Appointments Service (port 8001)..."
cd "$SCRIPT_DIR/services/appointments-service"
$PYTHON main.py > /tmp/appointments-service.log 2>&1 &
APPOINTMENTS_PID=$!
echo "   ✓ Appointments Service started (PID: $APPOINTMENTS_PID)"

# 启动 Items Service
echo "📦 Starting Items Service (port 8002)..."
cd "$SCRIPT_DIR/services/items-service"
$PYTHON main.py > /tmp/items-service.log 2>&1 &
ITEMS_PID=$!
echo "   ✓ Items Service started (PID: $ITEMS_PID)"

# 启动 API Gateway
echo "🌐 Starting API Gateway (port 8000)..."
cd "$SCRIPT_DIR"
$PYTHON -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/api-gateway.log 2>&1 &
GATEWAY_PID=$!
echo "   ✓ API Gateway started (PID: $GATEWAY_PID)"

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 5

echo ""
echo "🔍 Health Checks:"

# Test Appointments Service
if curl -s http://localhost:8001/health > /dev/null 2>&1; then
    echo "   ✓ Appointments Service is healthy (http://localhost:8001)"
else
    echo "   ✗ Appointments Service failed (check log: /tmp/appointments-service.log)"
fi

# Test Items Service
if curl -s http://localhost:8002/health > /dev/null 2>&1; then
    echo "   ✓ Items Service is healthy (http://localhost:8002)"
else
    echo "   ✗ Items Service failed (check log: /tmp/items-service.log)"
fi

# Test Gateway
if curl -s http://localhost:8000/api/v1/utils/health-check/ > /dev/null 2>&1; then
    echo "   ✓ API Gateway is healthy (http://localhost:8000)"
else
    echo "   ✗ API Gateway failed (check log: /tmp/api-gateway.log)"
fi

echo ""
echo "📚 API Documentation:"
echo "   - API Gateway: http://localhost:8000/docs"
echo "   - Appointments Service: http://localhost:8001/docs"
echo "   - Items Service: http://localhost:8002/docs"

echo ""
echo "🔌 Service URLs:"
echo "   - Frontend should connect to: http://localhost:8000"
echo "   - Appointments API (via Gateway): http://localhost:8000/api/v1/appointments"
echo "   - Items API (via Gateway): http://localhost:8000/api/v1/items"

echo ""
echo "📝 Process IDs:"
echo "   - API Gateway: $GATEWAY_PID"
echo "   - Appointments Service: $APPOINTMENTS_PID"
echo "   - Items Service: $ITEMS_PID"

echo ""
echo "🛑 To stop all services:"
echo "   kill $GATEWAY_PID $APPOINTMENTS_PID $ITEMS_PID"

echo ""
echo "📄 Logs:"
echo "   - API Gateway: /tmp/api-gateway.log"
echo "   - Appointments: /tmp/appointments-service.log"
echo "   - Items: /tmp/items-service.log"

echo ""
echo "✅ All services are running!"
