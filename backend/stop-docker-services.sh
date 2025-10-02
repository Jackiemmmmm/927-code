#!/bin/bash

# Stop all Docker services

echo "🛑 Stopping Docker services..."

cd "$(dirname "$0")"

docker compose -f docker-compose.microservices.yml down

echo ""
echo "✅ All Docker services stopped!"
echo ""
echo "💡 To start again: ./start-docker-services.sh"
echo "💡 To remove volumes: docker compose -f docker-compose.microservices.yml down -v"
