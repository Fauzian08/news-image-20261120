#!/usr/bin/env python3
"""Draw the news-image-20261120 poster: THE WORLD IN ONE DAY, Friday 20 Nov 2026.

Renders entry.png (1024x1024) from the story data embedded below with PIL
shapes and text only. No network, no external images, no downloaded fonts.
Run: python3 draw.py  (writes entry.png next to this file)
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 16

PAPER = (247, 242, 231)
INK = (26, 26, 26)
GRAY = (90, 86, 78)
LIGHT = (223, 216, 200)
RED = (176, 58, 46)
BLUE = (31, 78, 121)
TEAL = (15, 118, 110)
GOLD = (146, 110, 16)
DARK = (32, 32, 34)
WHITE = (255, 255, 255)
CREAM = (255, 252, 244)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            trial = cur + " " + w
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


TAG_COLORS = {
    "REPORTED": (15, 118, 110),
    "CLAIM": (180, 83, 9),
    "FORECAST": (55, 48, 163),
}


def chip(draw, x, y, tag, fnt):
    """Draw a tag pill; returns its width."""
    tw = draw.textlength(tag, font=fnt)
    w = int(tw) + 12
    h = 16
    draw.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=TAG_COLORS[tag])
    draw.text((x + 6, y + 3), tag, font=fnt, fill=WHITE)
    return w


# ---------------------------------------------------------------- stories
# tag: REPORTED = as reported; CLAIM = single-source/contested;
# FORECAST = a stated plan about the future.
CARDS = [
    {
        "kicker": "MIDDLE EAST  ·  RIYADH",
        "color": RED,
        "art": "riyadh",
        "head": "HOUTHI MISSILE HITS\nRIYADH\u2019S TALLEST TOWER",
        "sub": ("PIF Tower: windows out on 7\u20138 floors; no injuries."),
        "tag": "REPORTED",
    },
    {
        "kicker": "EUROPE  ·  KYIV",
        "color": BLUE,
        "art": "kyiv",
        "head": "OVERNIGHT STRIKES\nKILL 6 IN KYIV",
        "sub": ("Ballistic strikes hit three Dnipro bridges overnight. "
                "EU to summon Russia\u2019s envoy over embassy damage "
                "in the capital."),
        "tag": "REPORTED",
    },
    {
        "kicker": "ASIA-PACIFIC  ·  INDIA",
        "color": TEAL,
        "art": "cyclone",
        "head": "CYCLONE AKVAN HITS\nINDIA\u2019S EAST COAST",
        "sub": ("Third cyclone in a month crosses the coast near Gopalpur "
                "at 70\u201380 km/h. About 300,000 people evacuated; "
                "no major damage reported yet."),
        "tag": "REPORTED",
    },
]

# (headline, subline, tag)
STORIES = [
    ("Nepal PM to make first state visit to India",
     "Balendra Shah to meet Modi in New Delhi", "REPORTED"),
    ("White House fires cyber chief after tech chaos",
     "Dismissal follows a string of technology failures", "REPORTED"),
    ("Trump: no rush on new Iran strikes, eyes 2027",
     "President says decision can wait; 2027 in view", "FORECAST"),
    ("COP31 wraps up in Türkiye",
     "Summit closes; final text omits fossil-fuel phase-out", "REPORTED"),
    ("Poland lifts air-threat warning at border",
     "Unknown objects near Ukraine border under investigation", "REPORTED"),
    ("UK pledges 1,000+ drones for Ukraine, \u00a3260m",
     "New military package announced in London", "REPORTED"),
    ("Argentina Senate backs disability law, 71\u20130",
     "Permanent framework approved unanimously", "REPORTED"),
    ("US sanctions Comancheros and \u2018Ndrangheta",
     "Treasury targets two crime groups", "REPORTED"),
    ("Trump posthumously pardons Pete Rose",
     "Baseball\u2019s banned hits leader cleared", "REPORTED"),
    ("Gas blast kills 6 in Georgia, block collapses",
     "Residential building destroyed in explosion", "REPORTED"),
    ("UK\u2013EU youth mobility scheme agreed",
     "Deal on young people living and working abroad", "REPORTED"),
    ("Meta \u2018reevaluating\u2019 2030 net-zero target",
     "AI buildout blamed for climate goal rethink", "REPORTED"),
    ("US auctions first-ever deep-sea mining leases",
     "Seabed blocks go under the hammer", "REPORTED"),
    ("Somalia expels UAE ambassador",
     "Mogadishu alleges UAE interference", "REPORTED"),
    ("Gaza: 65,000 tents wait as winter nears",
     "Gazans return as Israeli ground operation ends", "REPORTED"),
    ("Malaysia to resettle 10,000 Rohingya in Turkey",
     "UNGA chief tells Myanmar to \u2018bring Rohingya home\u2019", "FORECAST"),
    ("Xi\u2013Albanese talks in Shenzhen",
     "Xi urges trust-based partnership", "REPORTED"),
    ("Senegal boat capsizing kills 4",
     "Deaths amid a surge in migration crossings", "REPORTED"),
]

TIMELINE = [
    ("OVERNIGHT", "Kyiv: overnight strikes kill 6, hit 3 Dnipro bridges"),
    ("MORNING", "Akvan makes landfall near Gopalpur, 08:00 IST"),
    ("MIDDAY", "White House fires cyber chief"),
    ("AFTERNOON", "EU to summon Russian envoy over Kyiv damage"),
    ("LATE AFT.", "UK pledges 1,000+ drones for Ukraine"),
    ("EVENING", "COP31 wraps up in Türkiye"),
]

EXCLUDED = ("ICJ Myanmar genocide verdict  ·  Anthropic Nasdaq debut (+17%)  ·  "
            "US Senate rejects Iran war-powers vote 51\u201348  ·  APEC Shenzhen closes  ·  "
            "Voyager 1 phones home  ·  Fiona the hippo dies  ·  "
            "Xi\u2013Trump\u2013Putin peace declaration  \u2014  ALL 19 NOV")

# Rough continent outlines in (lon, lat); drawn on an equirectangular strip.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
     (-80, 62), (-75, 45), (-80, 32), (-85, 26), (-90, 21), (-97, 16),
     (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-140, 60),
     (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 5), (-60, 0), (-50, -5), (-35, -8), (-40, -20),
     (-48, -28), (-55, -35), (-65, -45), (-70, -52), (-73, -40),
     (-75, -25), (-80, -15), (-81, -5), (-80, 5)],
    [(-10, 36), (-5, 43), (-2, 48), (0, 51), (5, 55), (10, 58), (18, 56),
     (20, 60), (25, 65), (30, 70), (40, 68), (45, 60), (40, 50), (35, 45),
     (30, 40), (25, 38), (20, 40), (12, 44), (5, 43), (-2, 37), (-9, 38)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (40, 15), (48, 10), (50, 0), (40, -10), (35, -20), (30, -30),
     (20, -35), (15, -30), (12, -18), (8, -5), (0, 5), (-8, 5), (-15, 10)],
    [(40, 68), (60, 70), (80, 72), (100, 75), (130, 72), (160, 70),
     (178, 65), (160, 60), (140, 55), (130, 45), (120, 40), (110, 30),
     (100, 20), (95, 10), (90, 15), (80, 8), (75, 20), (65, 25), (55, 28),
     (48, 30), (42, 40), (40, 50)],
    [(113, -22), (114, -30), (115, -35), (125, -35), (135, -38), (145, -38),
     (150, -35), (153, -28), (150, -22), (145, -15), (140, -12),
     (135, -15), (130, -13), (125, -15), (120, -20), (115, -22)],
]

# (lon, lat, label or None)
MAP_POINTS = [
    (114, 22, "Shenzhen"), (30, 50, "Kyiv"), (47, 25, "Riyadh"),
    (-77, 39, "Washington"), (85, 19, "Gopalpur"), (0, 51, "London"),
    (-58, -35, "Buenos Aires"), (45, 2, None), (34, 31, "Gaza"),
    (149, -35, None), (17, 15, "Dakar"),
]


def draw_globe(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(178, 216, 230),
                 outline=BLUE, width=3)
    for k in (-0.55, 0, 0.55):
        x0 = cx + k * r
        draw.arc([x0 - r * 0.45, cy - r, x0 + r * 0.45, cy + r],
                 start=270, end=90, fill=BLUE, width=2)
        draw.arc([x0 - r * 0.45, cy - r, x0 + r * 0.45, cy + r],
                 start=90, end=270, fill=BLUE, width=2)
    for k in (-0.5, 0, 0.5):
        y0 = cy + k * r
        draw.arc([cx - r, y0 - r * 0.4, cx + r, y0 + r * 0.4],
                 start=180, end=360, fill=BLUE, width=2)
        draw.arc([cx - r, y0 - r * 0.4, cx + r, y0 + r * 0.4],
                 start=0, end=180, fill=BLUE, width=2)


def draw_art(draw, kind, x, y, w, h):
    """Illustration panel for a lead card."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 226, 208),
                   outline=LIGHT, width=1)
    if kind == "riyadh":
        # dusk sky over Riyadh; PIF Tower struck, missile streak inbound
        draw.rectangle([x, y, x + w, y + h], fill=(66, 50, 82))
        draw.rectangle([x, y + h - 34, x + w, y + h], fill=(214, 128, 64))
        for sx, sy in [(x + 24, y + 12), (x + 62, y + 22), (x + 292, y + 10)]:
            draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=WHITE)
        # skyline silhouettes
        draw.rectangle([x, y + h - 26, x + 70, y + h], fill=(38, 34, 48))
        draw.rectangle([x + 78, y + h - 34, x + 140, y + h], fill=(38, 34, 48))
        draw.rectangle([x + 240, y + h - 30, x + w, y + h], fill=(38, 34, 48))
        # PIF Tower: tall slab with a slanted top
        tx0, tx1 = x + 168, x + 216
        draw.polygon([(tx0, y + h), (tx0, y + 16), (tx1, y + 8),
                      (tx1, y + h)], fill=(52, 48, 66))
        # lit windows, with the impact floor blown out in orange
        for wy in range(y + 26, y + h - 8, 9):
            for wx in (tx0 + 8, tx0 + 20, tx0 + 32):
                fill = (255, 110, 40) if wy == y + 44 else (255, 205, 110)
                draw.rectangle([wx, wy, wx + 5, wy + 4], fill=fill)
        # missile streak diving at the tower
        draw.line([x + 28, y + 10, tx0 + 4, y + 38], fill=(255, 220, 140),
                  width=3)
        draw.line([x + 28, y + 10, tx0 - 28, y + 28], fill=(255, 160, 60),
                  width=2)
        # blast flash at the impact point
        bx, by = tx0 + 4, y + 40
        draw.ellipse([bx - 13, by - 13, bx + 13, by + 13],
                     fill=(255, 190, 60))
        draw.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=(255, 240, 180))
        # smoke drifting off the blast
        draw.ellipse([bx + 8, by - 18, bx + 24, by - 6], fill=(150, 142, 148))
    elif kind == "kyiv":
        # night sky, domed cathedral, bridge arcs
        draw.rectangle([x, y, x + w, y + h], fill=(38, 52, 84))
        for sx, sy in [(x + 30, y + 18), (x + 260, y + 30), (x + 150, y + 12)]:
            draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=WHITE)
        draw.ellipse([x + w - 52, y + 12, x + w - 28, y + 36],
                     fill=(240, 230, 200))
        bx, by = x + 40, y + h - 60
        draw.rectangle([bx, by, bx + 130, y + h], fill=(212, 196, 160))
        for dx, dw, dh in [(8, 26, 26), (52, 34, 32), (104, 26, 26)]:
            draw.rectangle([bx + dx, by - dh + 14, bx + dx + dw, by + 14],
                           fill=(212, 196, 160))
            draw.ellipse([bx + dx - 2, by - dh - 2, bx + dx + dw + 2,
                          by - dh + 18], fill=(176, 58, 46))
        draw.arc([x + 200, y + h - 46, x + 300, y + h + 30], start=180,
                 end=360, fill=(255, 215, 0), width=4)
        draw.arc([x + 210, y + h - 30, x + 290, y + h + 22], start=180,
                 end=360, fill=(255, 215, 0), width=3)
    elif kind == "cyclone":
        # sea + coastline + spiral storm
        draw.rectangle([x, y, x + w, y + h], fill=(178, 216, 230))
        draw.polygon([(x, y + h), (x + 120, y + h - 40), (x + w, y + h - 70),
                      (x + w, y + h)], fill=(154, 165, 120))
        cx, cy = x + w // 2, y + h // 2 - 6
        for r in (14, 26, 38, 50):
            draw.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300,
                     fill=WHITE, width=5)
        draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED)
        for rx in range(x + 20, x + w - 10, 26):
            draw.line([rx, y + h - 12, rx - 8, y + h - 26], fill=BLUE, width=2)


