#!/usr/bin/env python3
"""
자동 스케줄러: 하루 3회 정당 뉴스 크롤링
- 오전 10:30
- 오후 15:30
- 저녁 19:30
"""

import schedule
import time
import subprocess
import sys
from datetime import datetime


def run_crawler():
    """크롤러를 실행하고 결과를 출력"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'='*60}")
    print(f"[{timestamp}] 크롤링 시작...")
    print(f"{'='*60}\n")

    try:
        # main.py를 sample 모드로 실행 (각 정당당 최신 3개)
        result = subprocess.run(
            [sys.executable, "src/main.py", "sample"],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )

        print(result.stdout)
        if result.stderr:
            print("경고/에러:", result.stderr)

        if result.returncode == 0:
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 크롤링 완료 ✓")
        else:
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 크롤링 실패 (exit code: {result.returncode})")

    except Exception as e:
        print(f"에러 발생: {e}")

    print(f"{'='*60}\n")


def main():
    print("정당 뉴스 자동 크롤러 시작")
    print("스케줄:")
    print("  - 오전 10:30")
    print("  - 오후 15:30")
    print("  - 저녁 19:30")
    print("\n프로그램을 종료하려면 Ctrl+C를 누르세요.\n")

    # 스케줄 등록
    schedule.every().day.at("10:30").do(run_crawler)
    schedule.every().day.at("15:30").do(run_crawler)
    schedule.every().day.at("19:30").do(run_crawler)

    # 시작 즉시 한 번 실행 (선택사항)
    print("초기 크롤링을 실행합니다...")
    run_crawler()

    # 스케줄러 루프
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # 1분마다 체크
    except KeyboardInterrupt:
        print("\n\n스케줄러를 종료합니다.")


if __name__ == "__main__":
    main()
