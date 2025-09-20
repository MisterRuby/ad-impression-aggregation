# IPTV 광고 노출 데이터 집계 파이프라인

## 프로젝트 개요

이 프로젝트는 IPTV 광고 노출 데이터를 실시간으로 처리하고 집계하는 완전한 데이터 파이프라인입니다. 광고 노출 로그를 생성, 처리, 저장, 집계하여 분석용 API를 제공합니다.

## 시스템 아키텍처

```text
[CSV Files] → [NiFi] → [Kafka] → [Druid] → [API Server]
```

### 데이터 플로우

1. **데이터 수집**: Apache NiFi가 CSV 파일을 모니터링하고 JSON으로 변환
2. **스트림 처리**: Kafka를 통해 실시간 데이터 스트리밍
3. **데이터 저장**: Druid가 Kafka 토픽에서 데이터를 수집하고 분석 가능한 형태로 저장
4. **API 제공**: Spring Boot API 서버가 Druid에서 집계된 데이터를 REST API로 제공

## 주요 컴포넌트

### 1. Apache NiFi

**포트**: 8443 (HTTPS), 8080 (HTTP)

**역할**: 데이터 ETL 및 실시간 처리

**주요 플로우**:

- `GetFile`: CSV 파일 모니터링
- `SplitRecord`: CSV 레코드 분할
- `ConvertRecord`: CSV → JSON 변환
- `PublishKafka`: Kafka 토픽으로 데이터 전송

### 2. Apache Kafka

**포트**: 9092 (External), 9093 (Internal)

**역할**: 실시간 스트림 처리

**주요 토픽**:

- `ad-impressions`: 광고 노출 데이터

**관련 서비스**:

- **Zookeeper**: Kafka 클러스터 코디네이션 (포트: 2181)
- **Kafka UI**: 웹 기반 관리 인터페이스 (포트: 8090)

### 3. Apache Druid

**포트**:

- Router: 8888 (통합 접점)
- Coordinator: 8082
- Broker: 8083
- Historical: 8084
- MiddleManager: 8085

**역할**: 실시간 분석 데이터베이스

**아키텍처**:

- **Coordinator**: 클러스터 관리 및 세그먼트 할당
- **Broker**: 쿼리 라우팅 및 결과 병합
- **Historical**: 과거 데이터 세그먼트 서빙
- **MiddleManager**: 실시간 인덱싱 작업 관리
- **Router**: 클라이언트 요청 라우팅

**데이터소스**: `ad-impressions`

**수집 방식**: Kafka Supervisor를 통한 실시간 수집

**스키마**:

```json
{
  "timestampSpec": {
    "column": "impression_time",
    "format": "auto"
  },
  "dimensionsSpec": {
    "dimensions": [
      "impression_id",
      "ad_id",
      "segment",
      "kafka.timestamp",
      "kafka.topic",
      "channel_id",
      "region_code"
    ]
  },
  "primaryKeyDimensions": ["impression_id"]
}
```

**특징**:

- 시간당 세그먼트 분할 (`segmentGranularity: "hour"`)
- 중복 제거 활성화 (`deduplicateRows: true`)
- PostgreSQL 메타데이터 저장소

### 4. API Server (`api-server/`)

**기술스택**: Kotlin + Spring Boot

**포트**: 8723

**역할**: 집계된 데이터 API 제공

**주요 엔드포인트**:

#### `/api/analytics/channels`

- 채널별 광고 노출량 집계
- GroupBy 쿼리를 통한 channel_id별 카운트

#### `/api/analytics/regions`

- 지역별 광고 노출량 집계
- GroupBy 쿼리를 통한 region_code별 카운트

**Druid 연동**:

- Base URL: `http://localhost:8888` (Druid Router)
- REST API를 통한 GroupBy 쿼리 실행
- 조회 기간: 2024-01-01 ~ 2025-12-31

**응답 형식**:

```json
{
  "success": true,
  "data": [
    {
      "channel_id": "CH001",
      "count": 1542
    }
  ],
  "message": "3 개 채널의 노출량을 조회했습니다."
}
```

## 환경 설정

### 메모리 및 CPU 할당

| 서비스              | 메모리 | CPU       | 설명          |
| ------------------- | ------ | --------- | ------------- |
| NiFi                | 4GB    | 2.0 cores | ETL 처리      |
| Druid Coordinator   | 512MB  | -         | 클러스터 관리 |
| Druid Broker        | 1GB    | -         | 쿼리 처리     |
| Druid Historical    | 1GB    | -         | 데이터 서빙   |
| Druid MiddleManager | 1GB    | -         | 인덱싱        |
| Kafka               | 1GB    | -         | 스트림 처리   |
| PostgreSQL          | -      | -         | 메타데이터    |

### 네트워크

모든 서비스는 `ad-impression-aggregation` 브리지 네트워크에서 통신합니다.

### 볼륨 마운트

```yaml
# NiFi
./iptv-ad-log-generator/ad_logs:/opt/nifi/nifi-current/data/input
./nifi/output:/opt/nifi/nifi-current/data/output

# Druid
druid_shared:/opt/shared  # 세그먼트 및 로그 공유
```

## 실행 방법

### 1. 전체 스택 시작

```bash
docker-compose up -d
```

### 2. 테스트 데이터 생성

```bash
cd iptv-ad-log-generator
python ad_log_generator.py --once --count 1000
```

### 3. 데이터 파이프라인 확인

- NiFi UI: https://localhost:8443/nifi
- Kafka UI: http://localhost:8090
- Druid Router: http://localhost:8888
- API Server: http://localhost:8723/api/analytics/channels

## 모니터링 및 헬스체크

모든 주요 서비스에 헬스체크가 구성되어 있습니다:

- **Zookeeper**: ruok 명령어
- **Kafka**: broker-api-versions 확인
- **PostgreSQL**: pg_isready
- **Druid 서비스들**: `/status/health` 엔드포인트

## 데이터 보존 정책

- **Kafka**: 24시간 로그 보존
- **Druid**: 로컬 스토리지에 영구 보존
- **PostgreSQL**: 메타데이터 영구 보존

## 확장성 고려사항

1. **Kafka**: 파티션 수 증가로 처리량 향상 가능
2. **Druid**: Historical 노드 추가로 쿼리 성능 향상
3. **NiFi**: 클러스터 모드로 확장 가능
4. **API Server**: 로드 밸런서 뒤에 다중 인스턴스 배포

## 문제 해결

### 일반적인 이슈

1. **Druid 서비스 시작 실패**: PostgreSQL과 Zookeeper가 먼저 ready 상태인지 확인
2. **Kafka 연결 실패**: 네트워크 설정 및 advertised.listeners 확인
3. **NiFi 플로우 실행 실패**: 입력 디렉토리 권한 및 CSV 파일 형식 확인

### 로그 확인

```bash
# 특정 서비스 로그 확인
docker logs druid-coordinator
docker logs kafka-broker
docker logs nifi-ad-processor

# 모든 서비스 상태 확인
docker-compose ps
```

이 문서는 전체 데이터 파이프라인의 구조와 각 컴포넌트의 역할을 이해하는 데 도움이 됩니다. 추가적인 설정이나 문제 해결이 필요한 경우 각 컴포넌트별 상세 문서를 참조하세요.
