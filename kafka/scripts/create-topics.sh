#!/bin/bash

# Kafka 토픽 생성 스크립트
KAFKA_CONTAINER="kafka-broker"
KAFKA_INTERNAL_HOST="kafka:9093"

echo "Kafka 토픽 생성 시작..."

# ad-impressions 토픽 생성
echo "Creating ad-impressions topic..."
docker exec ${KAFKA_CONTAINER} kafka-topics --create \
  --bootstrap-server ${KAFKA_INTERNAL_HOST} \
  --topic ad-impressions \
  --partitions 3 \
  --replication-factor 1 \
  --if-not-exists

# 토픽 목록 확인
echo "토픽 목록 확인:"
docker exec ${KAFKA_CONTAINER} kafka-topics --list --bootstrap-server ${KAFKA_INTERNAL_HOST}

echo "토픽 생성 완료!"