"""카드뉴스 렌더러: JSON 명세 -> PNG 카드 여러 장

사용법:
  python3 render.py spec.json            # spec.json 옆 out/ 폴더에 저장
  python3 render.py spec.json -o 폴더     # 저장 위치 지정

명세 형식은 SKILL.md 참고.
"""
import argparse
import base64
import html
import json
import mimetypes
import pathlib
import sys

SIZES = {"square": (1080, 1080), "portrait": (1080, 1350), "story": (1080, 1920)}

DEFAULT_THEME = {
    "bg": "#05070f",        # 배경 바깥색
    "bg2": "#16204a",       # 배경 빛 번짐 색
    "text": "#e8ecf8",      # 제목 글자색
    "muted": "#c3cbe4",     # 본문 글자색
    "accent": "#ffb347",    # 강조색 (라벨, 큰 숫자)
    "accent_text": "#1a1204",  # 라벨 안 글자색
    "stars": True,          # 배경 별 점 표시
    "shadow": True,         # 제목 그림자 (밝은 테마는 false)
    "font": "Noto Sans KR",  # Google Fonts 이름
}

CHROMIUM = "/opt/pw-browsers/chromium"


def data_uri(path):
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def rich(text):
    """HTML 이스케이프 후 줄바꿈(\\n)만 <br>로 바꾼다."""
    return html.escape(text or "").replace("\n", "<br>")


CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: var(--W); height: var(--H); }
body { font-family: var(--font), 'Noto Sans KR', sans-serif; color: var(--text); background: var(--bg);
  word-break: keep-all; overflow-wrap: anywhere; }
.card { position: relative; width: var(--W); height: var(--H); overflow: hidden; padding: 80px;
  display: flex; flex-direction: column;
  background: radial-gradient(ellipse at 70% 15%, var(--bg2) 0%, var(--bg) 65%); }
