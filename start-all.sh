#!/bin/bash

# 전체 시스템 시작 스크립트

echo "🚀 Starting Ad Impression Aggregation System..."

# 1. Docker Compose 서비스 시작
echo "📦 Starting all services..."
docker-compose up -d

# 2. 서비스 상태 확인
echo -e "\n⏳ Waiting for services to be ready..."
sleep 10

# 3. 서비스 상태 체크
echo -e "\n✅ Checking service status..."
docker-compose ps

# 4. Kafka 토픽 생성 (필요시)
echo -e "\n📝 Creating Kafka topics..."
docker exec kafka-broker kafka-topics --create --if-not-exists \
  --bootstrap-server localhost:9092 \
  --topic ad-impressions \
  --partitions 3 \
  --replication-factor 1 2>/dev/null || echo "Topic already exists"

# 5. 접속 URL 안내
echo -e "\n🌐 Service URLs:"
echo "  NiFi:             http://localhost:8080/nifi (admin/ctsBtRBKHRAx69EqUghvvgEvjnaLjFEB)"
echo "  Kafka UI:         http://localhost:8090"
echo "  Schema Registry:  http://localhost:8081"

echo -e "\n✨ All services started successfully!"
echo "Run './stop-all.sh' to stop all services"
