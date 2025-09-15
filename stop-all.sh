#!/bin/bash

# 전체 시스템 종료 스크립트

echo "🛑 Stopping Ad Impression Aggregation System..."

# 1. Docker Compose 서비스 종료
echo "📦 Stopping all services..."
docker-compose down

# 2. 볼륨 유지 여부 확인
read -p "Do you want to remove data volumes? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "🗑️ Removing volumes..."
    docker-compose down -v
    echo "✅ All volumes removed"
else
    echo "💾 Volumes preserved for next run"
fi

echo -e "\n✨ All services stopped successfully!"