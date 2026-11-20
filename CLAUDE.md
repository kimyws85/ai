# CLAUDE.md

## 소통 규칙

- 모든 답변, 진행 상황, 명령어 설명(Bash description 포함)은 **한글**로 쓴다.
- 짧고 바로 쓸 수 있게 답한다.

## 프로젝트 구조

- **태양계 여행 사이트** (정적 HTML/CSS/JS, 빌드 도구 없음)
  - `index.html` 홈, `planets.html` 행성 소개, `compare.html` 크기·거리 비교
  - `css/style.css`: 색상 변수(`--bg`, `--accent` 등)와 전체 스타일
  - `js/data.js`: 행성 데이터 (`PLANETS` 배열, 공개 천문 자료 기준 근삿값). 행성 수치는 여기를 기준으로 한다
  - `images/`: 태양·행성 사진
- **카드뉴스**: `cardnews/<주제>/spec.json` + `out/card_N.png`
  - `cardnews/make_cards.py`: 첫 태양계 카드뉴스용 스크립트 (예전 방식)
  - 새 카드뉴스는 `카드` 스킬을 쓴다 (`/카드 <주제>`)

## 카드뉴스 (`.claude/skills/카드/`)

- 렌더링: `python3 .claude/skills/카드/scripts/render.py cardnews/<주제>/spec.json --preview`
- Python Playwright가 필요하다 (`pip install playwright`). 브라우저는 `/opt/pw-browsers/chromium`에 이미 있으니 `playwright install`은 하지 않는다.
- 숫자·사실은 반드시 출처와 대조하고, 계산이 들어간 문장은 직접 계산해서 확인한다.
- 만든 뒤 `preview.png`를 직접 열어 글자 겹침, 사진 테두리, 넘침을 확인한다.

## Git

- 작업 브랜치에 커밋하고 푸시한다. `main`에 직접 푸시하지 않는다.
- PR은 요청할 때만 만든다.
- 커밋 메시지는 한글로 쓴다.
