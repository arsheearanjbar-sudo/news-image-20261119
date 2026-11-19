#!/usr/bin/env python3
"""Draw the news-image-20261119 entry: a newspaper front page summing up
Thursday 19 November 2026 in six verified stories.

Stories (each verified from a major outlet's 19 November 2026 coverage):
  1. LEAD: Xi, Trump and Putin hold their first-ever trilateral summit in
     Shenzhen, on the sidelines of APEC (Yonhap, published 19 Nov 09:03
     KST; Nikkei live, updated 19 Nov 09:06 JST). Agenda: nuclear arms,
     Ukraine, Iran.
  2. The International Court of Justice delivers its ruling in the
     Gambia v Myanmar Rohingya genocide case (Al Jazeera, 18 Nov preview;
     court announced the ruling for 19 Nov, reading from 08:00 GMT;
     first ICJ genocide judgment in over a decade).
  3. Grand Theft Auto VI goes live worldwide, rolling out at midnight
     local time from New Zealand (CNA, updated 19 Nov 08:14 SGT;
     Metacritic 99; 13 years after GTA V).
  4. Iran says three oil tankers caught fire after hitting naval mines
     east of the Strait of Hormuz (NDTV, published 19 Nov 05:20 IST;
     IRGC statement Wed evening; the claim is unverified).
  5. Cyclone Akvan turns into a very severe cyclonic storm on 19 Nov
     (IMD via Business Today / Free Press Journal; landfall zone revised
     to Narsapur-Puri, crossing Friday; heavy rain in Bengal from today).
  6. India begin their Test series against New Zealand in Wellington
     (ABP Live / News18, 18 Nov previews; first Test starts Thu 19 Nov
     at the Basin Reserve, 11:00 NZDT).

Everything is drawn by code with PIL: flat shapes, no photos, no copied art.
Deterministic: same input always renders the same PNG bytes.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

W, H = 1024, 1024
PAPER = (246, 241, 230)      # warm off-white newsprint
INK = (17, 17, 17)           # near-black
RED = (155, 28, 28)          # dark red accent (kickers, date)
GREY = (85, 85, 85)          # subline grey
SUB = (51, 51, 51)           # dark grey subline text
M = 28                        # side margin
CW = W - 2 * M                # content width = 968


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(path, text, start, max_w, floor=20):
    """Largest font size <= start whose rendering of text fits max_w."""
    for size in range(start, floor - 1, -1):
        f = font(path, size)
        if f.getlength(text) <= max_w:
            return f
    return font(path, floor)


def star_points(cx, cy, r_out, r_in, n=5, rot_deg=-90):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot_deg + i * 180.0 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


# ---------------------------------------------------------------- pictures
def draw_summit(d, x0, y0, w, h):
    """Summit stage: three flags (China, USA, Russia) over a dark band.
    Panel (x0,y0,w,h)."""
    x1, y1 = x0 + w, y0 + h
    d.rectangle([x0, y0, x1, y1], fill=(207, 227, 239))  # pale sky
    # three flags in a row, centred vertically in the upper part
    fw, fh = 104, 76
    fy0 = y0 + (h - 44 - fh) // 2
    fy1 = fy0 + fh
    gap = (w - 3 * fw) // 4
    fx = [x0 + gap + i * (fw + gap) for i in range(3)]
    # China: red field, one yellow star
    d.rectangle([fx[0], fy0, fx[0] + fw, fy1], fill=(222, 41, 16))
    d.polygon(star_points(fx[0] + 26, fy0 + fh // 2, 20, 8.5),
              fill=(255, 222, 0))
    # USA: stripes + blue canton
    for i in range(4):
        col = (179, 25, 34) if i % 2 == 0 else (255, 255, 255)
        d.rectangle([fx[1], fy0 + i * (fh // 4),
                     fx[1] + fw, fy0 + (i + 1) * (fh // 4)], fill=col)
    d.rectangle([fx[1], fy0, fx[1] + 42, fy0 + fh // 2], fill=(60, 59, 110))
    # Russia: white / blue / red bands
    for i, col in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        d.rectangle([fx[2], fy0 + i * (fh // 3),
                     fx[2] + fw, fy0 + (i + 1) * (fh // 3)], fill=col)
    # dark foreground band
    d.rectangle([x0, y1 - 44, x1, y1], fill=(31, 42, 68))
    # three small gold dots on the band: summit table microphones
    for i in range(3):
        cx = fx[i] + fw // 2
        d.ellipse([cx - 5, y1 - 30, cx + 5, y1 - 20], fill=(242, 193, 78))


def draw_court_narrow(d, x0, y0, w, h):
    """A courthouse, scaled to a narrow panel: pediment, columns, steps."""
    x1, y1 = x0 + w, y0 + h
    d.rectangle([x0, y0, x1, y1], fill=(232, 228, 216))
    cx = x0 + w // 2
    pw = w * 0.34  # half pediment width
    # pediment (triangle roof)
    d.polygon([(cx - pw, y0 + h * 0.36), (cx + pw, y0 + h * 0.36),
               (cx, y0 + h * 0.08)], fill=(107, 112, 120))
    # entablature
    d.rectangle([cx - pw - 4, y0 + h * 0.36, cx + pw + 4, y0 + h * 0.44],
                fill=(85, 90, 97))
    # four columns
    col_w = w * 0.045
    for off in (-0.27, -0.09, 0.09, 0.27):
        cxx = cx + off * w
        d.rectangle([cxx, y0 + h * 0.44, cxx + col_w, y0 + h * 0.86],
                    fill=(125, 131, 140))
    # door between the middle columns
    d.rectangle([cx - col_w * 0.6, y0 + h * 0.58,
                 cx + col_w * 0.6, y0 + h * 0.86], fill=(58, 63, 70))
    # steps
    d.rectangle([cx - pw - 6, y0 + h * 0.86, cx + pw + 6, y0 + h * 0.93],
                fill=(85, 90, 97))
    d.rectangle([cx - pw - 12, y0 + h * 0.93, cx + pw + 12, y1],
                fill=(85, 90, 97))


def draw_gamepad(d, x0, y0, w, h):
    """A game controller on a dark panel."""
    x1, y1 = x0 + w, y0 + h
    d.rectangle([x0, y0, x1, y1], fill=(31, 42, 68))
    cx, cy = x0 + w // 2, y0 + h // 2 + 4
    # controller body
    d.rounded_rectangle([cx - 118, cy - 30, cx + 118, cy + 30], radius=22,
                        fill=(46, 61, 92))
    # grips
    d.ellipse([cx - 118, cy + 8, cx - 78, cy + 38], fill=(46, 61, 92))
    d.ellipse([cx + 78, cy + 8, cx + 118, cy + 38], fill=(46, 61, 92))
    # D-pad (plus sign), left
    px, py = cx - 78, cy - 2
    d.rectangle([px - 5, py - 16, px + 5, py + 16], fill=(207, 212, 218))
    d.rectangle([px - 16, py - 5, px + 16, py + 5], fill=(207, 212, 218))
    # four action buttons, right
    btns = [(cx + 62, cy - 16, (46, 204, 113)),   # green
            (cx + 82, cy - 2, (231, 76, 60)),     # red
            (cx + 62, cy + 12, (241, 196, 15)),   # yellow
            (cx + 42, cy - 2, (52, 152, 219))]    # blue
    for (bx, by, col) in btns:
        d.ellipse([bx - 8, by - 8, bx + 8, by + 8], fill=col)
    # two joysticks
    for jx in (cx - 22, cx + 22):
        d.ellipse([jx - 11, cy + 10, jx + 11, cy + 32], fill=(24, 32, 52))
        d.ellipse([jx - 7, cy + 14, jx + 7, cy + 28], fill=(125, 131, 140))
    # small start dots in the middle
    d.ellipse([cx - 8, cy - 14, cx - 2, cy - 8], fill=(207, 212, 218))
    d.ellipse([cx + 2, cy - 14, cx + 8, cy - 8], fill=(207, 212, 218))


def draw_tanker(d, x0, y0, w, h):
    """An oil tanker on fire in the strait: sea, hull, flames, smoke."""
    x1, y1 = x0 + w, y0 + h
    d.rectangle([x0, y0, x1, y0 + h * 0.38], fill=(223, 234, 242))  # sky
    d.rectangle([x0, y0 + h * 0.38, x1, y1], fill=(47, 111, 178))  # sea
    # tanker hull (dark), bow to the right
    hx0, hx1 = x0 + 18, x1 - 18
    hy0, hy1 = y0 + h * 0.55, y0 + h * 0.82
    d.polygon([(hx0, hy0), (hx1 - 26, hy0), (hx1, hy0 + (hy1 - hy0) * 0.55),
               (hx1 - 26, hy1), (hx0, hy1)], fill=(31, 42, 68))
    # deck line + superstructure
    d.rectangle([hx0 + 8, hy0 - 18, hx0 + 52, hy0], fill=(207, 212, 218))
    d.rectangle([hx0 + 20, hy0 - 30, hx0 + 40, hy0 - 18], fill=(179, 25, 34))
    # flames above mid-ship (orange outer, yellow inner)
    fx = x0 + w * 0.58
    d.polygon([(fx - 26, hy0), (fx - 12, hy0 - 30), (fx - 2, hy0 - 12),
               (fx + 10, hy0 - 34), (fx + 22, hy0 - 10), (fx + 28, hy0)],
              fill=(217, 79, 4))
    d.polygon([(fx - 12, hy0), (fx - 4, hy0 - 18), (fx + 4, hy0 - 6),
               (fx + 12, hy0 - 20), (fx + 16, hy0)], fill=(242, 193, 78))
    # smoke drifting up-right
    for (sx, sy, r) in [(fx + 34, hy0 - 34, 9), (fx + 52, hy0 - 46, 11),
                        (fx + 72, hy0 - 56, 8)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(120, 120, 120))
    # wave lines
    d.line([x0 + 10, y1 - 8, x1 - 10, y1 - 8], fill=(191, 227, 242), width=2)


def draw_cyclone(d, x0, y0, w, h):
    """Cyclone spiral over the sea, coastline below, warning triangle."""
    x1, y1 = x0 + w, y0 + h
    d.rectangle([x0, y0, x1, y0 + 42], fill=(223, 234, 242))   # sky
    d.rectangle([x0, y0 + 42, x1, y1], fill=(47, 111, 178))    # sea
    cx, cy = x0 + w // 2 - 50, y0 + 50
    for r, start, end in [(40, 20, 300), (30, 140, 60), (20, 260, 180)]:
        d.arc([cx - r, cy - r, cx + r, cy + r], start, end,
              fill=(255, 255, 255), width=7)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(255, 255, 255),
              outline=(47, 111, 178), width=2)  # eye
    d.polygon([(x0, y1), (x0, y1 - 16), (x0 + 120, y1 - 20),
               (x0 + 260, y1 - 14), (x0 + 380, y1 - 20), (x1, y1 - 15),
               (x1, y1)], fill=(201, 168, 106))
    tx, ty = x1 - 46, y0 + 8
    d.polygon([(tx + 17, ty), (tx + 36, ty + 32), (tx, ty + 32)],
              fill=(217, 79, 4))
    f = font(SANS_BOLD, 24)
    d.text((tx + 17, ty + 18), "!", font=f, fill=(255, 255, 255),
           anchor="mm")


def draw_cricket(d, x0, y0, w, h):
    """Cricket: stumps on the pitch, a red ball in the air, a bat."""
    x1, y1 = x0 + w, y0 + h
    d.rectangle([x0, y0, x1, y1], fill=(230, 240, 230))
    # pitch strip
    d.rectangle([x0 + 40, y0 + h * 0.52, x1 - 40, y0 + h * 0.86],
                fill=(201, 168, 106))
    # crease lines
    d.line([x0 + 40, y0 + h * 0.60, x1 - 40, y0 + h * 0.60],
           fill=(255, 255, 255), width=2)
    # stumps (three, centre-left): pale wood with a dark outline so they
    # read against the tan pitch
    sx = x0 + w * 0.30
    for i in range(3):
        d.rectangle([sx + i * 13, y0 + h * 0.30, sx + i * 13 + 9,
                     y0 + h * 0.60], fill=(245, 240, 225),
                    outline=(90, 70, 40), width=1)
    # bails
    d.rectangle([sx, y0 + h * 0.27, sx + 35, y0 + h * 0.30],
                fill=(245, 240, 225), outline=(90, 70, 40), width=1)
    # bat: blade + handle, leaning on the stumps
    bx = sx + 56
    d.polygon([(bx, y0 + h * 0.26), (bx + 20, y0 + h * 0.26),
               (bx + 12, y0 + h * 0.62), (bx - 8, y0 + h * 0.62)],
              fill=(139, 94, 52), outline=(90, 60, 30))
    d.rectangle([bx + 4, y0 + h * 0.10, bx + 12, y0 + h * 0.27],
                fill=(90, 60, 30))
    # red ball in the air, right side
    ballx, bally = x0 + w * 0.80, y0 + h * 0.28
    d.ellipse([ballx - 15, bally - 15, ballx + 15, bally + 15],
              fill=(179, 25, 34))
    d.arc([ballx - 15, bally - 15, ballx + 15, bally + 15], 200, 340,
          fill=(255, 255, 255), width=2)
    # ground line
    d.line([x0 + 20, y0 + h * 0.86, x1 - 20, y0 + h * 0.86],
           fill=(120, 120, 120), width=2)


# ------------------------------------------------------------------- layout
def rule(d, y, width=1, x0=M, x1=W - M):
    d.line([x0, y, x1, y], fill=INK, width=width)


def grid_block(d, bx, by, kicker, headline_lines, subline, draw_pic):
    """One 472x240 story block: picture on top, kicker, 2-line headline,
    subline. (Same geometry as the 18 November entry.)"""
    bw, bh = 472, 240
    ph = 104  # picture height
    d.rectangle([bx, by, bx + bw, by + ph], outline=INK, width=2)
    draw_pic(d, bx + 2, by + 2, bw - 4, ph - 4)
    d.text((bx, by + 112), kicker, font=font(SANS_BOLD, 18), fill=RED,
           anchor="la")
    y = by + 134
    for ln in headline_lines:
        hf = fit(SERIF_BOLD, ln, 32, bw - 8, floor=26)
        d.text((bx, y), ln, font=hf, fill=INK, anchor="la")
        y += 32
    sf = fit(SANS, subline, 26, bw - 8, floor=21)
    d.text((bx, by + 202), subline, font=sf, fill=SUB, anchor="la")


def narrow_block(d, bx, by, kicker, headline_lines, subline, draw_pic):
    """One 310x240 story block: smaller picture, kicker, 2-line headline,
    one-line subline."""
    bw = 310
    ph = 96  # picture height
    d.rectangle([bx, by, bx + bw, by + ph], outline=INK, width=2)
    draw_pic(d, bx + 2, by + 2, bw - 4, ph - 4)
    d.text((bx, by + 104), kicker, font=font(SANS_BOLD, 17), fill=RED,
           anchor="la")
    y = by + 126
    for ln in headline_lines:
        hf = fit(SERIF_BOLD, ln, 30, bw - 8, floor=24)
        d.text((bx, y), ln, font=hf, fill=INK, anchor="la")
        y += 30
    sf = fit(SANS, subline, 22, bw - 8, floor=17)
    d.text((bx, by + 198), subline, font=sf, fill=SUB, anchor="la")


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    title = "THE WORLD TODAY"
    tf = fit(SERIF_BOLD, title, 92, CW, floor=60)
    d.text((W // 2, 70), title, font=tf, fill=INK, anchor="mm")
    rule(d, 126, width=3)
    rule(d, 132, width=1)

    # ---- date, named prominently
    date = "THURSDAY 19 NOVEMBER 2026"
    df = fit(SANS_BOLD, date, 42, 820, floor=30)
    d.text((W // 2, 160), date, font=df, fill=RED, anchor="mm")
    d.text((W // 2, 192), "SIX STORIES FROM ONE DAY",
           font=font(SANS, 19), fill=GREY, anchor="mm")
    rule(d, 212, width=1)

    # ---- lead story: trilateral summit (picture left, text right)
    ly0, ly1 = 222, 470
    d.rectangle([M, ly0, M + 388, ly1], outline=INK, width=2)
    draw_summit(d, M + 2, ly0 + 2, 384, ly1 - ly0 - 4)
    tx = M + 408
    d.text((tx, 246), "DIPLOMACY", font=font(SANS_BOLD, 20), fill=RED,
           anchor="la")
    lead_head = ["XI, TRUMP, PUTIN", "MEET IN SHENZHEN"]
    lh = [fit(SERIF_BOLD, ln, 56, W - M - tx, floor=44) for ln in lead_head]
    d.text((tx, 274), lead_head[0], font=lh[0], fill=INK, anchor="la")
    d.text((tx, 338), lead_head[1], font=lh[1], fill=INK, anchor="la")
    d.text((tx, 410), "First-ever trilateral summit.",
           font=font(SANS, 27), fill=SUB, anchor="la")
    sub2 = "Nuclear arms, Ukraine, Iran on agenda."
    sf2 = fit(SANS, sub2, 27, W - M - tx, floor=24)
    d.text((tx, 444), sub2, font=sf2, fill=SUB, anchor="la")

    # ---- divider
    rule(d, 484, width=2)

    # ---- row 1: three narrow blocks (ICJ, GTA VI, Hormuz)
    narrow_block(d, M, 496, "JUSTICE", ["ICJ RULES ON", "ROHINGYA CASE"],
                 "Verdict today; first in a decade.", draw_court_narrow)
    narrow_block(d, 357, 496, "CULTURE", ["GTA VI GOES", "LIVE WORLDWIDE"],
                 "Out at midnight; Metacritic 99.", draw_gamepad)
    narrow_block(d, 686, 496, "MIDDLE EAST",
                 ["IRAN SAYS 3", "TANKERS HIT MINES"],
                 "Fires east of Hormuz; unverified.", draw_tanker)

    # ---- row 2: two wide blocks (Akvan, India v NZ Test)
    grid_block(d, M, 748, "WEATHER", ["AKVAN TURNS", "VERY SEVERE"],
               "Very severe by tonight; landfall Friday.", draw_cyclone)
    grid_block(d, 524, 748, "SPORT", ["INDIA v NZ", "TEST BEGINS"],
               "First Test starts in Wellington today.", draw_cricket)

    img.save(OUT, format="PNG")
    size = os.path.getsize(OUT)
    print(f"wrote {OUT}: {size} bytes, {W}x{H}")
    return size


if __name__ == "__main__":
    build()
