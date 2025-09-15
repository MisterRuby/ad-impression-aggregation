#!/usr/bin/env python3
"""
IPTV 광고 송출 로그 CSV 자동 생성 스크립트

이 스크립트는 IPTV 시스템에서 광고 송출 로그를 주기적으로 CSV 파일로 생성합니다.
"""

import csv
import os
import json
import random
import schedule
import time
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Optional
from pathlib import Path


@dataclass
class AdImpressionLog:
    """광고 송출 로그 데이터 모델"""
    timestamp: str
    channel_id: str
    channel_name: str
    ad_id: str
    ad_name: str
    advertiser: str
    duration: int  # 초 단위
    viewer_count: int
    region: str
    device_type: str
    ad_position: str  # pre-roll, mid-roll, post-roll
    campaign_id: str
    revenue: float


class AdLogGenerator:
    """광고 로그 생성 및 CSV 출력 클래스"""

    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self) -> dict:
        """설정 파일 로드"""
        default_config = {
            "output_directory": "./ad_logs",
            "file_prefix": "iptv_ad_log",
            "schedule_interval": "minutely",  # minutely, hourly, daily, weekly
            "max_files_to_keep": 30,
            "channels": [
                {"id": "CH001", "name": "KBS1"},
                {"id": "CH002", "name": "KBS2"},
                {"id": "CH003", "name": "MBC"},
                {"id": "CH004", "name": "SBS"},
                {"id": "CH005", "name": "tvN"}
            ],
            "advertisers": [
                "삼성전자", "LG전자", "현대자동차", "SK텔레콤", "KB금융",
                "신한은행", "롯데", "CJ", "네이버", "카카오"
            ],
            "regions": ["서울", "경기", "부산", "대구", "인천", "광주", "대전", "울산"],
            "device_types": ["STB", "Smart TV", "Mobile", "Tablet", "PC"]
        }

        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                print(f"설정 파일 로드 실패: {e}, 기본 설정 사용")
        else:
            # 기본 설정 파일 생성
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, ensure_ascii=False, indent=2)
            print(f"기본 설정 파일 생성: {self.config_file}")

        return default_config

    def generate_sample_logs(self, count: int = 100) -> List[AdImpressionLog]:
        """샘플 광고 송출 로그 데이터 생성"""
        logs = []
        base_time = datetime.now() - timedelta(hours=1)

        for i in range(count):
            # 랜덤한 시간 간격으로 로그 생성
            log_time = base_time + timedelta(minutes=random.randint(0, 60))

            channel = random.choice(self.config["channels"])
            advertiser = random.choice(self.config["advertisers"])

            log = AdImpressionLog(
                timestamp=log_time.strftime("%Y-%m-%d %H:%M:%S"),
                channel_id=channel["id"],
                channel_name=channel["name"],
                ad_id=f"AD{random.randint(1000, 9999)}",
                ad_name=f"{advertiser} 광고 {random.randint(1, 10)}",
                advertiser=advertiser,
                duration=random.choice([15, 30, 60, 90]),
                viewer_count=random.randint(1000, 50000),
                region=random.choice(self.config["regions"]),
                device_type=random.choice(self.config["device_types"]),
                ad_position=random.choice(["pre-roll", "mid-roll", "post-roll"]),
                campaign_id=f"CMP{random.randint(100, 999)}",
                revenue=round(random.uniform(100, 5000), 2)
            )
            logs.append(log)

        # 시간순 정렬
        logs.sort(key=lambda x: x.timestamp)
        return logs

    def create_csv_file(self, logs: List[AdImpressionLog]) -> str:
        """CSV 파일 생성"""
        # 출력 디렉토리 생성
        output_dir = Path(self.config["output_directory"])
        output_dir.mkdir(exist_ok=True)

        # 파일명 생성
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.config['file_prefix']}_{timestamp}.csv"
        file_path = output_dir / filename

        # CSV 파일 작성
        with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
            if logs:
                fieldnames = list(asdict(logs[0]).keys())
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # 헤더 작성
                writer.writeheader()

                # 데이터 작성
                for log in logs:
                    writer.writerow(asdict(log))

        print(f"CSV 파일 생성: {file_path} ({len(logs)} 건)")
        return str(file_path)

    def cleanup_old_files(self):
        """오래된 파일 정리"""
        output_dir = Path(self.config["output_directory"])
        if not output_dir.exists():
            return

        # 파일 목록을 생성 시간순으로 정렬
        csv_files = list(output_dir.glob(f"{self.config['file_prefix']}_*.csv"))
        csv_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

        # 설정된 개수를 초과하는 파일 삭제
        max_files = self.config.get("max_files_to_keep", 30)
        if len(csv_files) > max_files:
            files_to_delete = csv_files[max_files:]
            for file_path in files_to_delete:
                try:
                    file_path.unlink()
                except Exception as e:
                    print(f"파일 삭제 실패 {file_path}: {e}")

    def generate_and_save_logs(self, log_count: Optional[int] = None):
        """로그 생성 및 저장 실행"""
        try:
            if log_count is None:
                log_count = 10000  # 기본적으로 10000건 생성

            # 로그 데이터 생성
            logs = self.generate_sample_logs(log_count)

            # CSV 파일 생성
            csv_file = self.create_csv_file(logs)

            # 오래된 파일 정리
            self.cleanup_old_files()

        except Exception as e:
            print(f"로그 생성 중 오류 발생: {e}")

    def start_scheduler(self):
        """스케줄러 시작"""
        interval = self.config.get("schedule_interval", "minutely")

        if interval == "minutely":
            schedule.every().minute.do(self.generate_and_save_logs)
            print("스케줄 설정: 매분 로그 생성")
        elif interval == "hourly":
            schedule.every().hour.do(self.generate_and_save_logs)
            print("스케줄 설정: 매시간 로그 생성")
        elif interval == "daily":
            schedule.every().day.at("00:00").do(self.generate_and_save_logs)
            print("스케줄 설정: 매일 자정 로그 생성")
        elif interval == "weekly":
            schedule.every().monday.at("00:00").do(self.generate_and_save_logs)
            print("스케줄 설정: 매주 월요일 자정 로그 생성")
        else:
            print(f"지원하지 않는 스케줄 간격: {interval}")
            return

        print("광고 로그 생성 스케줄러 시작")

        # 즉시 한 번 실행
        self.generate_and_save_logs()

        # 스케줄 실행
        while True:
            schedule.run_pending()
            time.sleep(1)  # 1초마다 체크


def main():
    """메인 함수"""
    import argparse

    parser = argparse.ArgumentParser(description='IPTV 광고 송출 로그 CSV 생성기')
    parser.add_argument('--config', default='config.json', help='설정 파일 경로')
    parser.add_argument('--once', action='store_true', help='한 번만 실행하고 종료')
    parser.add_argument('--count', type=int, help='생성할 로그 개수')

    args = parser.parse_args()

    generator = AdLogGenerator(args.config)

    if args.once:
        # 한 번만 실행
        generator.generate_and_save_logs(args.count)
    else:
        # 스케줄러 모드로 실행
        try:
            generator.start_scheduler()
        except KeyboardInterrupt:
            print("사용자에 의해 스케줄러 중지됨")


if __name__ == "__main__":
    main()