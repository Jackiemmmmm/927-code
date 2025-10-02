#!/bin/bash

# Start all microservices using Docker Compose

echo "🐳 Starting Microservices in Docker..."
echo ""

cd "$(dirname "$0")"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found. Using default values."
    echo "   Create a .env file with your configuration for production use."
    echo ""
fi

# Build and start services
echo "📦 Building Docker images..."
docker compose -f docker-compose.microservices.yml build

echo ""
echo "🚀 Starting services..."
docker compose -f docker-compose.microservices.yml up -d

echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 10

echo ""
echo "🔍 Checking service status..."
docker compose -f docker-compose.microservices.yml ps

echo ""
echo "🔍 Health Checks:"

# Check db
if docker compose -f docker-compose.microservices.yml ps | grep -q "db.*healthy"; then
    echo "   ✓ Database is healthy"
else
    echo "   ⚠ Database status unknown"
fi

# Check appointments-service
if docker compose -f docker-compose.microservices.yml ps | grep -q "appointments-service.*healthy"; then
    echo "   ✓ Appointments Service is healthy"
else
    echo "   ⚠ Appointments Service status unknown"
fi

# Check items-service
if docker compose -f docker-compose.microservices.yml ps | grep -q "items-service.*healthy"; then
    echo "   ✓ Items Service is healthy"
else
    echo "   ⚠ Items Service status unknown"
fi

# Check api-gateway
if docker compose -f docker-compose.microservices.yml ps | grep -q "api-gateway.*healthy"; then
    echo "   ✓ API Gateway is healthy"
else
    echo "   ⚠ API Gateway status unknown"
fi

echo ""
echo "📚 Service URLs:"
echo "   - API Gateway: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - Appointments Service: http://localhost:8001"
echo "   - Items Service: http://localhost:8002"
echo "   - PostgreSQL: localhost:5432"

echo ""
echo "📝 Useful Commands:"
echo "   - View logs: docker-compose -f docker-compose.microservices.yml logs -f"
echo "   - Stop services: ./stop-docker-services.sh"
echo "   - View specific service logs: docker-compose -f docker-compose.microservices.yml logs -f <service-name>"

echo ""
echo "✅ All services started!"
