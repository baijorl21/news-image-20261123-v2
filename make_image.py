#!/usr/bin/env python3
"""Draw entry.png: one picture summing up the world news of Monday 23 November 2026.

All artwork is drawn from scratch with PIL primitives and text: no photos,
no copyrighted assets, no outlet logos. Run: python3 make_image.py

Stories (verified against Reuters/AP/AFP/Anadolu coverage, 23-24 Nov 2026):
COP31 collapses with no deal; Iran war widens at Hormuz/Bahrain; Ukraine
sinks the Russian corvette Merkury off Libya; AI market meltdown; Democrats
reach 258 House seats; Indonesia factory fire (24 dead) and the EU-Indonesia
trade pact.
"""
import math

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
BACKDROP = (20, 22, 26)
CARD = (30, 34, 42)
CARD_EDGE = (64, 72, 88)
RED = (229, 72, 77)
AMBER = (245, 166, 35)
BLUE = (76, 141, 255)
WHITE = (244, 246, 250)
MIST = (176, 190, 208)
LEAF = (120, 220, 160)

SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def face(size, bold=True):
    return ImageFont.truetype(SANS_BOLD if bold else SANS, size)


def wrapped(draw, text, fnt, max_width):
    """Greedy word wrap against a pixel width."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def gavel(draw, cx, cy):
    # gavel head + handle, diagonal; fits within +/-40 of center
    draw.line([cx - 24, cy + 24, cx + 24, cy - 24], fill=AMBER, width=9)
    draw.line([cx - 20, cy - 20, cx + 32, cy + 32], fill=WHITE, width=7)
    draw.rectangle([cx - 38, cy + 30, cx + 22, cy + 38], fill=MIST)


def tanker(draw, cx, cy):
    # hull
    draw.polygon([(cx - 70, cy), (cx + 70, cy), (cx + 56, cy + 26),
                  (cx - 56, cy + 26)], fill=AMBER)
    draw.rectangle([cx - 30, cy - 22, cx + 10, cy], fill=AMBER)
    draw.rectangle([cx + 26, cy - 14, cx + 46, cy], fill=AMBER)
    # small flame above the deck
    draw.ellipse([cx - 10, cy - 40, cx + 10, cy - 24], fill=RED)
    draw.polygon([(cx - 7, cy - 26), (cx + 7, cy - 26), (cx, cy - 40)], fill=RED)


def capsized_ship(draw, cx, cy):
    # hull upside down, bow pointing up-left
    draw.polygon([(cx - 66, cy - 6), (cx + 66, cy - 6), (cx + 44, cy + 22),
                  (cx - 44, cy + 22)], fill=BLUE)
    draw.polygon([(cx - 66, cy - 6), (cx - 34, cy - 30), (cx + 6, cy - 6)],
                 fill=BLUE)
    # waves
    for k, wy in enumerate((cy + 30, cy + 38)):
        draw.arc([cx - 70 + k * 20, wy - 6, cx - 20 + k * 20, wy + 6],
                 start=0, end=180, fill=MIST, width=4)
        draw.arc([cx + 4 + k * 20, wy - 6, cx + 54 + k * 20, wy + 6],
                 start=0, end=180, fill=MIST, width=4)


def falling_chart(draw, cx, cy):
    pts = [(cx - 70, cy - 38), (cx - 30, cy - 14), (cx + 6, cy - 24),
           (cx + 40, cy + 8), (cx + 70, cy + 38)]
    draw.line(pts, fill=RED, width=7)
    for px, py in pts:
        draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=WHITE)
    draw.polygon([(cx + 70, cy + 44), (cx + 52, cy + 34), (cx + 58, cy + 56)],
                 fill=RED)


def dome(draw, cx, cy):
    # capitol dome + columns
    draw.arc([cx - 34, cy - 40, cx + 34, cy + 6], start=180, end=360, fill=BLUE, width=6)
    draw.rectangle([cx - 34, cy - 6, cx + 34, cy + 2], fill=BLUE)
    draw.line([cx, cy - 44, cx, cy - 40], fill=BLUE, width=5)
    for k in range(-2, 3):
        x = cx + k * 15
        draw.line([x, cy + 4, x, cy + 30], fill=WHITE, width=5)
    draw.rectangle([cx - 46, cy + 30, cx + 46, cy + 38], fill=WHITE)


def flame_and_rings(draw, cx, cy):
    # flame (left) + interlocked rings (right)
    fx, fy = cx - 38, cy
    outer = [(fx, fy - 34), (fx + 18, fy - 2), (fx + 20, fy + 18),
             (fx + 9, fy + 30), (fx - 9, fy + 30), (fx - 20, fy + 18),
             (fx - 18, fy - 2)]
    draw.polygon(outer, fill=(255, 130, 60))
    draw.polygon([(fx, fy - 4), (fx + 10, fy + 14), (fx + 5, fy + 28),
                  (fx - 5, fy + 28), (fx - 10, fy + 14)], fill=AMBER)
    rx = cx + 34
    draw.ellipse([rx - 30, cy - 22, rx + 4, cy + 22], outline=BLUE, width=5)
    draw.ellipse([rx - 4, cy - 22, rx + 30, cy + 22], outline=WHITE, width=5)


def fit_font(draw, text, start_size, max_width, bold=True):
    """Largest font size (down from start_size) that fits max_width."""
    size = start_size
    while size > 12 and draw.textlength(text, font=face(size, bold)) > max_width:
        size -= 1
    return face(size, bold)


def panel(draw, box, title, color, body, stat, icon):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=14, fill=CARD, outline=CARD_EDGE, width=3)
    draw.rectangle([x0, y0, x0 + 9, y1], fill=color)
    inner = x1 - x0 - 36
    ty = y0 + 14
    for piece in wrapped(draw, title, face(30), inner):
        draw.text((x0 + 24, ty), piece, font=face(30), fill=color)
        ty += 36
    # icon row
    iy = ty + 44
    icon(draw, (x0 + x1) // 2, iy)
    by = iy + 50
    for line in body:
        for piece in wrapped(draw, line, face(23, bold=False), inner):
            draw.text((x0 + 24, by), piece, font=face(23, bold=False), fill=WHITE)
            by += 27
    stat_font = fit_font(draw, stat, 25, inner)
    draw.text((x0 + 24, y1 - 38), stat, font=stat_font, fill=color)


def build():
    img = Image.new("RGB", (SIZE, SIZE), BACKDROP)
    d = ImageDraw.Draw(img)

    # Masthead
    d.text((24, 22), "ONE IMAGE  ·  ONE DAY  ·  THE WORLD", font=face(25), fill=AMBER)
    d.text((24, 56), "NO DEAL. MORE WAR.", font=face(64), fill=WHITE)
    d.text((24, 124), "MELTDOWN.", font=face(64), fill=RED)
    d.text((24, 196), "MONDAY 23 NOVEMBER 2026", font=face(28), fill=MIST)
    d.rectangle([24, 238, 1000, 243], fill=RED)

    # 3x2 grid of story panels
    gx, gy, gw, gh, gap = 16, 258, 322, 306, 12
    panels = [
        ("COP31 COLLAPSES", RED,
         ["No deal in Antalya.", "0 fossil-fuel mentions", "in the final text."],
         "1ST FAILURE SINCE 2009", gavel),
        ("IRAN WAR WIDENS", RED,
         ["Missiles hit US bases", "in Bahrain; tankers", "burn at Hormuz."],
         "PAUSE TIL 2027?", tanker),
        ("WARSHIP SUNK IN LIBYA", RED,
         ["Ukraine drones sink", "Russian corvette", "Merkury in Benghazi."],
         "KYIV: CHILD PULLED ALIVE", capsized_ship),
        ("AI MELTDOWN", AMBER,
         ["Nvidia -45% from peak.", "Nikkei -5.06% Friday.", "Anthropic IPO fades."],
         "$2.7T ERASED", falling_chart),
        ("DEMOCRATS' 258", BLUE,
         ["Biggest House majority", "since 1992.", "+44 seats vs 2018."],
         "258 SEATS", dome),
        ("DISASTER & A DEAL", AMBER,
         ["Factory fire in Indonesia:", "24 dead, ~30 missing.", "EU-Indonesia pact: 730M."],
         "FIRE + PACT", flame_and_rings),
    ]
    for i, (title, color, body, stat, icon) in enumerate(panels):
        col, row = i % 3, i // 3
        x0 = gx + col * (gw + gap)
        y0 = gy + row * (gh + gap)
        panel(d, (x0, y0, x0 + gw, y0 + gh), title, color, body, stat, icon)

    # Ticker
    ty = 908
    d.rectangle([0, ty, SIZE, ty + 44], fill=(12, 13, 16))
    ticker = "ALCARAZ WINS ATP FINALS  ·  MARQUEZ 8TH TITLE  ·  DELTA OUTAGE: 1,000+ FLIGHTS  ·  POLAND SCRAMBLES JETS  ·  BOLSONARO IN ICU"
    ticker_font = fit_font(d, ticker, 20, SIZE - 32)
    d.text((16, ty + 10), ticker, font=ticker_font, fill=MIST)

    # Footer
    d.text((16, 966), "Sources: Reuters · AP · AFP · Anadolu · Irish Times",
           font=face(20, bold=False), fill=MIST)
    d.text((16, 992), "Drawn from scratch — no photos. One day: 23 November 2026.",
           font=face(18, bold=False), fill=(120, 130, 145))

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    build()
