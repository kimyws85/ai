---
name: 카드
description: 인스타그램용 한글 카드뉴스(PNG 이미지 여러 장)를 만든다. 사용자가 "카드뉴스", "카드 만들어", "인스타 캐러셀", "/카드"를 말하거나 어떤 주제를 여러 장짜리 이미지 슬라이드로 정리해 달라고 할 때 사용한다.
---

# 카드뉴스 만들기

주제를 받아 1080px 카드뉴스 PNG를 만든다. 진행 상황과 명령 설명은 모두 한글로 쓴다.

## 1. 정할 것 (모르면 AskUserQuestion으로 한 번에 묻기)

- **주제/내용**: 사용자가 준 자료, 레포 안 파일, 또는 직접 조사한 내용
- **크기**: `square` 1080x1080 (기본) / `portrait` 1080x1350 / `story` 1080x1920
- **장수**: 기본 5장 (표지 1 + 본문 3 + 마무리 1), 인스타 최대 10장
- **분위기/색**: 기본은 어두운 우주 테마. 주제에 맞게 `theme` 색을 바꾼다
- **브랜드 이름**: 카드 왼쪽 아래에 표시할 이름 (없으면 생략)

사용자가 이미 말한 건 다시 묻지 않는다.

## 2. 내용 쓰기 원칙

- 카드 한 장에 메시지 하나. 제목은 2줄 이내, 본문은 2~3줄 이내.
- 본문 카드에는 눈에 띄는 숫자나 키워드를 `big`에 넣는다 (예: `464°C`, `21.9km`).
- **사실 확인 필수**: 숫자와 사실은 출처(레포 데이터, 사용자 자료, 검색)와 대조한다. 계산이 들어가는 문장(예: "발견 후 아직 한 바퀴도 못 돌았다")은 직접 계산해서 맞는지 확인한다.
- 줄바꿈은 `\n`으로 넣는다. HTML 태그는 쓰지 않는다 (자동 이스케이프됨).

## 3. 명세 파일 작성

작업 폴더(예: `cardnews/<주제>/`)에 `spec.json`을 만든다. 이미지 경로는 spec.json 기준 상대경로.

```json
{
  "size": "square",
  "brand": "태양계 여행",
  "theme": { "bg": "#05070f", "bg2": "#16204a", "accent": "#ffb347", "stars": true },
  "cards": [
    { "kind": "cover", "kicker": "태양계 여행", "title": "알고 보면 반전인\n태양계 상식 3가지",
      "body": "교과서엔 없던 행성들의 진짜 모습", "image": "../../images/sun.jpg", "zoom": 122 },
    { "kind": "fact", "kicker": "반전 01 · 금성", "title": "가장 뜨거운 행성은\n수성이 아니다",
      "big": "464°C", "body": "두꺼운 이산화탄소 대기의 온실효과 때문이에요.",
      "image": "../../images/venus.jpg", "accent": "#d9b27a" },
    { "kind": "outro", "kicker": "보너스", "title": "더 많은 이야기는\n다음 편에서", "body": "저장하고 친구에게 공유해 주세요" }
  ]
}
```

카드 필드:

| 필드 | 설명 |
|---|---|
| `kind` | `cover`(표지) / `fact`(본문) / `outro`(마무리) |
| `kicker` | 위쪽 라벨 (짧게) |
| `title` | 제목 (필수) |
| `big` | 크게 강조할 숫자·키워드 (선택) |
| `body` | 설명 문장 (선택) |
| `image` | 사진 경로 (선택). 없으면 글자만으로 배치됨 |
| `shape` | `circle`(기본, 행성·인물·제품 컷) / `rect`(일반 사진) |
| `zoom` | 사진 확대 % (circle 기본 112). 사진 가장자리 검은 여백이 보이면 올린다 |
| `filter` | CSS filter (예: 회색 사진을 따뜻하게 `sepia(1) saturate(4) hue-rotate(-12deg)`) |
| `accent` | 이 카드만 강조색 변경 |

`theme` 키: `bg`, `bg2`, `text`, `muted`, `accent`, `accent_text`, `stars`(true/false), `shadow`(제목 그림자, true/false), `font`(Google Fonts 이름, 기본 `Noto Sans KR`).
밝은 테마 예: `{"bg":"#fff8ef","bg2":"#ffe2c2","text":"#1f1a14","muted":"#5b5147","accent":"#ff7a45","accent_text":"#ffffff","stars":false,"shadow":false}`

## 4. 렌더링

필요하면 먼저 `pip install playwright` (브라우저는 미리 설치돼 있으니 `playwright install`은 하지 않는다).

```bash
python3 .claude/skills/카드/scripts/render.py cardnews/<주제>/spec.json --preview
```

결과: `cardnews/<주제>/out/card_1.png ...` 와 이어붙인 `preview.png`.

## 5. 검수 (반드시)

`preview.png`를 Read로 열어 직접 본다. 아래 문제가 있으면 spec을 고쳐 다시 렌더링한다.

- 글자가 사진·페이지 번호·브랜드와 겹침 → 제목/본문을 줄이거나 `\n` 위치 조정
- 사진 가장자리에 검은 테두리 → `zoom` 올리기
- 글자가 카드 밖으로 넘침 → 문장 줄이기
- 숫자·사실 오류 → 고치기

## 6. 전달

완성된 PNG들을 SendUserFile로 보내고, 카드별 내용을 표로 짧게 정리한다. 수정한 사실 오류가 있으면 알려준다.
