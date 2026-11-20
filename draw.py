#!/usr/bin/env python3
"""Draw the news-image-20261120 poster, round 3: THE WORLD IN ONE DAY,
Friday 20 Nov 2026. Tiered layout: masthead, stat strip, 3 illustrated
leads, 10 illustrated features, world map + 23-item tail list, DATE CHECK.

Renders entry.png (1024x1024) from the story data embedded below with PIL
shapes and text only. No network, no external images, no downloaded fonts.
Every story was verified as 20 Nov (happened or first reported 20 Nov in
some time zone) before inclusion. Run: python3 draw.py
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
PURPLE = (55, 48, 163)
AMBER = (180, 83, 9)
GREEN = (46, 125, 50)
VIOLET = (90, 60, 140)

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


def chip(draw, x, y, tag, fnt, h=16):
    """Draw a tag pill; returns its width."""
    tw = draw.textlength(tag, font=fnt)
    w = int(tw) + 12
    draw.rounded_rectangle([x, y, x + w, y + h], radius=h // 2,
                           fill=TAG_COLORS[tag])
    draw.text((x + 6, y + (h - fnt.size) // 2 - 1), tag, font=fnt, fill=WHITE)
    return w


# ---------------------------------------------------------------- stories
# Leads 01-03 (verified in rounds 1-2). Features 04-13 (new stories verified
# 20 Nov by web search in the round-3 session). Tail 14-36 (verified in
# rounds 1-2, plus Nicholls verified 20 Nov in round 3).
LEADS = [
    {
        "num": "01", "kicker": "MIDDLE EAST  ·  RIYADH", "color": RED,
        "art": "riyadh", "topic": "CYCLONE" if False else "MISSILE STRIKE",
        "head": "HOUTHI MISSILE HITS\nRIYADH\u2019S TALLEST TOWER",
        "sub": "PIF Tower: windows out on 7\u20138 floors; no injuries. (Reuters)",
        "tag": "REPORTED",
    },
    {
        "num": "02", "kicker": "EUROPE  ·  KYIV", "color": BLUE,
        "art": "kyiv", "topic": "WAR",
        "head": "OVERNIGHT STRIKES\nKILL 6 IN KYIV",
        "sub": "Three Dnipro bridges hit overnight; EU to summon Russia\u2019s envoy. (Reuters)",
        "tag": "REPORTED",
    },
    {
        "num": "03", "kicker": "ASIA-PACIFIC  ·  INDIA", "color": TEAL,
        "art": "cyclone", "topic": "CYCLONE",
        "head": "CYCLONE AKVAN HITS\nINDIA\u2019S EAST COAST",
        "sub": ("Third cyclone in a month crosses near Gopalpur at 70\u201380 km/h; "
                "~300,000 evacuated. (IMD, The Hindu)"),
        "tag": "REPORTED",
    },
]

FEATURES = [
    {
        "num": "04", "kicker": "USA  ·  GAMES", "color": RED, "art": "gta",
        "head": "GTA VI SELLS 24.6M\nCOPIES IN A DAY",
        "sub": "Sensor Tower estimate: $2.36bn on day one (Reuters)",
        "tag": "REPORTED",
    },
    {
        "num": "05", "kicker": "SEOUL/TOKYO", "color": TEAL,
        "art": "markets",
        "head": "AI SELL-OFF SINKS ASIA\nTO WORST WEEK SINCE 2020",
        "sub": "Nikkei \u22125%, Kospi \u22125.2%; MSCI Asia \u22123.2% (Reuters)",
        "tag": "REPORTED",
    },
    {
        "num": "06", "kicker": "SPACE", "color": DARK, "art": "space",
        "head": "BEPICOLOMBO REACHES\nMERCURY",
        "sub": "ESA/JAXA probe ends 6bn-mile trip; orbit insertion Sat. (Reuters)",
        "tag": "REPORTED",
    },
    {
        "num": "07", "kicker": "BRUSSELS  ·  POLITICS", "color": BLUE,
        "art": "flags",
        "head": "BURNHAM SEALS EU\u2013UK\nRESET DEAL",
        "sub": "Food, youth mobility, emissions deals agreed (Reuters)",
        "tag": "REPORTED",
    },
    {
        "num": "08", "kicker": "TOKYO  ·  ECONOMY", "color": TEAL, "art": "cpi",
        "head": "JAPAN INFLATION HITS\n2.3%; BOJ HIKE EYED",
        "sub": "Headline CPI 2.3% in Oct; core 2.2% (Reuters)",
        "tag": "REPORTED",
    },
    {
        "num": "09", "kicker": "WELLINGTON", "color": TEAL,
        "art": "cricket",
        "head": "PHILLIPS MAKES HISTORY\nWITH 118 VS INDIA",
        "sub": "First NZ batter with tons in all formats vs India in a year (Reuters)",
        "tag": "REPORTED",
    },
    {
        "num": "10", "kicker": "BARCELONA  ·  HEALTH", "color": RED, "art": "pill",
        "head": "CANCER PILL SHRINKS\nTUMOURS 60.7%",
        "sub": "Daraxonrasib + chemo, 61 patients, early trial (EORTC)",
        "tag": "REPORTED",
    },
    {
        "num": "11", "kicker": "ANTALYA  ·  CLIMATE", "color": TEAL, "art": "cop31",
        "head": "COP31 WRAPS UP\nIN T\u00dcRKIYE",
        "sub": "Summit closes; final text omits fossil-fuel phase-out (Reuters)",
        "tag": "REPORTED",
    },
    {
        "num": "12", "kicker": "ROME  ·  LABOUR", "color": RED, "art": "italy",
        "head": "ITALY HIT BY NATIONWIDE\nSTRIKE",
        "sub": "CGIL walkout over wages and public spending (Reuters)",
        "tag": "REPORTED",
    },
    {
        "num": "13", "kicker": "NARATHIWAT", "color": GOLD,
        "art": "blast",
        "head": "BLASTS HIT 7 AREAS\nIN SOUTH THAILAND",
        "sub": "Explosions reported across Narathiwat province (NST)",
        "tag": "REPORTED",
    },
]

# (num, place, headline, source, tag)
TAIL = [
    ("14", "NEPAL", "PM to make first state visit to India", "Reuters", "REPORTED"),
    ("15", "USA", "White House fires cyber chief", "AP", "REPORTED"),
    ("16", "USA", "Trump: no rush on Iran strikes", "Reuters", "FORECAST"),
    ("17", "POLAND", "Lifts air-threat warning at border", "Reuters", "REPORTED"),
    ("18", "ARGENTINA", "Senate backs disability law, 71\u20130", "AP", "REPORTED"),
    ("19", "USA", "Trump pardons Pete Rose", "AP", "REPORTED"),
    ("20", "LONDON", "UK\u2013EU youth mobility scheme agreed", "Reuters", "REPORTED"),
    ("21", "USA", "Auctions first deep-sea mining leases", "Reuters", "REPORTED"),
    ("22", "GAZA", "65,000 tents wait as winter nears", "AP", "REPORTED"),
    ("23", "CHINA", "Xi\u2013Albanese talks in Shenzhen", "Reuters", "REPORTED"),
    ("24", "USA", "Sanctions Comancheros, \u2018Ndrangheta", "Reuters", "REPORTED"),
    ("25", "GEORGIA", "Gas blast kills 6, block collapses", "AP", "REPORTED"),
    ("26", "USA", "Meta \u2018reevaluating\u2019 2030 net-zero goal", "Reuters", "REPORTED"),
    ("27", "SOMALIA", "Expels UAE ambassador", "Reuters", "REPORTED"),
    ("28", "MALAYSIA", "To resettle 10,000 Rohingya in Turkey", "Reuters", "FORECAST"),
    ("29", "SENEGAL", "Boat capsizing kills 4", "AFP", "REPORTED"),
    ("30", "USA", "DHS rushes billions for deportations", "CNN", "REPORTED"),
    ("31", "USA", "Democrats warn Trump team: save records", "CNN", "REPORTED"),
    ("32", "CHINA", "Holds lending rates at 3.00% / 3.50%", "Reuters", "REPORTED"),
    ("33", "USA", "Names Kirsten Davies as cyber chief", "Le Monde", "REPORTED"),
    ("34", "UK", "Pledges 1,000+ drones for Ukraine", "Reuters", "REPORTED"),
    ("35", "GERMANY", "Allies meet in Berlin, back talks", "BBC", "REPORTED"),
    ("36", "NZ", "Nicholls scores 175* in 216-run stand", "Reuters", "REPORTED"),
]

# (big number, label) — all verified 20 Nov facts
STATS = [
    ("300,000+", "evacuated ahead of Cyclone Akvan"),
    ("24.6m", "GTA VI copies sold in a day (Sensor Tower est.)"),
    ("\u22125.2%", "Kospi in a day; Asia\u2019s worst week since 2020"),
    ("2.3%", "Japan Oct headline CPI; BoJ hike eyed"),
    ("118", "Phillips\u2019 historic century vs India"),
    ("60.7%", "tumours shrank on daraxonrasib + chemo"),
]

# (label, count, color)
REGIONS = [
    ("EUROPE", 10, BLUE), ("AMERICAS", 11, RED),
    ("ASIA-PACIFIC", 8, TEAL), ("MIDEAST", 2, GOLD),
    ("AFRICA", 2, GREEN), ("OCEANIA", 2, VIOLET),
    ("WORLD/SPACE", 1, DARK),
]

EXCLUDED = ("ICJ Myanmar genocide verdict  ·  Anthropic Nasdaq debut (+17%)  ·  "
            "US Senate rejects Iran war-powers vote 51\u201348  ·  APEC Shenzhen closes  ·  "
            "Voyager 1 phones home  ·  Fiona the hippo dies  ·  "
            "Xi\u2013Trump\u2013Putin peace declaration  ·  "
            "Trump asks court to drop Alaska suit  ·  "
            "Bukele registers third-term bid  \u2014  ALL 19 NOV")

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
    # New Zealand sliver
    [(166, -34), (168, -38), (170, -42), (174, -41), (178, -38), (176, -35)],
]

# (num, lon, lat, dx, dy) — numbered pins for the 13 lead+feature stories.
MAP_PINS = [
    ("01", 47, 25, 0, 0), ("02", 30, 50, 0, 0), ("03", 85, 19, 0, 0),
    ("04", -77, 39, 0, 0), ("05", 127, 37, -2, -3), ("07", 4, 51, 0, 0),
    ("08", 139, 35, 3, 3), ("09", 174.7, -41, 0, 0), ("10", 2, 41, -3, 2),
    ("11", 30, 37, 0, 0), ("12", 12, 42, 4, -2), ("13", 101, 6, 0, 0),
]


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
        draw.rectangle([x, y + h - 26, x + 70, y + h], fill=(38, 34, 48))
        draw.rectangle([x + 78, y + h - 34, x + 140, y + h], fill=(38, 34, 48))
        draw.rectangle([x + 240, y + h - 30, x + w, y + h], fill=(38, 34, 48))
        tx0, tx1 = x + 168, x + 216
        draw.polygon([(tx0, y + h), (tx0, y + 16), (tx1, y + 8),
                      (tx1, y + h)], fill=(52, 48, 66))
        for wy in range(y + 26, y + h - 8, 9):
            for wx in (tx0 + 8, tx0 + 20, tx0 + 32):
                fill = (255, 110, 40) if wy == y + 44 else (255, 205, 110)
                draw.rectangle([wx, wy, wx + 5, wy + 4], fill=fill)
        draw.line([x + 28, y + 10, tx0 + 4, y + 38], fill=(255, 220, 140),
                  width=3)
        draw.line([x + 28, y + 10, tx0 - 28, y + 28], fill=(255, 160, 60),
                  width=2)
        bx, by = tx0 + 4, y + 40
        draw.ellipse([bx - 13, by - 13, bx + 13, by + 13],
                     fill=(255, 190, 60))
        draw.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=(255, 240, 180))
        draw.ellipse([bx + 8, by - 18, bx + 24, by - 6], fill=(150, 142, 148))
    elif kind == "kyiv":
        # night sky, domed cathedral, bridge arcs
        draw.rectangle([x, y, x + w, y + h], fill=(38, 52, 84))
        for sx, sy in [(x + 30, y + 18), (x + 260, y + 30), (x + 150, y + 12)]:
            draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=WHITE)
        draw.ellipse([x + w - 52, y + 12, x + w - 28, y + 36],
                     fill=(240, 230, 200))
        bx, by = x + 40, y + h - 54
        draw.rectangle([bx, by, bx + 130, y + h], fill=(212, 196, 160))
        for dx, dw, dh in [(8, 26, 24), (52, 34, 28), (104, 26, 24)]:
            draw.rectangle([bx + dx, by - dh + 14, bx + dx + dw, by + 14],
                           fill=(212, 196, 160))
            draw.ellipse([bx + dx - 2, by - dh - 2, bx + dx + dw + 2,
                          by - dh + 18], fill=(176, 58, 46))
        draw.arc([x + 200, y + h - 46, x + 300, y + h + 30], start=180,
                 end=360, fill=(255, 215, 0), width=4)
        draw.arc([x + 210, y + h - 30, x + 290, y + h + 22], start=180,
                 end=360, fill=(255, 215, 0), width=3)
    elif kind == "cyclone":
        # sea + coastline + spiral storm (radii scaled to panel height)
        draw.rectangle([x, y, x + w, y + h], fill=(178, 216, 230))
        draw.polygon([(x, y + h), (x + 120, y + h - 40), (x + w, y + h - 70),
                      (x + w, y + h)], fill=(154, 165, 120))
        cx, cy = x + w // 2, y + h // 2 - 4
        for r in (11, 20, 29, 38):
            draw.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300,
                     fill=WHITE, width=5)
        draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED)
        for rx in range(x + 20, x + w - 10, 26):
            draw.line([rx, y + h - 12, rx - 8, y + h - 26], fill=BLUE, width=2)


def draw_mini_art(draw, kind, x, y, w, h):
    """Small illustration strip for a feature card (simple flat shapes)."""
    if kind == "gta":
        draw.rectangle([x, y, x + w, y + h], fill=(32, 32, 48))
        # gamepad body
        draw.rounded_rectangle([x + 14, y + 7, x + 78, y + h - 5], radius=8,
                               fill=(70, 70, 95))
        draw.line([x + 26, y + 13, x + 26, y + h - 11], fill=WHITE, width=3)
        draw.line([x + 20, y + 16, x + 32, y + 16], fill=WHITE, width=3)
        draw.ellipse([x + 58, y + 11, x + 66, y + 19], fill=(255, 200, 60))
        draw.ellipse([x + 68, y + 16, x + 76, y + 24], fill=(255, 110, 60))
        draw.text((x + w - 8, y + 4), "24.6m", font=font(BOLD, 15),
                  fill=(255, 210, 90), anchor="ra")
        draw.text((x + w - 8, y + 19), "COPIES", font=font(BOLD, 7),
                  fill=WHITE, anchor="ra")
    elif kind == "markets":
        draw.rectangle([x, y, x + w, y + h], fill=(24, 24, 26))
        pts = [(x + 6, y + 5), (x + 50, y + 8), (x + 90, y + 6),
               (x + 130, y + 16), (x + w - 8, y + h - 5)]
        draw.line(pts, fill=(255, 80, 60), width=3)
        for px, py in pts:
            draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 200, 60))
        draw.text((x + 8, y + h - 13), "\u22125.2%", font=font(BOLD, 10),
                  fill=(255, 120, 90))
    elif kind == "space":
        draw.rectangle([x, y, x + w, y + h], fill=(20, 30, 58))
        for sx, sy in [(x + 12, y + 6), (x + 60, y + 4), (x + 110, y + 8)]:
            draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=WHITE)
        draw.ellipse([x + w - 40, y + 3, x + w - 12, y + h - 3],
                     fill=(170, 165, 155))
        draw.ellipse([x + w - 32, y + 7, x + w - 26, y + 13], fill=(120, 115, 108))
        draw.ellipse([x + w - 24, y + 16, x + w - 18, y + 22], fill=(120, 115, 108))
        draw.polygon([(x + 20, y + 16), (x + 34, y + 12), (x + 34, y + 20)],
                     fill=(255, 210, 90))
        draw.text((x + 44, y + 8), "6BN MILES", font=font(BOLD, 10),
                  fill=WHITE)
    elif kind == "flags":
        draw.rectangle([x, y, x + w // 2, y + h], fill=(0, 51, 153))
        for k in range(5):
            import math
            ang = math.pi * 2 * k / 5 - math.pi / 2
            sx = x + w // 4 + int(9 * math.cos(ang))
            sy = y + h // 2 + int(9 * math.sin(ang))
            draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 215, 0))
        draw.rectangle([x + w // 2, y, x + w, y + h], fill=WHITE)
        draw.rectangle([x + w // 2, y + h // 2 - 3, x + w, y + h // 2 + 3],
                       fill=(200, 16, 46))
        draw.rectangle([x + w * 3 // 4 - 3, y, x + w * 3 // 4 + 3, y + h],
                       fill=(200, 16, 46))
    elif kind == "cpi":
        draw.rectangle([x, y, x + w, y + h], fill=(232, 226, 208))
        bars = [(x + 16, 8, (120, 118, 110)), (x + 46, 5, (120, 118, 110)),
                (x + 76, 2, RED)]
        for bx, bh, col in bars:
            draw.rectangle([bx, y + h - 4 - bh, bx + 22, y + h - 4], fill=col)
        draw.text((x + w - 8, y + 3), "2.3%", font=font(BOLD, 14),
                  fill=RED, anchor="ra")
        draw.text((x + w - 8, y + 18), "OCT CPI", font=font(BOLD, 7),
                  fill=GRAY, anchor="ra")
    elif kind == "cricket":
        draw.rectangle([x, y, x + w, y + h], fill=(27, 94, 32))
        draw.polygon([(x + 30, y + 4), (x + 44, y + 4), (x + 38, y + h - 4),
                      (x + 24, y + h - 4)], fill=(222, 196, 150))
        draw.rectangle([x + 33, y + h - 10, x + 37, y + h - 2], fill=(120, 72, 20))
        draw.ellipse([x + 62, y + 6, x + 74, y + 18], fill=RED,
                     outline=WHITE, width=1)
        draw.text((x + w - 8, y + 4), "118", font=font(BOLD, 15),
                  fill=WHITE, anchor="ra")
        draw.text((x + w - 8, y + 19), "RECORD", font=font(BOLD, 7),
                  fill=(255, 220, 120), anchor="ra")
    elif kind == "pill":
        draw.rectangle([x, y, x + w, y + h], fill=(230, 242, 240))
        # capsule, two halves
        draw.rounded_rectangle([x + 18, y + 8, x + 74, y + h - 8], radius=8,
                               fill=RED)
        draw.rounded_rectangle([x + 46, y + 8, x + 74, y + h - 8], radius=8,
                               fill=WHITE, outline=(200, 200, 200), width=1)
        draw.text((x + w - 8, y + 3), "60.7%", font=font(BOLD, 14),
                  fill=TEAL, anchor="ra")
        draw.text((x + w - 8, y + 18), "RESPONSE", font=font(BOLD, 7),
                  fill=GRAY, anchor="ra")
    elif kind == "cop31":
        draw.rectangle([x, y, x + w, y + h], fill=(15, 118, 110))
        draw.ellipse([x + 12, y + 4, x + 36, y + h - 4], fill=(178, 216, 230),
                     outline=WHITE, width=1)
        draw.rectangle([x + 52, y + 5, x + 58, y + h - 10], fill=WHITE)
        draw.ellipse([x + 48, y + h - 12, x + 62, y + h - 2], fill=RED)
        draw.text((x + w - 8, y + 4), "FINAL DAY", font=font(BOLD, 11),
                  fill=WHITE, anchor="ra")
        draw.text((x + w - 8, y + 18), "DEADLOCK", font=font(BOLD, 7),
                  fill=(255, 220, 120), anchor="ra")
    elif kind == "italy":
        draw.rectangle([x, y, x + w // 3, y + h], fill=(0, 140, 69))
        draw.rectangle([x + w // 3, y, x + 2 * w // 3, y + h], fill=WHITE)
        draw.rectangle([x + 2 * w // 3, y, x + w, y + h], fill=(205, 33, 42))
        draw.rectangle([x + w // 2 - 42, y + h - 13, x + w // 2 + 42, y + h - 2],
                       fill=DARK)
        draw.text((x + w // 2, y + h - 13), "SCIOPERO", font=font(BOLD, 8),
                  fill=WHITE, anchor="ma")
    elif kind == "blast":
        draw.rectangle([x, y, x + w, y + h], fill=(38, 34, 48))
        cx, cy = x + 34, y + h // 2
        pts = []
        import math
        for k in range(12):
            ang = math.pi * k / 6
            r = 11 if k % 2 == 0 else 5
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        draw.polygon(pts, fill=(255, 150, 40))
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 240, 180))
        draw.text((x + w - 8, y + 4), "7 AREAS", font=font(BOLD, 12),
                  fill=WHITE, anchor="ra")
        draw.text((x + w - 8, y + 18), "NARATHIWAT", font=font(BOLD, 7),
                  fill=(255, 200, 120), anchor="ra")


def draw_lead(draw, card, x, y, w, h):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CREAM,
                           outline=LIGHT, width=1)
    draw.rounded_rectangle([x, y, x + w, y + 26], radius=10, fill=card["color"])
    draw.rectangle([x, y + 16, x + w, y + 26], fill=card["color"])
    draw.text((x + 10, y + 7), card["kicker"], font=font(BOLD, 11), fill=WHITE)
    chip(draw, x + w - 78, y + 5, card["tag"], font(BOLD, 8))
    draw_art(draw, card["art"], x + 10, y + 34, w - 20, 76)
    # numbered kicker
    d2 = draw
    d2.text((x + 10, y + 116), card["num"] + "  \u00b7  " + card["topic"],
            font=font(BOLD, 10), fill=card["color"])
    f_head = font(BOLD, 19)
    hy = y + 132
    for line in card["head"].split("\n"):
        d2.text((x + 10, hy), line, font=f_head, fill=INK)
        hy += 22
    f_sub = font(REG, 11)
    lines = wrap(d2, card["sub"], f_sub, w - 20)
    sy = hy + 2
    for line in lines[:2]:
        d2.text((x + 10, sy), line, font=f_sub, fill=(64, 60, 52))
        sy += 13


def draw_feature(draw, feat, x, y, w, h):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=CREAM,
                           outline=LIGHT, width=1)
    draw_mini_art(draw, feat["art"], x + 5, y + 5, w - 10, 26)
    draw.text((x + 6, y + 35), feat["num"] + " \u00b7 " + feat["kicker"],
              font=font(BOLD, 8), fill=feat["color"])
    chip(draw, x + w - 60, y + 34, feat["tag"], font(BOLD, 7), h=13)
    f_head = font(BOLD, 11)
    hy = y + 49
    for line in feat["head"].split("\n"):
        draw.text((x + 6, hy), line, font=f_head, fill=INK)
        hy += 12
    f_sub = font(REG, 9)
    lines = wrap(draw, feat["sub"], f_sub, w - 12)
    sy = hy + 1
    for line in lines[:2]:
        draw.text((x + 6, sy), line, font=f_sub, fill=(64, 60, 52))
        sy += 10


def draw_map(draw, x, y, w, h):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=8,
                           fill=(223, 232, 234), outline=LIGHT, width=1)
    lon0, lon1, lat0, lat1 = -170, 190, 78, -56

    def proj(lon, lat):
        px = x + (lon - lon0) / (lon1 - lon0) * w
        py = y + (lat0 - lat) / (lat0 - lat1) * h
        return px, py

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=(154, 165, 120), outline=(107, 114, 86))
    f_pin = font(BOLD, 8)
    for num, lon, lat, dx, dy in MAP_PINS:
        px, py = proj(lon, lat)
        px += dx
        py += dy
        draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED,
                     outline=WHITE, width=2)
        draw.text((px, py - 1), num, font=f_pin, fill=WHITE, anchor="mm")
    # space story chip, bottom-left inside the map
    draw.rounded_rectangle([x + 8, y + h - 26, x + 108, y + h - 8], radius=6,
                           fill=DARK)
    draw.text((x + 58, y + h - 17), "SPACE \u00b7 06 MERCURY",
              font=font(BOLD, 8), fill=WHITE, anchor="mm")
    draw.text((x + w - 8, y + h - 17), "1\u20133 LEAD \u00b7 4\u201313 FEATURE",
              font=font(BOLD, 8), fill=INK, anchor="rm")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.text((MARGIN, 8), "THE WORLD IN ONE DAY", font=font(BOLD, 11), fill=RED)
    d.text((W - MARGIN, 8), "FRIDAY\u2019S NEWS  \u00b7  ONE PAGE",
           font=font(BOLD, 10), fill=GRAY, anchor="ra")
    d.text((MARGIN, 24), "Friday 20 November 2026", font=font(SERIF, 38),
           fill=INK)
    d.text((MARGIN, 66),
           "Cyclone Akvan makes landfall  \u00b7  Missiles hit Kyiv overnight  \u00b7  "
           "GTA VI sells 24.6m in a day  \u00b7  Asia\u2019s worst week since 2020",
           font=font(REG, 12), fill=GRAY)
    d.text((W - MARGIN, 66), "36 STORIES  \u00b7  7 REGIONS",
           font=font(BOLD, 12), fill=INK, anchor="ra")
    d.line([(MARGIN, 86), (W - MARGIN, 86)], fill=INK, width=2)
    d.line([(MARGIN, 89), (W - MARGIN, 89)], fill=INK, width=1)

    # ---- stat strip
    cell_w = (W - 2 * MARGIN) / len(STATS)
    for i, (num, label) in enumerate(STATS):
        cx = MARGIN + cell_w * i
        d.text((cx + cell_w / 2, 94), num, font=font(BOLD, 21), fill=RED,
               anchor="ma")
        lines = wrap(d, label, font(REG, 9), cell_w - 12)
        ly = 118
        for line in lines[:2]:
            d.text((cx + cell_w / 2, ly), line, font=font(REG, 9),
                   fill=GRAY, anchor="ma")
            ly += 11
        if i:
            d.line([(cx, 96), (cx, 134)], fill=LIGHT, width=1)

    # ---- region counts
    rx = MARGIN
    f_reg = font(BOLD, 9)
    for label, count, color in REGIONS:
        txt = label + " " + str(count)
        tw = d.textlength(txt, font=f_reg)
        d.rounded_rectangle([rx, 140, rx + tw + 12, 155], radius=7, fill=color)
        d.text((rx + 6, 142), txt, font=f_reg, fill=WHITE)
        rx += tw + 12 + 6
    d.text((W - MARGIN, 141), "ALL STORIES: FRI 20 NOV 2026, ANY TIME ZONE",
           font=font(BOLD, 9), fill=GRAY, anchor="ra")

    # ---- three lead cards
    cw, gap = 328, 8
    for i, card in enumerate(LEADS):
        draw_lead(d, card, MARGIN + i * (cw + gap), 162, cw, 204)

    # ---- ten feature cards, two rows of five
    fw = 193
    fgap = 6
    for i, feat in enumerate(FEATURES):
        row, col = divmod(i, 5)
        fx = MARGIN + col * (fw + fgap)
        fy = 372 + row * (95 + fgap)
        draw_feature(d, feat, fx, fy, fw, 95)

    # ---- bottom section headers
    d.text((MARGIN, 574), "WHERE IT HAPPENED", font=font(BOLD, 13), fill=INK)
    d.text((MARGIN + 176, 576), "Pins 1\u201313 (Lead & Feature)",
           font=font(REG, 10), fill=GRAY)
    d.text((328, 574), "ALSO ON FRIDAY 20 NOVEMBER \u2014 23 MORE STORIES",
           font=font(BOLD, 13), fill=INK)
    d.text((W - MARGIN, 576), "World Briefs (14\u201336)",
           font=font(REG, 10), fill=GRAY, anchor="ra")

    # ---- world map
    draw_map(d, MARGIN, 592, 300, 324)

    # ---- tail list, two columns
    f_num = font(BOLD, 10)
    f_place = font(BOLD, 10)
    f_head = font(REG, 10)
    f_src = font(REG, 9)
    col_x = [328, 664]
    col_w = [326, 344]
    for i, (num, place, head, src, tag) in enumerate(TAIL):
        col = 0 if i < 12 else 1
        row = i if i < 12 else i - 12
        x = col_x[col]
        y = 592 + row * 27
        num_color = RED if tag == "REPORTED" else (
            PURPLE if tag == "FORECAST" else AMBER)
        d.text((x, y), num, font=f_num, fill=num_color)
        px = x + 24
        d.text((px, y), place, font=f_place, fill=INK)
        px += d.textlength(place, font=f_place) + 6
        d.text((px, y), head, font=f_head, fill=INK)
        px += d.textlength(head, font=f_head) + 4
        d.text((px, y), "(" + src + ")", font=f_src, fill=GRAY)

    # ---- date check strip
    d.rounded_rectangle([MARGIN, 922, W - MARGIN, 976], radius=8, fill=DARK)
    d.text((MARGIN + 12, 930), "\u2715  DATE CHECK \u2014 NOT 20 NOV, EXCLUDED:",
           font=font(BOLD, 12), fill=WHITE)
    f_exc = font(REG, 10)
    lines = wrap(d, EXCLUDED, f_exc, W - 2 * MARGIN - 24)
    ey = 948
    for line in lines[:2]:
        d.text((MARGIN + 12, ey), line, font=f_exc, fill=(210, 205, 195))
        ey += 14

    # ---- footer
    d.text((W // 2, 984),
           "Tail numbers: red = REPORTED  \u00b7  purple = FORECAST  \u00b7  "
           "amber = CLAIM. Every story here happened, or was first reported, "
           "on Friday 20 November 2026 in at least one time zone.",
           font=font(REG, 9), fill=GRAY, anchor="ma")
    d.text((W // 2, 998),
           "Sources: Reuters, AP, AFP, BBC, IMD, The Hindu, EORTC, Sensor Tower, "
           "NST, Le Monde. Original vector drawings \u2014 no photos.",
           font=font(REG, 9), fill=GRAY, anchor="ma")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
