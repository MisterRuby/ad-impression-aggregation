# NiFi를 통한 IPTV 광고 로그 처리 환경 구성

Apache NiFi를 Docker Compose로 구성하여 IPTV 광고 송출 로그 CSV 파일을 자동으로 읽고 처리하는 환경입니다.

## 디렉토리 구조

```
ad-impression-aggregation/
├── nifi/                              # NiFi 관련 파일들
│   ├── docker-compose.yml             # NiFi Docker Compose 설정
│   ├── .env                          # 환경 변수 설정
│   ├── config/                       # NiFi 설정 파일
│   │   └── logback.xml
│   ├── output/                       # NiFi 처리 결과 출력 디렉토리
│   └── NIFI_SETUP.md                 # 이 파일
├── iptv-ad-log-generator/             # 광고 로그 생성기
│   ├── ad_logs/                       # CSV 파일 생성 위치 (NiFi 입력 소스)
│   ├── ad_log_generator.py
│   └── config.json
```

## 사용 방법

### 1. NiFi 시작

```bash
# nifi 디렉토리로 이동
cd nifi

# Docker Compose로 NiFi 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f nifi
```

### 2. NiFi 웹 UI 접근

- **URL**: https://localhost:8443/nifi
- **사용자명**: admin
- **비밀번호**: ctsBtRBKHRAx69EqUghvvgEvjnaLjFEB

### 3. 광고 로그 생성기 실행

```bash
# 광고 로그 생성기 디렉토리로 이동
cd iptv-ad-log-generator

# 패키지 설치
pip install -r requirements.txt

# 매분마다 1000건 CSV 파일 생성 (스케줄러 모드)
python ad_log_generator.py

# 또는 한 번만 실행
python ad_log_generator.py --once
```

### 4. NiFi에서 CSV 파일 처리 플로우 구성

#### 기본 프로세서 구성 예시:

1. **GetFile** 프로세서
   - Input Directory: `/opt/nifi/nifi-current/data/input`
   - File Filter: `iptv_ad_log_.*\.csv`
   - Keep Source File: false
   - Minimum File Age: 1 sec

2. **ConvertRecord** 프로세서 (CSV → JSON)
   - Record Reader: CSVReader
   - Record Writer: JsonRecordSetWriter

3. **PutFile** 프로세서 (처리 결과 저장)
   - Directory: `/opt/nifi/nifi-current/data/output`

## 볼륨 마운트 설정

| 호스트 경로 | 컨테이너 경로 | 설명 |
|-------------|---------------|------|
| `../iptv-ad-log-generator/ad_logs` | `/opt/nifi/nifi-current/data/input` | CSV 입력 파일 (읽기 전용) |
| `./output` | `/opt/nifi/nifi-current/data/output` | 처리된 파일 출력 |
| `./config` | `/opt/nifi/nifi-current/conf` | NiFi 설정 파일 |

## 환경 변수 설정

`.env` 파일에서 다음 설정을 변경할 수 있습니다:

```env
NIFI_USERNAME=admin
NIFI_PASSWORD=ctsBtRBKHRAx69EqUghvvgEvjnaLjFEB
NIFI_HTTPS_PORT=8443
NIFI_HTTP_PORT=8080
```

## NiFi 플로우 템플릿 가이드

### CSV 파일 모니터링 및 처리 기본 플로우:

1. **GetFile**: CSV 파일 감지 및 읽기
2. **UpdateAttribute**: 파일 메타데이터 추가
3. **ConvertRecord**: CSV → JSON/Avro/Parquet 변환
4. **RouteOnAttribute**: 조건별 라우팅
5. **PutFile/PutElasticsearch/PutKafka**: 최종 저장/전송

### 고급 처리 옵션:

- **ValidateRecord**: 데이터 검증
- **QueryRecord**: SQL 쿼리를 통한 데이터 필터링/변환
- **PartitionRecord**: 채널별/지역별 데이터 분할
- **MergeRecord**: 여러 파일 병합

## 모니터링

### 로그 확인
```bash
# NiFi 컨테이너 로그
docker-compose logs nifi

# 컨테이너 내부 로그 파일
docker exec -it nifi-ad-processor tail -f /opt/nifi/nifi-current/logs/nifi-app.log
```

### 리소스 모니터링
```bash
# 컨테이너 리소스 사용량
docker stats nifi-ad-processor
```

## 문제 해결

### 1. 포트 충돌
다른 서비스가 8443/8080 포트를 사용 중인 경우, `.env` 파일에서 포트 변경

### 2. 메모리 부족
`docker-compose.yml`에서 JVM 힙 크기 조정:
```yaml
NIFI_JVM_HEAP_INIT: 4g
NIFI_JVM_HEAP_MAX: 4g
```

### 3. 볼륨 권한 문제
```bash
# 디렉토리 권한 설정
sudo chown -R 1000:1000 ./nifi-output ./nifi-config
```

## 확장 가능성

- **Kafka 연동**: 실시간 스트리밍 처리
- **Elasticsearch**: 검색 및 분석 기능
- **Prometheus/Grafana**: 모니터링 대시보드
- **Schema Registry**: 스키마 관리

## 중지 및 정리

```bash
# NiFi 중지
docker-compose down

# 볼륨까지 삭제 (주의: 데이터 손실)
docker-compose down -v

# 이미지 정리
docker image prune -f
```