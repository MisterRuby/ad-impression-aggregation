# IPTV 광고 송출 로그 CSV 자동 생성기

IPTV 시스템에서 광고 송출 로그를 주기적으로 CSV 파일로 생성하는 Python 스크립트입니다.

## 주요 기능

- 광고 송출 로그 데이터 자동 생성
- CSV 파일 형태로 출력
- 스케줄링 기능 (시간별/일별/주별)
- 설정 파일을 통한 커스터마이징
- 오래된 파일 자동 정리
- 로깅 기능

## 설치 방법

1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

## 사용 방법

### 기본 실행 (스케줄러 모드)
```bash
python ad_log_generator.py
```

### 한 번만 실행
```bash
python ad_log_generator.py --once
```

### 특정 개수의 로그 생성
```bash
python ad_log_generator.py --once --count 500
```

### 커스텀 설정 파일 사용
```bash
python ad_log_generator.py --config my_config.json
```

## 설정 파일

첫 실행 시 `config.json` 파일이 자동으로 생성됩니다. 다음 항목들을 설정할 수 있습니다:

```json
{
  "output_directory": "./ad_logs",
  "file_prefix": "iptv_ad_log",
  "schedule_interval": "hourly",
  "max_files_to_keep": 30,
  "channels": [
    {"id": "CH001", "name": "KBS1"},
    {"id": "CH002", "name": "KBS2"}
  ],
  "advertisers": ["삼성전자", "LG전자", "현대자동차"],
  "regions": ["서울", "경기", "부산"],
  "device_types": ["STB", "Smart TV", "Mobile"]
}
```

### 설정 옵션 설명

- `output_directory`: CSV 파일이 저장될 디렉토리
- `file_prefix`: 생성되는 파일명의 접두사
- `schedule_interval`: 스케줄 간격 ("hourly", "daily", "weekly")
- `max_files_to_keep`: 보관할 최대 파일 개수
- `channels`: 채널 목록
- `advertisers`: 광고주 목록
- `regions`: 지역 목록
- `device_types`: 디바이스 타입 목록

## 출력 파일 형식

생성되는 CSV 파일에는 다음 컬럼들이 포함됩니다:

| 컬럼명 | 설명 |
|--------|------|
| timestamp | 송출 시간 |
| channel_id | 채널 ID |
| channel_name | 채널명 |
| ad_id | 광고 ID |
| ad_name | 광고명 |
| advertiser | 광고주 |
| duration | 광고 재생 시간(초) |
| viewer_count | 시청자 수 |
| region | 지역 |
| device_type | 디바이스 타입 |
| ad_position | 광고 위치 (pre-roll, mid-roll, post-roll) |
| campaign_id | 캠페인 ID |
| revenue | 매출액 |

## 로그 파일

실행 로그는 `ad_log_generator.log` 파일에 저장됩니다.

## 파일 구조

```
ad-impression-aggregation/
├── ad_log_generator.py      # 메인 스크립트
├── requirements.txt         # 패키지 의존성
├── config.json             # 설정 파일 (자동 생성)
├── ad_log_generator.log    # 로그 파일 (자동 생성)
├── ad_logs/               # 출력 디렉토리 (자동 생성)
│   ├── iptv_ad_log_20231215_120000.csv
│   └── iptv_ad_log_20231215_130000.csv
└── README.md              # 이 파일
```

## 스케줄 설정

- `hourly`: 매시간 정각에 실행
- `daily`: 매일 자정(00:00)에 실행
- `weekly`: 매주 월요일 자정에 실행

스케줄러는 백그라운드에서 계속 실행되며, Ctrl+C로 중단할 수 있습니다.

## 주의사항

- 스크립트는 샘플 데이터를 생성합니다. 실제 IPTV 시스템과 연동하려면 데이터 소스 부분을 수정해야 합니다.
- 파일 개수 제한 기능으로 디스크 공간 관리가 자동으로 이루어집니다.
- 설정 파일의 채널, 광고주 등 정보는 실제 환경에 맞게 수정하세요.