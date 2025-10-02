#!/bin/bash

# 启动所有微服务

# 使用项目的 Python 虚拟环境
PYTHON="../.venv/bin/python"

echo "Starting Appointments Service on port 8001..."
cd appointments-service
$PYTHON main.py > /tmp/appointments-service.log 2>&1 &
APPOINTMENTS_PID=$!

cd ..

echo "Starting Items Service on port 8002..."
cd items-service
$PYTHON main.py > /tmp/items-service.log 2>&1 &
ITEMS_PID=$!

cd ..

echo "All services started!"
echo "Appointments Service PID: $APPOINTMENTS_PID (log: /tmp/appointments-service.log)"
echo "Items Service PID: $ITEMS_PID (log: /tmp/items-service.log)"
echo ""
echo "To stop services, run: kill $APPOINTMENTS_PID $ITEMS_PID"
echo ""
echo "Health checks:"
echo "- Appointments: http://localhost:8001/health"
echo "- Items: http://localhost:8002/health"
echo ""
echo "API Documentation:"
echo "- Appointments: http://localhost:8001/docs"
echo "- Items: http://localhost:8002/docs"
echo ""
echo "Waiting for services to be ready..."
sleep 3

# 测试服务是否启动成功
curl -s http://localhost:8001/health && echo " ✓ Appointments service is healthy"
curl -s http://localhost:8002/health && echo " ✓ Items service is healthy"
