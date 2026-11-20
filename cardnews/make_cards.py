"""태양계 카드뉴스 생성기 (1080x1080 PNG 5장)

실행: python3 cardnews/make_cards.py
결과: cardnews/out/card_1.png ~ card_5.png
"""
import base64
import pathlib

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent
IMG = ROOT.parent / "images"
OUT = ROOT / "out"
TOTAL = 5


def img(name):
    path = IMG / name
    mime = "image/png" if path.suffix == ".png" else "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


# 카드 내용: 수치는 레포의 js/data.js, compare.html 기준
CARDS = [
    dict(kind="cover", image="sun.jpg", glow="#ffb347",
         kicker="태양계 여행",
         title="알고 보면 반전인<br>태양계 상식 3가지",
         body="교과서엔 없던 행성들의 진짜 모습"),
    dict(kind="fact", image="venus.jpg", glow="#d9b27a",
         kicker="반전 01 · 금성",
         title="가장 뜨거운 행성은<br>수성이 아니다",
         big="464°C",
         body="태양에서 두 번째인 금성이 1등이에요. 두꺼운 이산화탄소 대기가 열을 가두는 온실효과 때문이에요."),
    dict(kind="fact", image="jupiter.png", glow="#d6a77a",
         kicker="반전 02 · 목성",
         title="지구가 1,300개<br>들어가는 거인",
         big="하루 10시간",
         body="태양계에서 가장 크지만 자전은 가장 빨라요. 약 10시간 만에 한 바퀴를 돌아요."),
    dict(kind="fact", image="mars.png", glow="#c8643c",
         kicker="반전 03 · 화성",
         title="에베레스트의 2배,<br>올림포스 산",
         big="21.9km",
         body="태양계에서 가장 큰 화산이 화성에 있어요. 높이가 에베레스트 산(8.8km)의 두 배가 넘어요."),
    dict(kind="outro", image="neptune.png", glow="#6ea8ff",
         kicker="보너스 · 해왕성",
         title="해왕성의 1년은<br>지구 시간으로 165년",
         body="1846년에 발견된 뒤 2011년에야 처음으로 한 바퀴를 돌았어요.<br>더 많은 행성 이야기는 「태양계 여행」에서 만나요."),
]

# 사진 속 검은 여백을 잘라내기 위한 확대 비율(%)
ZOOM = {"sun.jpg": 122, "jupiter.png": 128, "mars.png": 126, "neptune.png": 118}

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1080px; }
body { font-family: 'Noto Sans KR', sans-serif; color: #e8ecf8; background: #05070f; word-break: keep-all; }
.card { position: relative; width: 1080px; height: 1080px; overflow: hidden;
  background: radial-gradient(ellipse at 70% 20%, #16204a 0%, #05070f 65%); }
.stars { position: absolute; inset: 0;
  background-image:
    radial-gradient(2px 2px at 8% 12%, #fff9, transparent),
    radial-gradient(1.5px 1.5px at 22% 68%, #fff7, transparent),
    radial-gradient(2px 2px at 37% 30%, #fff8, transparent),
    radial-gradient(1.5px 1.5px at 51% 88%, #fff6, transparent),
    radial-gradient(2px 2px at 63% 8%, #fff9, transparent),
    radial-gradient(1.5px 1.5px at 78% 52%, #fff6, transparent),
    radial-gradient(2px 2px at 90% 80%, #fff8, transparent),
    radial-gradient(1.5px 1.5px at 14% 92%, #fff7, transparent),
    radial-gradient(1.5px 1.5px at 46% 50%, #fff5, transparent),
    radial-gradient(2px 2px at 95% 28%, #fff7, transparent); }
.planet { position: absolute; border-radius: 50%; background-size: 112%; background-repeat: no-repeat; background-position: center; }
.kicker { display: inline-block; font-size: 30px; font-weight: 700; letter-spacing: 1px;
  padding: 10px 26px; border-radius: 999px; color: #1a1204; background: var(--glow); }
h1 { font-weight: 900; line-height: 1.25; letter-spacing: -1px; }
.body { color: #c3cbe4; font-size: 36px; line-height: 1.6; font-weight: 500; }
.page { position: absolute; right: 80px; bottom: 64px; font-size: 26px; font-weight: 700; color: #9aa6c7; }
.brand { position: absolute; left: 80px; bottom: 64px; font-size: 26px; color: #9aa6c7; font-weight: 500;
  display: flex; align-items: center; gap: 12px; }
.brand i { width: 16px; height: 16px; border-radius: 50%; background: #ffb347; box-shadow: 0 0 12px #ffb347; }

/* 표지 */
.cover .planet { width: 760px; height: 760px; right: -220px; bottom: -220px;
  box-shadow: 0 0 140px 30px rgba(255,170,60,.45);
  filter: sepia(1) saturate(4) hue-rotate(-12deg) brightness(1.05); }
.cover .text { position: absolute; left: 80px; top: 200px; width: 860px; }
.cover h1 { font-size: 104px; margin: 40px 0 36px; text-shadow: 0 4px 30px #000c; }
.cover .body { font-size: 40px; }

/* 본문 */
.fact .planet { width: 440px; height: 440px; right: -130px; top: 80px;
  box-shadow: 0 0 90px 10px color-mix(in srgb, var(--glow) 45%, transparent); }
.fact .text { position: absolute; left: 80px; top: 150px; width: 920px; }
.fact h1 { font-size: 78px; margin: 36px 0 0; text-shadow: 0 4px 24px #000c; }
.fact .big { position: absolute; left: 80px; top: 560px; font-size: 140px; font-weight: 900;
  color: var(--glow); letter-spacing: -3px; line-height: 1; }
.fact .body { position: absolute; left: 80px; top: 730px; width: 900px; }

/* 마무리 */
.outro .planet { width: 460px; height: 460px; left: 50%; top: 80px; transform: translateX(-50%);
  box-shadow: 0 0 120px 20px rgba(110,168,255,.4); }
.outro .text { position: absolute; left: 0; right: 0; top: 570px; text-align: center; padding: 0 80px; }
.outro h1 { font-size: 68px; margin: 30px 0 26px; }
.outro .body { font-size: 32px; }
.outro .brand { left: 50%; transform: translateX(-50%); bottom: 56px; }
"""


def card_html(i, c):
    kind = c["kind"]
    big = f'<div class="big">{c["big"]}</div>' if c.get("big") else ""
    body_inside = kind != "fact"
    body = f'<p class="body">{c["body"]}</p>'
    return f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{CSS}</style></head>
<body><div class="card {kind}" style="--glow:{c['glow']}">
  <div class="stars"></div>
  <div class="planet" style="background-image:url({img(c['image'])});background-size:{ZOOM.get(c['image'], 112)}%"></div>
  <div class="page">{i} / {TOTAL}</div>
  <div class="text"><span class="kicker">{c['kicker']}</span><h1>{c['title']}</h1>{body if body_inside else ''}</div>
  {big}{'' if body_inside else body}
  <div class="brand"><i></i>태양계 여행</div>
</div></body></html>"""


def main():
    OUT.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        page = browser.new_page(viewport={"width": 1080, "height": 1080})
        for i, c in enumerate(CARDS, 1):
            page.set_content(card_html(i, c), wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            path = OUT / f"card_{i}.png"
            page.screenshot(path=str(path))
            print(f"저장 완료: {path}")
        browser.close()


if __name__ == "__main__":
    main()
