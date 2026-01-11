# 진보당 크롤러 자동 실행 설정

진보당은 GitHub Actions IP가 차단되어 로컬에서만 크롤링 가능합니다.
컴퓨터 부팅 시 자동으로 `crawl_jinboparty.py`가 실행되도록 설정하는 방법입니다.

## Windows (집 컴퓨터) 설정

### 1. 시작 프로그램 폴더 열기
- `Win + R` 키를 누르고 `shell:startup` 입력 후 Enter

### 2. 바로가기 만들기
1. 열린 폴더에서 우클릭 → **새로 만들기** → **바로 가기**
2. 항목 위치 입력:
   ```
   pythonw "C:\Users\nikki\iCloudDrive\Work\personal\Against Apathy\party-news-weekly\crawl_jinboparty.py"
   ```
3. 이름: `진보당 크롤러`
4. **마침** 클릭

### 3. 환경 변수 설정 (필요한 경우)
시스템 환경 변수에 아래 값들이 설정되어 있어야 합니다:
- `NOTION_TOKEN`: Notion Integration Token
- `NOTION_DATABASE_ID`: Notion Database ID

설정 방법:
1. `Win + R` → `sysdm.cpl` → **고급** 탭 → **환경 변수**
2. **사용자 변수**에서 **새로 만들기** 클릭
3. 위 두 변수 추가

---

## macOS (회사 컴퓨터) 설정

### 1. LaunchAgent plist 파일 생성

터미널에서 아래 명령어 실행:

```bash
cat > ~/Library/LaunchAgents/com.partynews.jinboparty.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.partynews.jinboparty</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>crawl_jinboparty.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/YOUR_USERNAME/Library/Mobile Documents/com~apple~CloudDocs/Work/personal/Against Apathy/party-news-weekly</string>
    <key>RunAtLoad</key>
    <true/>
    <key>EnvironmentVariables</key>
    <dict>
        <key>NOTION_TOKEN</key>
        <string>YOUR_NOTION_TOKEN</string>
        <key>NOTION_DATABASE_ID</key>
        <string>YOUR_DATABASE_ID</string>
    </dict>
    <key>StandardOutPath</key>
    <string>/tmp/jinboparty_crawler.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/jinboparty_crawler_error.log</string>
</dict>
</plist>
EOF
```

### 2. 값 수정
plist 파일을 열어서 아래 값들을 실제 값으로 변경:
- `YOUR_USERNAME` → 맥 사용자 이름 (터미널에서 `whoami` 실행하면 확인 가능)
- `YOUR_NOTION_TOKEN` → Notion Integration Token
- `YOUR_DATABASE_ID` → Notion Database ID

편집 명령어:
```bash
nano ~/Library/LaunchAgents/com.partynews.jinboparty.plist
```

### 3. LaunchAgent 활성화
```bash
launchctl load ~/Library/LaunchAgents/com.partynews.jinboparty.plist
```

### 4. 확인
```bash
# 상태 확인
launchctl list | grep jinboparty

# 로그 확인
cat /tmp/jinboparty_crawler.log
```

### 5. 비활성화 (필요한 경우)
```bash
launchctl unload ~/Library/LaunchAgents/com.partynews.jinboparty.plist
```

---

## 수동 실행

자동 실행 외에 수동으로 실행하려면:

```bash
# 프로젝트 폴더로 이동
cd "C:\Users\nikki\iCloudDrive\Work\personal\Against Apathy\party-news-weekly"  # Windows
cd ~/Library/Mobile\ Documents/com~apple~CloudDocs/Work/personal/Against\ Apathy/party-news-weekly  # macOS

# 실행
python crawl_jinboparty.py
```

---

## 참고

- **GitHub Actions**: 진보당을 제외한 6개 정당은 하루 3회 (10:30, 15:30, 19:30 KST) 자동 크롤링
- **로컬 크롤러**: 진보당만 컴퓨터 부팅 시 1회 실행
- 중복 게시글은 자동으로 건너뜀 (Notion DB URL 체크)