.stars { position: absolute; inset: 0; pointer-events: none;
  background-image:
    radial-gradient(2px 2px at 8% 12%, #fff9, transparent), radial-gradient(1.5px 1.5px at 22% 68%, #fff7, transparent),
    radial-gradient(2px 2px at 37% 30%, #fff8, transparent), radial-gradient(1.5px 1.5px at 51% 88%, #fff6, transparent),
    radial-gradient(2px 2px at 63% 8%, #fff9, transparent), radial-gradient(1.5px 1.5px at 78% 52%, #fff6, transparent),
    radial-gradient(2px 2px at 90% 80%, #fff8, transparent), radial-gradient(1.5px 1.5px at 14% 92%, #fff7, transparent),
    radial-gradient(1.5px 1.5px at 46% 50%, #fff5, transparent), radial-gradient(2px 2px at 95% 28%, #fff7, transparent); }
.pic { position: absolute; background-repeat: no-repeat; background-position: center; }
.pic.circle { border-radius: 50%; box-shadow: 0 0 100px 14px color-mix(in srgb, var(--accent) 40%, transparent); }
.pic.rect { border-radius: 32px; }
.text, .bottom, .foot { position: relative; z-index: 1; }
.kicker { display: inline-block; font-size: 30px; font-weight: 700; padding: 10px 26px; border-radius: 999px;
  color: var(--accent-text); background: var(--accent); }
h1 { font-weight: 900; line-height: 1.25; letter-spacing: -1px; text-shadow: var(--shadow); }
.body { color: var(--muted); font-size: 36px; line-height: 1.6; font-weight: 500; }
.big { font-size: 140px; font-weight: 900; color: var(--accent); letter-spacing: -3px; line-height: 1.05; }
.foot { margin-top: 48px; display: flex; justify-content: space-between; align-items: center;
  font-size: 26px; font-weight: 600; color: var(--muted); opacity: .85; }
.brand { display: flex; align-items: center; gap: 12px; }
.brand i { width: 16px; height: 16px; border-radius: 50%; background: var(--accent); box-shadow: 0 0 12px var(--accent); }

/* 표지 */
.cover .text { margin-top: 120px; max-width: 880px; }
.cover h1 { font-size: 100px; margin: 40px 0 36px; }
.cover .body { font-size: 40px; }
.cover .pic { width: 760px; height: 760px; right: -220px; bottom: -220px; }
.cover .foot { margin-top: auto; }

/* 본문 */
.fact h1 { font-size: 78px; margin-top: 36px; }
.fact.has-pic .text { max-width: 640px; }
.fact .pic { width: 440px; height: 440px; right: -120px; top: 80px; }
.fact .bottom { margin-top: auto; }
.fact .body { margin-top: 28px; }

/* 마무리 */
.outro { align-items: center; text-align: center; }
.outro .pic { position: relative; width: 460px; height: 460px; flex: none; margin-bottom: 40px; }
.outro .text { margin-top: auto; }
.outro h1 { font-size: 68px; margin: 30px 0 26px; }
.outro .body { font-size: 32px; }
.outro .foot { width: 100%; margin-top: auto; }
"""


def card_html(i, total, card, spec, base, size):
    W, H = size
    theme = {**DEFAULT_THEME, **spec.get("theme", {})}
    accent = card.get("accent", theme["accent"])
    kind = card.get("kind", "fact")
    if kind not in ("cover", "fact", "outro"):
        sys.exit(f"{i}번 카드: kind는 cover/fact/outro 중 하나여야 해요 (지금: {kind})")

    pic = ""
    if card.get("image"):
        p = (base / card["image"]).resolve()
        if not p.exists():
            sys.exit(f"{i}번 카드: 이미지 파일이 없어요 -> {p}")
        shape = card.get("shape", "circle")
        zoom = card.get("zoom", 112 if shape == "circle" else 100)
        bgsize = f"{zoom}%" if shape == "circle" else ("cover" if zoom == 100 else f"auto {zoom}%")
        extra = card.get("filter", "")
        pic = (f'<div class="pic {shape}" style="background-image:url({data_uri(p)});'
               f'background-size:{bgsize};{f"filter:{extra};" if extra else ""}"></div>')

    kicker = f'<span class="kicker">{rich(card["kicker"])}</span>' if card.get("kicker") else ""
    title = f'<h1>{rich(card.get("title"))}</h1>'
    body = f'<p class="body">{rich(card["body"])}</p>' if card.get("body") else ""
    big = f'<div class="big">{rich(card["big"])}</div>' if card.get("big") else ""

    if kind == "fact":
        content = f'<div class="text">{kicker}{title}</div><div class="bottom">{big}{body}</div>'
    else:
        content = f'<div class="text">{kicker}{title}{big}{body}</div>'
    if kind == "outro":
        content = pic + content
        pic = ""

    brand = spec.get("brand", "")
    foot = (f'<div class="foot"><span class="brand">{"<i></i>" + rich(brand) if brand else ""}</span>'
            f'<span>{i} / {total}</span></div>')
    font_link = theme["font"].replace(" ", "+")
    style = (f"--W:{W}px;--H:{H}px;--bg:{theme['bg']};--bg2:{theme['bg2']};--text:{theme['text']};"
             f"--muted:{theme['muted']};--accent:{accent};--accent-text:{theme['accent_text']};"
             f"--font:'{theme['font']}';--shadow:{'0 4px 24px #000a' if theme['shadow'] else 'none'}")
    cls = f"card {kind}{' has-pic' if card.get('image') else ''}"
    return f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={font_link}:wght@400;500;600;700;900&display=swap">
<style>{CSS}</style></head><body style="{style}"><div class="{cls}">
{'<div class="stars"></div>' if theme['stars'] else ''}{pic}{content}{foot}
</div></body></html>"""


def main():
    ap = argparse.ArgumentParser(description="JSON 명세로 카드뉴스 PNG 생성")
    ap.add_argument("spec")
    ap.add_argument("-o", "--out")
    ap.add_argument("--preview", action="store_true", help="모든 카드를 이어붙인 preview.png도 저장")
    args = ap.parse_args()

    spec_path = pathlib.Path(args.spec).resolve()
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    base = spec_path.parent
    out = pathlib.Path(args.out).resolve() if args.out else base / "out"
    out.mkdir(parents=True, exist_ok=True)
    size = SIZES.get(spec.get("size", "square"))
    if not size:
        sys.exit(f"size는 {', '.join(SIZES)} 중 하나여야 해요")
    cards = spec["cards"]

    from playwright.sync_api import sync_playwright
    paths = []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROMIUM) if pathlib.Path(CHROMIUM).exists() \
            else p.chromium.launch()
        page = browser.new_page(viewport={"width": size[0], "height": size[1]})
        for i, card in enumerate(cards, 1):
            page.set_content(card_html(i, len(cards), card, spec, base, size), wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            path = out / f"card_{i}.png"
            page.screenshot(path=str(path))
            paths.append(path)
            print(f"저장 완료: {path}")
        browser.close()

    if args.preview:
        from PIL import Image
        w, h = size[0] // 2, size[1] // 2
        sheet = Image.new("RGB", (w * len(paths), h))
        for k, pth in enumerate(paths):
            sheet.paste(Image.open(pth).convert("RGB").resize((w, h)), (w * k, 0))
        sheet.save(out / "preview.png")
        print(f"미리보기: {out / 'preview.png'}")


if __name__ == "__main__":
    main()
