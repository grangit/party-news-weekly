# party-news-weekly handoff

## 목적

- 여러 정당 사이트의 목록을 자동 수집해 Notion DB에 적재
- Notion DB 형태: `정당 / 카테고리 / 제목 / 날짜 / 링크`
- 상세 페이지 본문을 Notion 페이지에 문단 블록으로 저장
- 실행 주기: 매일 10시 / 18시 / 02시 (3회)

## 현재 상태 요약

- 크롤러 엔트리: `src/main.py`
- 타깃 목록: `config/sources.json`
- 실행 예:
  - 전체: `python3 src/main.py --sample 20`
  - Notion 업로드: `python3 src/main.py --sample 5 --notion`
  - 특정 사이트: `python3 src/main.py --only jinboparty --sample 10`
  - 특정 카테고리: `python3 src/main.py --only-category 논평 --sample 10`
  - 특정 id: `python3 src/main.py --only-id jinbo_category_286 --sample 10`

## 구현된 사이트별 파서

- 기본소득당: `/news/briefing`, `/news/press`(언론보도 외부 링크)
- 사회민주당: `/news/briefing` (카드형/onclick 대응)
- 조국혁신당: JS 렌더링 → API(`api.rebuildingkoreaparty.kr/api/board/list`)로 수집
  - 현재 categoryId=7 고정 + URL slug 필터링
- 진보당: 목록 텍스트 깨짐 → 상세 페이지에서 제목/날짜 재수집
  - `js_board_view('id')` → read URL 생성
  - `img_list_item` 카드형(보도자료) 대응
- 노동당: KBoard 목록 파싱(브리핑/논평 page_id 별도)
- 녹색당: press/event/statement/statement2/address
  - statement/statement2 모두 category=논평
- 정의당: board_view 링크 수집 (bbs_code=JS21, 브리핑룸)

## Notion 업로드

- 환경변수 필요:
  - `NOTION_TOKEN`
  - `NOTION_DATABASE_ID` (예: `2e1c9c3e833b803b8accf5fb620224bb`)
- DB 속성명(정확히):
  - 제목(Title), 정당(Text), 카테고리(Text), 날짜(Date), 링크(URL)
- 업로드 동작:
  - `--notion` 옵션 사용 시 업로드
  - 링크 기준 중복 체크 후 생성
  - 상세 페이지 본문을 문단 블록으로 추가
  - 날짜가 없으면 상세 페이지에서 보정

## 최근 개선 사항 (2026-01-11)

- **Selenium 기반 JavaScript 렌더링 크롤러 추가**
  - 조국혁신당과 진보당은 JavaScript로 콘텐츠를 렌더링하는 사이트
  - `selenium` 패키지를 추가하여 브라우저 자동화로 본문 추출
  - `fetch_with_selenium()` 함수로 JS 렌더링된 페이지 처리
  - Chrome WebDriver 필요 (headless 모드로 실행)

- **사이트별 본문 셀렉터 개선**
  - 조국혁신당: `.ck-content`, `.editor` 셀렉터 추가 (CKEditor 기반)
  - 진보당: `.content_box` 셀렉터 추가
  - `fetch_detail_for_notion()`이 사이트별로 Selenium 사용 여부 자동 판단

- **테스트 결과**
  - 조국혁신당: 본문 추출 성공 (12개 문단)
  - 진보당: 본문 추출 성공 (7개 문단)
  - 날짜 추출도 정상 작동

- **Notion 2000자 제한 처리**
  - Notion API는 rich_text 블록당 2000자 제한이 있음
  - `build_paragraph_blocks()` 함수가 긴 문단을 문장 단위로 자동 분할
  - 문장 경계를 기준으로 2000자 이하 청크로 나눔

- **Notion Select 속성 타입 지원**
  - "정당"과 "카테고리" 필드를 Notion의 Select 타입으로 설정 가능
  - `notion_create_page()`가 DB 스키마를 분석하여 자동으로 적절한 형식 사용
  - Text 타입과 Select 타입 모두 지원

- **날짜 필터링 기능**
  - `--date-from YYYY-MM-DD` 옵션으로 특정 날짜 이후 항목만 수집
  - 예: `--date-from 2026-01-01`은 2026년 1월 1일 이후 게시물만 수집
  - 날짜가 없는 항목은 최신 게시물일 수 있으므로 포함됨

- **녹색당 날짜 추출 개선**
  - 녹색당 사이트는 `ul.li_body` 구조 사용
  - 각 항목의 `li.time` 요소에서 날짜 추출 (YYYY-MM-DD 형식)
  - `list_text_title` 클래스를 가진 링크에서 제목 추출
  - 모든 게시물에서 일관되게 날짜와 제목 추출 성공

- **전체 정당 본문 추출 셀렉터 개선 (2026-01-11)**
  - 모든 정당의 상세 페이지 HTML 구조 분석 완료
  - 정당별 최적 셀렉터 업데이트:
    - **조국혁신당**: `article.newsArticle` (이전 `.ck-content`에서 변경)
    - **녹색당**: `.fr-view` (Froala 에디터)
    - **정의당**: `div.content` (이전 `#contents`보다 정확)
    - **진보당**: `.content_box` (유지)
    - **사회민주당**: `.view_content` (유지)
    - **노동당**: `.kboard-document .kboard-content` (유지)
    - **기본소득당**: `.entry-content` (유지)
  - `blog.naver.com`을 DETAIL_DOMAIN_ALLOWLIST에 추가 (사회민주당 블로그 지원)
  - 테스트 결과: 7개 정당 모두 본문 추출 정상 작동 확인
    - 기본소득당: 17문단/509자 ✓
    - 사회민주당: 1문단/1000자 ✓
    - 조국혁신당: 13문단/12041자 ✓
    - 진보당: 7문단/662자 ✓
    - 노동당: 17문단/4187자 ✓
    - 녹색당: 8문단/1390자 ✓
    - 정의당: 9문단/728자 ✓

## 남은 이슈/할 일

- **Chrome WebDriver 설정 필요**
  - Selenium 사용 시 Chrome 및 ChromeDriver가 시스템에 설치되어 있어야 함
  - ChromeDriver는 Chrome 버전과 호환되는 버전 사용 필요
  - 헤드리스 모드로 실행되므로 GUI 불필요
- 스케줄러(자동 실행)는 아직 미설정
  - macOS `launchd`로 10/18/02시 실행 예정

## 환경 변수 설정 예

```bash
export NOTION_TOKEN="새로 발급한 시크릿"
export NOTION_DATABASE_ID="2e1c9c3e833b803b8accf5fb620224bb"
```
