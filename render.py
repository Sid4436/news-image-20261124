#!/usr/bin/env python3
"""Render entry.png for make.fun news-image-20261124: the world's news of Tuesday 24 November 2026.

Drawn with Pillow primitives only (no downloaded art). Rendered at 2x and downsampled for clean edges.
Run: python3 render.py  -> writes entry.png beside this file (deterministic, no timestamps).
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

S = 2                      # supersampling factor
W = H = 1024
FONT_DIR = "/usr/share/fonts/truetype/noto/"

PAPER = (247, 242, 230)
INK = (24, 26, 33)
MUTED = (92, 96, 108)
RULE = (190, 182, 166)
RED = (186, 38, 42)
GREEN = (28, 140, 84)
BLUE = (36, 84, 160)
GOLD = (214, 160, 40)


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size * S)


F_MAST = font("NotoSerifDisplay-Black.ttf", 50)
F_DATE = font("NotoSans-Bold.ttf", 21)
F_TAG = font("NotoSans-Black.ttf", 15)
F_HEAD = font("NotoSerif-Bold.ttf", 27)
F_SUB = font("NotoSans-Regular.ttf", 17)
F_FOOT = font("NotoSans-SemiBold.ttf", 14)


def P(*v):
    """Scale logical coordinates to the supersampled canvas."""
    return tuple(int(round(x * S)) for x in v)


def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width * S:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- illustrations
# Each draws inside the logical box (x, y, w, h).

def art_markets(d, x, y, w, h):
    """Asian markets rebound: rising candlesticks and an up arrow."""
    d.rectangle(P(x, y, x + w, y + h), fill=(232, 240, 233))
    base = y + h - 18
    d.line(P(x + 14, base, x + w - 14, base), fill=RULE, width=2 * S)
    vals = [62, 54, 46, 58, 40, 30, 22, 12]
    bw = (w - 60) / len(vals)
    for i, top in enumerate(vals):
        cx = x + 24 + i * bw + bw / 2
        col = RED if i < 3 else GREEN
        t = y + 20 + top
        b = t + 26 + (i % 3) * 6
        d.line(P(cx, t - 8, cx, b + 8), fill=col, width=2 * S)
        d.rectangle(P(cx - bw * 0.3, t, cx + bw * 0.3, b), fill=col)
    d.line(P(x + 26, y + h - 40, x + w - 40, y + 26), fill=INK, width=5 * S)
    ax, ay = x + w - 40, y + 26
    d.polygon(P(ax + 8, ay - 8, ax - 18, ay - 2, ax + 2, ay + 18), fill=INK)
    for i, lab in enumerate(["KOSPI", "NIKKEI", "TAIEX"]):
        d.text(P(x + 16, y + 12 + i * 20), lab, font=F_TAG, fill=GREEN)


def art_chips(d, x, y, w, h):
    """Singapore probe: an AI chip under a magnifying glass."""
    d.rectangle(P(x, y, x + w, y + h), fill=(232, 236, 245))
    cx, cy, r = x + w * 0.42, y + h * 0.52, 34
    d.rectangle(P(cx - r, cy - r, cx + r, cy + r), fill=INK)
    d.rectangle(P(cx - r + 10, cy - r + 10, cx + r - 10, cy + r - 10), outline=GOLD, width=2 * S)
    d.text(P(cx - 13, cy - 11), "AI", font=F_TAG, fill=GOLD)
    for k in range(5):
        o = -r + 8 + k * (2 * r - 16) / 4
        d.line(P(cx + o, cy - r - 10, cx + o, cy - r), fill=INK, width=2 * S)
        d.line(P(cx + o, cy + r, cx + o, cy + r + 10), fill=INK, width=2 * S)
        d.line(P(cx - r - 10, cy + o, cx - r, cy + o), fill=INK, width=2 * S)
        d.line(P(cx + r, cy + o, cx + r + 10, cy + o), fill=INK, width=2 * S)
    mx, my, mr = cx + 78, cy - 10, 30
    d.ellipse(P(mx - mr, my - mr, mx + mr, my + mr), outline=BLUE, width=6 * S)
    d.line(P(mx + mr * 0.7, my + mr * 0.7, mx + mr + 26, my + mr + 26), fill=BLUE, width=9 * S)
    d.text(P(x + 12, y + 10), "SG", font=F_TAG, fill=RED)


def art_safety(d, x, y, w, h):
    """Australia online-safety bill: a phone behind a shield with a 5% fine tag."""
    d.rectangle(P(x, y, x + w, y + h), fill=(245, 236, 228))
    px, py = x + w * 0.30, y + 18
    d.rounded_rectangle(P(px, py, px + 54, py + h - 36), radius=8 * S, fill=INK)
    d.rectangle(P(px + 6, py + 10, px + 48, py + h - 52), fill=(120, 170, 220))
    sx, sy = px + 70, y + 26
    d.polygon(P(sx, sy, sx + 64, sy, sx + 64, sy + 42, sx + 32, sy + 78, sx, sy + 42), fill=RED)
    d.text(P(sx + 13, sy + 18), "5%", font=F_HEAD, fill=PAPER)
    d.text(P(x + 12, y + 10), "AU", font=F_TAG, fill=BLUE)


def art_quake(d, x, y, w, h):
    """Nepal M5.3 quake: Himalayan peaks over a seismograph trace."""
    d.rectangle(P(x, y, x + w, y + h), fill=(236, 233, 242))
    gy = y + h * 0.62
    d.polygon(P(x, gy, x + w * 0.25, y + 26, x + w * 0.42, gy - 30, x + w * 0.6, y + 14,
                x + w * 0.8, gy - 20, x + w, gy), fill=(120, 124, 150))
    d.polygon(P(x + w * 0.55, y + 30, x + w * 0.6, y + 14, x + w * 0.65, y + 30), fill=PAPER)
    d.polygon(P(x + w * 0.21, y + 38, x + w * 0.25, y + 26, x + w * 0.29, y + 38), fill=PAPER)
    pts, n = [], 40
    for i in range(n + 1):
        amp = [0, 3, -4, 5, -6, 20, -26, 30, -22, 14, -8, 4, -3, 2, 0][min(i // 3, 14)] if 9 <= i <= 33 else 0
        pts += [x + 10 + i * (w - 20) / n, gy + 22 + amp * 0.8]
    d.line(P(*pts), fill=RED, width=3 * S)
    d.text(P(x + 12, y + h - 26), "M5.3", font=F_TAG, fill=RED)


# ---------------------------------------------------------------- the day's stories
# Each was first reported on Tuesday 24 November 2026 and checked in at least two outlets.
STORIES = [
    ("ASIA · MARKETS", "Asian stocks surge as AI trade revives",
     "Kospi, Nikkei and Taiex leap; Seoul triggers a buy-side trading sidecar", art_markets),
    ("SINGAPORE · TECH", "Singapore keeps probing Megaspeed",
     "PM Wong, in Canberra: city-state won't be a conduit to dodge US chip curbs", art_chips),
    ("AUSTRALIA · TECH", "Tech giants face fines of up to 5% of global revenue",
     "Minister Anika Wells toughens Australia's online safety bill", art_safety),
    ("NEPAL · QUAKE", "M5.3 earthquake shakes eastern Nepal",
     "Koshi province near Sikkim; felt in India and Bhutan, no early casualty reports", art_quake),
]


def render(path):
    img = Image.new("RGB", P(W, H), PAPER)
    d = ImageDraw.Draw(img)
    # masthead
    d.rectangle(P(0, 0, W, 10), fill=RED)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=F_MAST) / S
    d.text(P((W - tw) / 2, 22), title, font=F_MAST, fill=INK)
    date = "TUESDAY, 24 NOVEMBER 2026  ·  ONE DAY OF WORLD NEWS"
    dw = d.textlength(date, font=F_DATE) / S
    d.text(P((W - dw) / 2, 94), date, font=F_DATE, fill=RED)
    d.line(P(36, 132, W - 36, 132), fill=INK, width=3 * S)
    d.line(P(36, 137, W - 36, 137), fill=INK, width=1 * S)
    # 2 x 2 grid of stories
    gx, gy, gap = 36, 156, 24
    cw = (W - 2 * gx - gap) / 2
    ch = 388
    for i, (tag, head, sub, art) in enumerate(STORIES):
        cx = gx + (i % 2) * (cw + gap)
        cy = gy + (i // 2) * (ch + gap)
        art(d, cx, cy, cw, 170)
        d.text(P(cx, cy + 184), tag, font=F_TAG, fill=RED)
        ty = cy + 206
        for line in wrap(d, head, F_HEAD, cw):
            d.text(P(cx, ty), line, font=F_HEAD, fill=INK)
            ty += 36
        ty += 4
        for line in wrap(d, sub, F_SUB, cw):
            d.text(P(cx, ty), line, font=F_SUB, fill=MUTED)
            ty += 24
    d.line(P(W / 2, gy, W / 2, gy + 2 * ch + gap), fill=RULE, width=1 * S)
    d.line(P(gx, gy + ch + gap / 2, W - gx, gy + ch + gap / 2), fill=RULE, width=1 * S)
    # footer
    d.line(P(36, H - 46, W - 36, H - 46), fill=INK, width=2 * S)
    foot = "Events first reported on Tuesday 24 November 2026 · each checked in two or more news reports"
    fw = d.textlength(foot, font=F_FOOT) / S
    d.text(P((W - fw) / 2, H - 36), foot, font=F_FOOT, fill=MUTED)
    out = img.resize((W, H), Image.LANCZOS)
    out.save(path, format="PNG", optimize=True)


if __name__ == "__main__":
    render(Path(__file__).with_name("entry.png"))
