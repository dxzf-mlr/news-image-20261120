#!/usr/bin/env python3
"""Draw the front page for 20 November 2026.

One 1024x1024 broadsheet, five verified stories of the day, all artwork
drawn here from PIL primitives -- no photos, no downloaded assets, no
network. Run:  python3 draw.py  ->  writes entry.png beside this file.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))

PAPER = (250, 247, 238)
INK = (22, 22, 22)
RED = (178, 34, 34)
BLUE = (31, 73, 125)
STEEL = (94, 130, 163)
SLATE = (70, 90, 110)
TEAL = (23, 128, 109)
GREY = (110, 108, 100)
LIGHT = (232, 228, 216)
GOLD = (214, 158, 46)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF2_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, text, fnt, x, y, max_w, leading, color=INK):
    """Draw wrapped text; returns the y just below the last line."""
    for line in wrap(d, text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def rule(d, x0, x1, y, width=2, color=INK):
    d.line([(x0, y), (x1, y)], fill=color, width=width)


def draw_globe(d, box):
    """A warming globe: blue sphere, meridians, a green leaf on top."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = min(x1 - x0, y1 - y0) // 2 - 6
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(58, 110, 165))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    # meridians and parallels
    for k in (-2, -1, 0, 1, 2):
        d.arc([cx - r, cy - r, cx + r, cy + r], 90 + k * 22, 270 - k * 22,
              fill=(250, 247, 238), width=2)
    for k in (-1, 0, 1):
        yy = cy + k * r // 2
        half = int((r * r - (k * r // 2) ** 2) ** 0.5)
        d.line([(cx - half, yy), (cx + half, yy)], fill=(250, 247, 238), width=2)
    # one green leaf sprouting from the top
    d.line([(cx, cy - r - 2), (cx + 6, cy - r - 30)], fill=(34, 110, 66),
           width=3)
    d.polygon([(cx + 6, cy - r - 32), (cx + 30, cy - r - 22),
               (cx + 10, cy - r - 6)], fill=(46, 139, 87))


def draw_bridge(d, box):
    """Suspension bridge silhouette, kept inside its box."""
    x0, y0, x1, y1 = box
    deck_y = y0 + (y1 - y0) * 2 // 3
    top = y0 + 6
    d.line([(x0, deck_y), (x1, deck_y)], fill=INK, width=4)
    for tx in (x0 + (x1 - x0) // 4, x0 + 3 * (x1 - x0) // 4):
        d.line([(tx, top), (tx, deck_y)], fill=INK, width=5)
        d.line([(tx - 12, top), (tx + 12, top)], fill=INK, width=3)
    # main cable: shallow sag between the towers, sampled as a polyline
    t1 = x0 + (x1 - x0) // 4
    t2 = x0 + 3 * (x1 - x0) // 4
    sag = deck_y - top - 8
    pts = []
    for i in range(21):
        fx = t1 + (t2 - t1) * i / 20
        # parabola: high at the towers, low at mid-span
        fy = top + 4 + sag * (1 - (2 * i / 20 - 1) ** 2)
        pts.append((fx, fy))
    d.line(pts, fill=INK, width=2)
    # side cables sloping down to the deck ends
    d.line([(x0 + 6, deck_y - 2), (t1, top + 4)], fill=INK, width=2)
    d.line([(t2, top + 4), (x1 - 6, deck_y - 2)], fill=INK, width=2)
    # suspenders
    for sx in range(t1 + 12, t2 - 4, 26):
        d.line([(sx, deck_y - 16), (sx, deck_y)], fill=GREY, width=2)
    # water below the deck
    for wy in range(int(deck_y) + 8, y1 - 2, 9):
        d.line([(x0 + 8, wy), (x1 - 8, wy)], fill=STEEL, width=2)


def draw_chart(d, box):
    """Bars climbing to the right, with a rising arrow, inside the box."""
    x0, y0, x1, y1 = box
    base = y1 - 8
    top = y0 + 12
    d.line([(x0 + 8, base), (x1 - 8, base)], fill=INK, width=3)
    d.line([(x0 + 8, top - 4), (x0 + 8, base)], fill=INK, width=3)
    bars = [0.22, 0.38, 0.52, 0.72, 0.95]
    bw = (x1 - x0 - 60) // 5
    span = base - top
    for i, frac in enumerate(bars):
        bx = x0 + 24 + i * (bw + 6)
        bh = int(span * frac)
        d.rectangle([bx, base - bh, bx + bw, base], fill=TEAL)
        d.rectangle([bx, base - bh, bx + bw, base], outline=INK, width=2)
    # arrow over the bars, inside the box
    pts = []
    for i, frac in enumerate(bars):
        cx = x0 + 24 + i * (bw + 6) + bw // 2
        pts.append((cx, base - int(span * frac) - 4))
    d.line(pts, fill=RED, width=4)
    d.polygon([(pts[-1][0], pts[-1][1] - 12), (pts[-1][0] + 14, pts[-1][1] + 2),
               (pts[-1][0] - 2, pts[-1][1] + 10)], fill=RED)


def draw_cyclone(d, box):
    """Spiral storm bands around a calm eye, inside the box."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    rmax = min(x1 - x0, y1 - y0) // 2 - 3
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=GOLD,
              outline=INK, width=2)
    for ring in range(1, 5):
        r = 8 + (rmax - 8) * ring // 4
        d.arc([cx - r, cy - r, cx + r, cy + r], ring * 55, ring * 55 + 250,
              fill=SLATE if ring % 2 else STEEL, width=4)
    # rain streaks hugging the spiral
    for sx, sy in ((cx - 52, cy - 14), (cx - 44, cy + 12),
                   (cx + 44, cy - 12), (cx + 52, cy + 14)):
        d.line([(sx, sy), (sx - 6, sy + 10)], fill=STEEL, width=3)
    # wind swooshes sweeping across the strip
    import math
    for base_y, amp in ((cy - 14, 5), (cy + 14, 5)):
        pts = []
        for i in range(25):
            fx = x0 + 10 + (x1 - x0 - 20) * i / 24
            fy = base_y + amp * math.sin(i / 24 * 4 * math.pi)
            pts.append((fx, fy))
        d.line(pts, fill=STEEL, width=2)


def draw_tower(d, box):
    """A tall tower at dusk, windows lit, with a low skyline."""
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=(38, 44, 66))
    tx0 = x0 + (x1 - x0) // 2 - 26
    tx1 = x0 + (x1 - x0) // 2 + 26
    d.polygon([(tx0, y1), (tx0, y0 + 14), (tx0 + 14, y0 + 4),
               (tx1 - 14, y0 + 4), (tx1, y0 + 14), (tx1, y1)],
              fill=(16, 18, 30))
    for row in range(3):
        for col in range(3):
            wx = tx0 + 8 + col * 14
            wy = y0 + 14 + row * 11
            lit = (row * 3 + col) % 3 != 0
            d.rectangle([wx, wy, wx + 8, wy + 7],
                        fill=GOLD if lit else (52, 58, 82))
    # low skyline on both sides
    for bx, bh in ((x0 + 6, 22), (x0 + 30, 14), (x1 - 44, 18), (x1 - 20, 12)):
        d.rectangle([bx, y1 - bh, bx + 16, y1], fill=(16, 18, 30))


def story_card(d, x, y, w, art_h, kicker, headline, deck, art_fn,
               head_size=27, deck_size=18):
    """One story block: kicker, headline, deck, illustration strip."""
    d.text((x, y), kicker, font=font(SANS_B, 18), fill=RED)
    y += 26
    y = para(d, headline, font(SERIF2_B, head_size), x, y, w,
             head_size + 6)
    y += 6
    y = para(d, deck, font(SANS, deck_size), x, y, w, deck_size + 6,
             color=(58, 58, 54))
    y += 8
    art_fn(d, (x, y, x + w, y + art_h))
    return y + art_h


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # outer frame
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=3)
    d.rectangle([20, 20, W - 21, H - 21], outline=INK, width=1)

    # masthead
    mast = font(SERIF_B, 82)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=mast)
    d.text(((W - tw) / 2, 30), title, font=mast, fill=INK)
    rule(d, 40, W - 40, 128, width=3)
    rule(d, 40, W - 40, 134, width=1)
    dateline = font(SANS_B, 18)
    d.text((40, 146), "FRIDAY, 20 NOVEMBER 2026",
           font=dateline, fill=INK)
    right = "FIVE STORIES  ·  ONE PAGE"
    d.text((W - 40 - d.textlength(right, font=dateline), 146), right,
           font=dateline, fill=INK)
    rule(d, 40, W - 40, 178, width=1)

    # ---- lead story: COP31 ----
    y = 196
    d.text((40, y), "CLIMATE  ·  COP31", font=font(SANS_B, 19), fill=RED)
    y += 32
    y = para(d, "COP31 closes with fossil-fuel phase-out dropped from final text",
             font(SERIF2_B, 42), 40, y, 560, 50)
    y += 10
    y = para(d, "The near-final draft omits the phase-out language after days "
                "of deadlock, leaving the talks to end without a deal on "
                "ending fossil fuels.",
             font(SANS, 21), 40, y, 560, 29, color=(58, 58, 54))
    # lead illustration, right column
    d.rectangle([632, 196, 984, 452], fill=(226, 234, 240),
                outline=INK, width=2)
    draw_globe(d, (672, 216, 944, 408))
    cap = font(SERIF_I, 17)
    cap_t = "A warming world, no phase-out deal."
    d.text((808 - d.textlength(cap_t, font=cap) / 2, 414), cap_t,
           font=cap, fill=(58, 58, 54))
    rule(d, 40, W - 40, 478, width=2)

    # ---- middle row: bridge | markets ----
    y = 492
    mid_left = story_card(d, 40, y, 452, 48,
                          "UKRAINE  ·  KERCH BRIDGE",
                          "Putin vows forceful reply after Kerch Bridge attack",
                          "Moscow rules out a sea or energy ceasefire after "
                          "the latest strike.",
                          draw_bridge)
    mid_right = story_card(d, 532, y, 452, 48,
                           "MARKETS  ·  NASDAQ DEBUT",
                           "Anthropic up 17% on debut, near $2 trillion",
                           "The record listing makes the AI firm one of the "
                           "world's most valuable.",
                           draw_chart)
    mid_end = max(mid_left, mid_right)
    d.line([(512, 500), (512, mid_end)], fill=GREY, width=1)
    rule(d, 40, W - 40, mid_end + 14, width=2)

    # ---- bottom row: cyclone | Riyadh ----
    y = mid_end + 30
    bot_left = story_card(d, 40, y, 452, 48,
                          "INDIA  ·  CYCLONE AKVAN",
                          "Cyclone Akvan hits India; Odisha evacuates 120,000",
                          "The storm hits India's east coast; 120,000 people "
                          "moved to shelters.",
                          draw_cyclone)
    bot_right = story_card(d, 532, y, 452, 48,
                           "SAUDI ARABIA  ·  RIYADH",
                           "Houthi strike hits Riyadh's tallest tower, PIF HQ",
                           "The attack reaches the kingdom's tallest building, "
                           "home of the sovereign fund.",
                           draw_tower)
    bot_end = max(bot_left, bot_right)
    d.line([(512, y), (512, bot_end)], fill=GREY, width=1)

    # footer
    rule(d, 40, W - 40, bot_end + 12, width=1)
    foot = font(SANS, 15)
    d.text((40, bot_end + 22),
           "Sources: Scoop News · The Hindu · The Japan Times · "
           "The Standard · NST · Mathrubhumi",
           font=foot, fill=GREY)
    right = "Drawn for make.fun"
    d.text((W - 40 - d.textlength(right, font=foot), bot_end + 22), right,
           font=foot, fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG")
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
