#!/usr/bin/env python3
"""Render entry.png: one image summing up the world news of 20 November 2026.

A clean newspaper-poster layout, 1024x1024, drawn with Pillow and the
DejaVu fonts. Flat colours + text, so the PNG stays well under 1 MiB.
Run:  python3 render.py   (writes entry.png next to this file)
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

W, H = 1024, 1024

PAPER = (245, 241, 230)      # warm off-white paper
NAVY = (20, 33, 61)          # masthead + headlines
AMBER = (252, 163, 17)       # date line on the masthead
CARD = (255, 255, 255)       # story cards
CARD_EDGE = (216, 210, 192)  # card borders
INK = (51, 48, 42)           # summary text
MUTED = (110, 105, 92)       # kickers
FOOTER_BG = (20, 33, 61)     # footer strip
FOOTER_INK = (235, 231, 220) # footer text

CHIP_COLORS = [
    (185, 28, 28),   # 1 genocide ruling - red
    (29, 78, 216),   # 2 trilateral summit - blue
    (180, 83, 9),    # 3 Kyiv strikes - burnt orange
    (124, 58, 237),  # 4 Riyadh hit - purple
    (21, 128, 61),   # 5 COP31 - green
    (15, 118, 110),  # 6 markets - teal
]

STORIES = [
    (
        "THE HAGUE  •  WORLD COURT",
        "ICJ RULES MYANMAR COMMITTED GENOCIDE",
        "The court finds Myanmar committed genocide against the Rohingya, 9-6 - the first such ruling against a state.",
    ),
    (
        "SHENZHEN  •  SUMMIT",
        "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
        "They sign a joint peace declaration after 70 minutes of talks; no breakthrough on Ukraine, Iran or nuclear arms.",
    ),
    (
        "KYIV  •  WAR IN UKRAINE",
        "RUSSIAN STRIKES HIT KYIV OVERNIGHT",
        "Missile and drone strikes kill 8, injure 28 and hit bridges; Russian missiles and a drone enter Polish airspace.",
    ),
    (
        "RIYADH  •  GULF",
        "HOUTHI MISSILE DAMAGES SAUDI PIF TOWER",
        "A missile damages the sovereign wealth fund tower in Riyadh; Saudi Arabia intercepts another missile and 5 drones.",
    ),
    (
        "ANTALYA  •  CLIMATE",
        "COP31 DRAFT DROPS FOSSIL-FUEL PHASE-OUT",
        "The draft agreement in Turkey removes all references to phasing out fossil fuels.",
    ),
    (
        "MARKETS  •  ECONOMY",
        "STOCKS FALL FOR A FIFTH STRAIGHT DAY",
        "S&P 500 down 2% and Nikkei down 4.8% after Anthropic's debut; IMF warns public debt nears 100% of GDP.",
    ),
]

FOOTER_LINES = [
    "ALSO: Kenya discharges its last Ebola patient  •  Israeli forces cross Gaza's Yellow Line",
    "EU-UK summit in Brussels  •  Italy fines Meta 805m euros over Android photo access",
]


def load_font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap(draw, text, font, max_width):
    """Greedy word wrap, measured with the real font."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    f_title = load_font("DejaVuSans-Bold.ttf", 54)
    f_date = load_font("DejaVuSans-Bold.ttf", 40)
    f_sub = load_font("DejaVuSans.ttf", 22)
    f_kicker = load_font("DejaVuSans-Bold.ttf", 19)
    f_head = load_font("DejaVuSans-Bold.ttf", 29)
    f_body = load_font("DejaVuSans.ttf", 21)
    f_foot = load_font("DejaVuSans.ttf", 20)
    f_chip = load_font("DejaVuSans-Bold.ttf", 22)

    # ---- Masthead -------------------------------------------------------
    draw.rectangle([0, 0, W, 170], fill=NAVY)
    draw.rectangle([0, 170, W, 176], fill=AMBER)
    title = "THE WORLD IN ONE IMAGE"
    tw = draw.textlength(title, font=f_title)
    draw.text(((W - tw) / 2, 24), title, font=f_title, fill=(255, 255, 255))
    date = "FRIDAY, 20 NOVEMBER 2026"
    dw = draw.textlength(date, font=f_date)
    draw.text(((W - dw) / 2, 88), date, font=f_date, fill=AMBER)
    sub = "Six stories that defined the day - from The Hague to Shenzhen to Kyiv"
    sw = draw.textlength(sub, font=f_sub)
    draw.text(((W - sw) / 2, 138), sub, font=f_sub, fill=(210, 208, 198))

    # ---- Story grid: 2 columns x 3 rows ---------------------------------
    margin, gutter = 28, 14
    col_w = (W - 2 * margin - gutter) // 2
    row_h = 240
    top = 188
    for i, (kicker, headline, summary) in enumerate(STORIES):
        row, col = divmod(i, 2)
        x0 = margin + col * (col_w + gutter)
        y0 = top + row * (row_h + gutter)
        x1, y1 = x0 + col_w, y0 + row_h
        color = CHIP_COLORS[i]

        draw.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=CARD,
                               outline=CARD_EDGE, width=2)
        draw.rounded_rectangle([x0, y0, x1, y0 + 8], radius=4, fill=color)

        # Number chip + kicker
        cx, cy = x0 + 16, y0 + 26
        draw.ellipse([cx, cy, cx + 44, cy + 44], fill=color)
        num = str(i + 1)
        nw = draw.textlength(num, font=f_chip)
        draw.text((cx + (44 - nw) / 2, cy + 9), num, font=f_chip,
                  fill=(255, 255, 255))
        draw.text((cx + 56, cy + 11), kicker, font=f_kicker, fill=color)

        # Headline, wrapped to at most 2 lines
        head_lines = wrap(draw, headline, f_head, col_w - 32)
        hy = y0 + 80
        for line in head_lines[:2]:
            draw.text((x0 + 16, hy), line, font=f_head, fill=NAVY)
            hy += 35

        # Summary, wrapped to at most 3 lines
        body_lines = wrap(draw, summary, f_body, col_w - 32)
        by = y0 + 156
        for line in body_lines[:3]:
            draw.text((x0 + 16, by), line, font=f_body, fill=INK)
            by += 26

    # ---- Footer strip: secondary briefs ----------------------------------
    fy0 = top + 3 * row_h + 2 * gutter + 12
    draw.rounded_rectangle([margin, fy0, W - margin, H - 16], radius=10,
                           fill=FOOTER_BG)
    fy = fy0 + 9
    for line in FOOTER_LINES:
        draw.text((margin + 20, fy), line, font=f_foot, fill=FOOTER_INK)
        fy += 27

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
