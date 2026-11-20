#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news front page (1024x1024 PNG).

Deterministic: no network, no randomness, no timestamps in the image.
Only PIL + the standard library. 31 stories, all verified from live news
searches on 20 Nov 2026 (Reuters, AP, BBC, IMD/The Hindu, Sensor Tower,
Fast Company, New African / African Spectator, NDTV, IANS/JagranJosh).
Layout: masthead + lead + 2x2 main stories + dotted world map with
region notes + 21-item ticker.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (20, 33, 61)
RED = (180, 35, 24)
NAVY = (20, 33, 61)
GREY = (90, 90, 88)
LIGHT = (232, 226, 210)
GOLD = (255, 210, 90)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, color, max_w, leading):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y


def rule(draw, x, y, w, color=INK, width=2):
    draw.line([(x, y), (x + w, y)], fill=color, width=width)


def draw_city(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 170, 60))
    draw.ellipse([x + w // 2 - 12, y + 2, x + w // 2 + 12, y + 26], fill=(255, 220, 120))
    for bx, bh in ((x + 6, 18), (x + 52, 25), (x + 104, 15), (x + 150, 22),
                   (x + 200, 19), (x + 250, 26), (x + 300, 16), (x + 350, 23),
                   (x + 400, 18)):
        if bx + 30 <= x + w:
            draw.rectangle([bx, y + h - bh, bx + 30, y + h], fill=INK)
    draw.rectangle([x, y + h - 5, x + w, y + h], fill=(40, 120, 140))


def draw_chart(draw, x, y, w, h):
    bars = [8, 12, 10, 16, 22, 30]
    base = y + h - 5
    for i, v in enumerate(bars):
        draw.rectangle([x + 8 + i * 30, base - v, x + 8 + i * 30 + 22, base],
                       fill=RED if i == len(bars) - 1 else INK)
    draw.rectangle([x + w - 78, y + 2, x + w - 8, y + 30], outline=INK, width=3,
                   fill=(214, 228, 240))
    draw.text((x + w - 68, y + 7), "ANT", font=font(SANS_B, 15), fill=INK)


def draw_cyclone(draw, x, y, w, h):
    # spiral storm: concentric arcs + rain ticks
    cx, cy = x + 52, y + h // 2
    for r in (8, 16, 24):
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300,
                 fill=INK, width=3)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
    for rx in range(x + 110, x + w - 175, 22):
        draw.line([(rx, y + 8), (rx - 5, y + h - 10)], fill=(60, 90, 140), width=2)
    draw.text((x + w - 150, y + h - 22), "110 KM/H GUSTS",
              font=font(SANS_B, 14), fill=INK)


def draw_gate(draw, x, y, w, h):
    # EU flag band: blue field, ring of gold stars
    import math
    draw.rectangle([x, y, x + w, y + h], fill=(0, 51, 153))
    cx, cy = x + 60, y + h // 2
    for k in range(12):
        a = math.pi * 2 * k / 12 - math.pi / 2
        sx = cx + 15 * math.cos(a)
        sy = cy + 15 * math.sin(a)
        draw.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 204, 0))
    draw.text((x + 110, y + h // 2 - 10), "EUROPE AT THE TABLE",
              font=font(SANS_B, 16), fill=(255, 255, 255))


# Dotted world map: 44 cols x 18 rows, '#' = land. Rough equirectangular.
WORLD = [
    "....##########.................######..............",
    "..##############......##......##########............",
    "..###############....####...##############..........",
    "...#############......##....###############.........",
    "....###########.............##############..##......",
    ".....#########......##.......############...###......",
    "......#######......####.......##########....###......",
    ".......#####........##.........########.....##.......",
    "........###.........####........######...............",
    ".........##..........##.........#####.....##.........",
    ".........###.........####........####....####.........",
    "..........##..........##.........###.....#####........",
    "..........###.........###........##.......####........",
    "...........##..........#.........##........###........",
    "...........##...................#.........##.........",
    "............#.............................##........",
    "............##...........................###.........",
    ".............#..........................##..........",
]
# (col, row) of story cities on the 44x18 grid
CITIES = [(13, 5), (24, 3), (28, 7), (32, 8), (43, 16), (16, 13), (25, 14)]


def draw_world(draw, x, y, cell=5):
    for r, row in enumerate(WORLD):
        for c, ch in enumerate(row):
            if ch == '#':
                draw.ellipse([x + c * cell, y + r * cell,
                              x + c * cell + 3, y + r * cell + 3],
                             fill=(120, 140, 160))
    for (c, r) in CITIES:
        px, py = x + c * cell - 1, y + r * cell - 1
        draw.ellipse([px, py, px + 6, py + 6], fill=RED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36
    CW = W - 2 * M

    # ---- masthead ----
    f_top = font(SANS_B, 17)
    d.text((M, 22), "THE WORLD IN ONE DAY", font=f_top, fill=GREY)
    d.text((W - M - d.textlength("ONE DAY  •  ONE PAGE", font=f_top), 22),
           "ONE DAY  •  ONE PAGE", font=f_top, fill=GREY)
    rule(d, M, 48, CW, INK, 3)
    d.text((M, 56), "THE WORLD IN ONE DAY", font=font(SERIF_B, 60), fill=INK)
    d.text((M, 124), "FRIDAY, 20 NOVEMBER 2026", font=font(SANS_B, 33), fill=RED)
    tag = "WORLD CHILDREN'S DAY"
    d.text((W - M - d.textlength(tag, font=font(SANS_B, 18)), 132), tag,
           font=font(SANS_B, 18), fill=GREY)
    rule(d, M, 164, CW, RED, 4)
    rule(d, M, 170, CW, INK, 2)

    # ---- lead: Trump / Iran ----
    y = 186
    f_kick = font(SANS_B, 18)
    d.text((M, y), "LEAD  •  WASHINGTON — IRAN", font=f_kick, fill=RED)
    f_lead = font(SERIF_B, 34)
    y = para(d, M, y + 26, "Trump puts the Iran war decision off until 2027",
             f_lead, INK, 690, 38)
    f_body = font(SANS, 20)
    y = para(d, M, y + 6,
             "Back from Shenzhen, Trump tells Reuters, Fox News and Axios "
             "he is 'not rushing' on new Iran strikes: 'We'll see what "
             "happens after January 1.' Netanyahu presses for a new offensive.",
             f_body, INK, 690, 25)
    # panel: the date
    fx, fy = 760, 198
    d.rectangle([fx, fy, fx + 192, fy + 162], outline=INK, width=3, fill=(255, 255, 255))
    d.text((fx + 12, fy + 10), "TRUMP'S DATE", font=font(SANS_B, 14), fill=INK)
    d.text((fx + 12, fy + 32), "JAN 1", font=font(SERIF_B, 44), fill=RED)
    d.text((fx + 12, fy + 82), "2027", font=font(SERIF_B, 44), fill=INK)
    para(d, fx + 12, fy + 130, "No strikes before then.",
         font(SANS, 14), INK, 168, 17)

    rule(d, M, 378, CW, INK, 2)

    # ---- row 2: Cyclone Akvan | GTA VI ----
    col_w = (CW - 24) // 2
    y0 = 390
    f_h2 = font(SERIF_B, 26)
    x = M
    d.text((x, y0), "INDIA  •  WEATHER", font=f_kick, fill=RED)
    yy = para(d, x, y0 + 26, "Cyclone Akvan hits Odisha",
              f_h2, INK, col_w, 31)
    yy = para(d, x, yy + 4,
              "Akvan hits near Gopalpur at noon, gusts 110 km/h. 300,000 "
              "in shelters; 69 trains cancelled.",
              font(SANS, 18), INK, col_w, 23)
    draw_cyclone(d, x, 503, col_w, 44)
    x = M + col_w + 24
    d.text((x, y0), "CULTURE  •  GAMING", font=f_kick, fill=RED)
    yy2 = para(d, x, y0 + 26, "GTA VI: $2.36bn on day one",
               f_h2, INK, col_w, 31)
    yy2 = para(d, x, yy2 + 4,
               "Sensor Tower counts 24.6m copies, $2.36bn by Thursday night "
               "— the biggest launch ever.",
               font(SANS, 18), INK, col_w, 23)
    draw_city(d, x, 503, col_w, 44)

    rule(d, M, 560, CW, INK, 2)

    # ---- row 3: Anthropic | Berlin ----
    y0 = 572
    x = M
    d.text((x, y0), "BUSINESS  •  AI", font=f_kick, fill=RED)
    yy = para(d, x, y0 + 26, "Anthropic up 17% at $97.17",
              f_h2, INK, col_w, 31)
    yy = para(d, x, yy + 4,
              "ANT opens $111.50, briefly tops $2tn, closes $97.17, up 17%. "
              "Wall St falls 2%+.",
              font(SANS, 18), INK, col_w, 23)
    draw_chart(d, x, 685, col_w, 44)
    x = M + col_w + 24
    d.text((x, y0), "EUROPE  •  BERLIN", font=f_kick, fill=RED)
    yy2 = para(d, x, y0 + 26, "Europe ready for Russia talks",
               f_h2, INK, col_w, 31)
    yy2 = para(d, x, yy2 + 4,
               "Allies will talk if Kyiv accepts. Kushner: Moscow "
               "'comfortable' with Article 5-style guarantees.",
               font(SANS, 18), INK, col_w, 23)
    draw_gate(d, x, 685, col_w, 44)

    # ---- world map strip ----
    my = 742
    d.text((M, my), "AROUND THE WORLD", font=font(SANS_B, 15), fill=INK)
    draw_world(d, M, my + 20)
    notes = [
        ("N. AMERICA", "Trump pardons baseball's hit king Pete Rose"),
        ("S. AMERICA", "42% of Brazilians see fraud in 2026 vote"),
        ("AFRICA", "South Sudan postpones first vote to Feb 2027"),
        ("ASIA", "Justice Varma resigns: 'not admission of guilt'"),
        ("OCEANIA", "Nicholls 113* rescues NZ; Kiwis 243-5 vs India"),
    ]
    nx = [276, 640]
    ny = [my + 20, my + 50, my + 80]
    for i, (region, text) in enumerate(notes):
        col = i % 2
        row = i // 2
        xx, yy = nx[col], ny[row]
        d.text((xx, yy), region, font=font(SANS_B, 13), fill=RED)
        para(d, xx, yy + 15, text, font(SANS, 14), INK, 330, 16)
    d.text((nx[1], ny[2] + 15), "Red dots mark today's stories.",
           font=font(SANS, 13), fill=GREY)

    # ---- ticker strip: 21 more stories, 3 cols x 7 rows ----
    ty = 866
    d.rectangle([M, ty, W - M, 1020], fill=NAVY)
    d.text((M + 14, ty + 8), "ALSO TODAY", font=font(SANS_B, 17), fill=GOLD)
    d.text((W - M - 14 - d.textlength("All stories as reported on 20 November 2026.",
                                     font=font(SANS, 13)), ty + 10),
           "All stories as reported on 20 November 2026.",
           font=font(SANS, 13), fill=(200, 200, 190))
    f_tick = font(SANS, 13)
    items = [
        u"\u2022  Citi misbooked trades; risk off by $35bn",
        u"\u2022  Goldy Brar tops Canada most-wanted list",
        u"\u2022  Musk: 'I'm not MAGA'; regrets $500m",
        u"\u2022  Chase cyberattack leaks customer emails",
        u"\u2022  Wall St falls 2%+ despite Anthropic debut",
        u"\u2022  Trump made 751 personal trades in Sept.",
        u"\u2022  Grindr launches $120/mo AI subscription",
        u"\u2022  New flying frog species found in Indonesia",
        u"\u2022  Irishman indicted over ax attack on US jet",
        u"\u2022  Rome rebukes Kyiv over blacklisted MPs",
        u"\u2022  APEC: Xi urges open trade, tech cooperation",
        u"\u2022  Modi opens FICCI centenary convention",
        u"\u2022  Women's Asian Hockey Trophy begins",
        u"\u2022  India beat Malaysia in Hong Kong badminton",
        u"\u2022  Sensex, Nifty post strong gains in Mumbai",
        u"\u2022  Goldman, Morgan Stanley net $113m each",
        u"\u2022  Libya seizes 4m+ drug pills, cocaine in raid",
        u"\u2022  Mozambique opposition leader goes on trial",
        u"\u2022  Nigerian troops protest unpaid ECOWAS pay",
        u"\u2022  Ethiopia, Eritrea build up forces on border",
        u"\u2022  Uganda charges missing opposition activist",
    ]
    cols_x = [M + 14, M + 332, M + 650]
    yy = ty + 32
    for r in range(7):
        for c in range(3):
            idx = r * 3 + c
            if idx < len(items):
                d.text((cols_x[c], yy), items[idx], font=f_tick, fill=PAPER)
        yy += 16

    img.save("entry.png", "PNG", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