def draw_card(draw, card, x, y, w, h):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CREAM,
                           outline=LIGHT, width=1)
    # header band
    draw.rounded_rectangle([x, y, x + w, y + 30], radius=10, fill=card["color"])
    draw.rectangle([x, y + 20, x + w, y + 30], fill=card["color"])
    draw.text((x + 12, y + 8), card["kicker"], font=font(BOLD, 12), fill=WHITE)
    chip(draw, x + w - 82, y + 7, card["tag"], font(BOLD, 9))
    # illustration
    draw_art(draw, card["art"], x + 10, y + 40, w - 20, 104)
    # headline
    f_head = font(BOLD, 20)
    hy = y + 152
    for line in card["head"].split("\n"):
        draw.text((x + 12, hy), line, font=f_head, fill=INK)
        hy += 24
    # sub
    f_sub = font(REG, 12)
    lines = wrap(draw, card["sub"], f_sub, w - 24)
    sy = hy + 6
    for line in lines[:4]:
        draw.text((x + 12, sy), line, font=f_sub, fill=(64, 60, 52))
        sy += 16


def draw_map(draw, x, y, w, h):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=8,
                           fill=(223, 232, 234), outline=LIGHT, width=1)
    lon0, lon1, lat0, lat1 = -180, 180, 78, -56

    def proj(lon, lat):
        px = x + (lon - lon0) / (lon1 - lon0) * w
        py = y + (lat0 - lat) / (lat0 - lat1) * h
        return px, py

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=(154, 165, 120), outline=(107, 114, 86))
    f_lab = font(BOLD, 10)
    for lon, lat, label in MAP_POINTS:
        px, py = proj(lon, lat)
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED,
                     outline=WHITE, width=2)
        if label:
            draw.text((px + 6, py - 6), label, font=f_lab, fill=INK,
                      stroke_width=2, stroke_fill=WHITE)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.text((MARGIN, 12), "THE WORLD IN ONE DAY", font=font(SERIF, 40), fill=INK)
    d.text((W - MARGIN, 18), "FRIDAY 20 NOVEMBER 2026", font=font(BOLD, 22),
           fill=RED, anchor="ra")
    d.text((MARGIN, 60),
           "The day\u2019s world news \u2014 every story below happened or was first reported today.",
           font=font(REG, 13), fill=GRAY)
    d.text((W - MARGIN, 60), "21 STORIES  ·  6 REGIONS", font=font(BOLD, 12),
           fill=INK, anchor="ra")
    d.line([(MARGIN, 86), (W - MARGIN, 86)], fill=INK, width=2)
    d.line([(MARGIN, 89), (W - MARGIN, 89)], fill=INK, width=1)

    # ---- three lead cards
    cw, gap = 328, 8
    for i, card in enumerate(CARDS):
        draw_card(d, card, MARGIN + i * (cw + gap), 96, cw, 272)

    # ---- world map strip
    d.text((MARGIN, 376), "WHERE IT HAPPENED", font=font(BOLD, 14), fill=INK)
    d.text((W - MARGIN, 378),
           "7 AMERICAS  ·  5 EUROPE  ·  4 ASIA-PACIFIC  ·  2 MIDDLE EAST  ·  "
           "2 AFRICA  ·  1 GLOBAL",
           font=font(BOLD, 11), fill=GRAY, anchor="ra")
    draw_map(d, MARGIN, 396, W - 2 * MARGIN, 128)

    # ---- story grid
    d.text((MARGIN, 532), "THE DAY\u2019S NEWS \u2014 EVERY STORY TAGGED",
           font=font(BOLD, 14), fill=INK)
    f_head, f_sub, f_tag = font(BOLD, 13), font(REG, 11), font(BOLD, 9)
    col_w = 488
    for i, (head, sub, tag) in enumerate(STORIES):
        col = i % 2
        row = i // 2
        x = MARGIN + col * (col_w + 16)
        y = 554 + row * 32
        chip(d, x, y + 1, tag, f_tag)
        d.text((x + 74, y), head, font=f_head, fill=INK)
        d.text((x + 74, y + 16), sub, font=f_sub, fill=GRAY)

    # ---- timeline
    d.text((MARGIN, 850), "THE DAY, IN ORDER", font=font(BOLD, 13), fill=INK)
    d.line([(MARGIN + 8, 884), (W - MARGIN - 8, 884)], fill=(150, 144, 130),
           width=2)
    slot = (W - 2 * MARGIN) / len(TIMELINE)
    for i, (when, what) in enumerate(TIMELINE):
        cx = MARGIN + slot * i + slot / 2
        d.ellipse([cx - 5, 879, cx + 5, 889], fill=RED, outline=WHITE, width=2)
        d.text((cx, 866), when, font=font(BOLD, 10), fill=RED, anchor="ma")
        lines = wrap(d, what, font(REG, 11), slot - 14)
        ty = 894
        for line in lines[:2]:
            d.text((cx, ty), line, font=font(REG, 11), fill=INK, anchor="ma")
            ty += 13

    # ---- date check strip
    d.rounded_rectangle([MARGIN, 930, W - MARGIN, 996], radius=8, fill=DARK)
    d.text((MARGIN + 12, 938), "\u2715  DATE CHECK \u2014 NOT 20 NOV, EXCLUDED:",
           font=font(BOLD, 13), fill=WHITE)
    f_exc = font(REG, 11)
    lines = wrap(d, EXCLUDED, f_exc, W - 2 * MARGIN - 24)
    ey = 958
    for line in lines[:2]:
        d.text((MARGIN + 12, ey), line, font=f_exc, fill=(210, 205, 195))
        ey += 15

    # ---- footer
    d.text((W // 2, 1002),
           "Tags \u2014 REPORTED: as reported  ·  CLAIM: single-source or contested  ·  "
           "FORECAST: about the future  ·  Drawn from wire reports published 20 Nov 2026",
           font=font(REG, 10), fill=GRAY, anchor="ma")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
