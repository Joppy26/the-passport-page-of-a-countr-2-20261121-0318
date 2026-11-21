#!/usr/bin/env python3
"""The Passport Page of a Country That Isn't There.

Draws one uncaptioned open passport spread for the Republic of Skerrya,
a cold-climate island republic that does not exist. Deterministic:
no network, no clock, no randomness. The same PNG bytes every run.

Run: python3 main.py   (writes entry.png to /output/entry.png,
or to $MAKEFUN_OUTPUT_DIR when that is set)
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
MONO = os.path.join(FONT_DIR, "DejaVuSansMono.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- country
COUNTRY = "REPUBLIC OF SKERRYA"
COUNTRY_NATIVE = "Lýðveldið Skerrya"
CAPITAL = "VEYHAVN"
HOLDER_SURNAME = "VEY"
HOLDER_GIVEN = "ELLA MAREN"
DOB = "14 MAR 1990"
POB = "VEYHAVN, SKERRYA"
SEX = "F"
ISSUE = "12 JAN 2021"
EXPIRY = "12 JAN 2031"
AUTHORITY = "HARBOUR OFFICE, VEYHAVN"
DOC_NO = "SKR 0842173"
DOC_NO_MRZ = "SKR084217"
NATIONALITY = "SKERRYAN"


# ---------------------------------------------------------------- MRZ
def mrz_check(text):
    """ICAO check digit: weights 7, 3, 1; A=10 .. Z=35, '<'=0."""
    weights = (7, 3, 1)
    total = 0
    for i, ch in enumerate(text):
        if ch == "<":
            value = 0
        elif ch.isdigit():
            value = int(ch)
        else:
            value = ord(ch) - ord("A") + 10
        total += value * weights[i % 3]
    return str(total % 10)


def mrz_lines():
    line1 = "P<SKR" + "VEY<<ELLA<MAREN"
    line1 = line1 + "<" * (44 - len(line1))
    dob = "900314"
    exp = "310112"
    personal = "<" * 14
    line2 = (
        DOC_NO_MRZ
        + mrz_check(DOC_NO_MRZ)
        + "SKR"
        + dob
        + mrz_check(dob)
        + SEX
        + exp
        + mrz_check(exp)
        + personal
        + mrz_check(personal)
    )
    line2 = line2 + "<" * (44 - len(line2))
    return line1, line2


# ---------------------------------------------------------------- helpers
def text(draw, xy, s, fnt, fill, anchor="la"):
    draw.text(xy, s, font=fnt, fill=fill, anchor=anchor)


def rule(draw, x0, y, x1, color, width=2):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def draw_stamp(base, cx, cy, w, h, lines, color, angle):
    """A rectangular ink stamp, slightly rotated, pasted onto base."""
    layer = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    ox, oy = 20, 20
    d.rounded_rectangle([ox, oy, ox + w, oy + h], radius=8,
                        outline=color, width=3)
    d.rounded_rectangle([ox + 5, oy + 5, ox + w - 5, oy + h - 5], radius=6,
                        outline=color, width=1)
    n = len(lines)
    for i, (s, fnt, gap) in enumerate(lines):
        y = oy + 12 + i * gap
        d.text((ox + w // 2, y), s, font=fnt, fill=color, anchor="ma")
    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=False)
    base.alpha_composite(layer, (cx - (w + 40) // 2, cy - (h + 40) // 2))


def draw_portrait(draw, box):
    """Stylised line-art portrait: a fisherwoman of Veyhavn."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(214, 226, 233), outline=(90, 110, 130), width=2)
    # shoulders / coat
    draw.polygon([(x0 + 18, y1 - 2), (x0 + 52, y1 - 62), (x0 + 108, y1 - 62),
                  (x0 + 142, y1 - 2)], fill=(52, 74, 102))
    draw.polygon([(x0 + 70, y1 - 60), (x0 + 80, y1 - 30), (x0 + 90, y1 - 60)],
                 fill=(244, 234, 210))
    # neck
    draw.rectangle([x0 + 70, y1 - 78, x0 + 90, y1 - 58], fill=(232, 195, 154))
    # head
    draw.ellipse([x0 + 48, y0 + 18, x0 + 112, y0 + 92], fill=(232, 195, 154),
                 outline=(120, 90, 60), width=2)
    # hair: dark sweep over the top of the head, tied back
    draw.pieslice([x0 + 44, y0 + 12, x0 + 116, y0 + 80], start=180, end=360,
                  fill=(74, 52, 38))
    draw.polygon([(x0 + 48, y0 + 44), (x0 + 58, y0 + 26), (x0 + 66, y0 + 46)],
                 fill=(74, 52, 38))
    draw.polygon([(x0 + 112, y0 + 44), (x0 + 102, y0 + 26), (x0 + 94, y0 + 46)],
                 fill=(74, 52, 38))
    # brows, eyes, nose, mouth
    draw.line([(x0 + 60, y0 + 52), (x0 + 72, y0 + 50)], fill=(74, 52, 38),
              width=2)
    draw.line([(x0 + 88, y0 + 50), (x0 + 100, y0 + 52)], fill=(74, 52, 38),
              width=2)
    draw.ellipse([x0 + 62, y0 + 55, x0 + 69, y0 + 60], fill=(40, 40, 40))
    draw.ellipse([x0 + 91, y0 + 55, x0 + 98, y0 + 60], fill=(40, 40, 40))
    draw.line([(x0 + 80, y0 + 58), (x0 + 78, y0 + 72), (x0 + 82, y0 + 73)],
              fill=(120, 90, 60), width=2)
    draw.arc([x0 + 70, y0 + 76, x0 + 90, y0 + 88], start=15, end=165,
             fill=(140, 70, 60), width=2)
    # faint guilloche corner marks on the photo
    draw.line([(x0 + 6, y0 + 6), (x0 + 20, y0 + 6)], fill=(90, 110, 130),
              width=1)
    draw.line([(x0 + 6, y0 + 6), (x0 + 6, y0 + 20)], fill=(90, 110, 130),
              width=1)


# ---------------------------------------------------------------- build
def build():
    img = Image.new("RGBA", (W, H), (31, 42, 58, 255))
    d = ImageDraw.Draw(img)

    # pages
    d.rectangle([36, 36, 500, 988], fill=(247, 240, 220, 255))
    d.rectangle([524, 36, 988, 988], fill=(247, 240, 220, 255))
    d.line([(512, 36), (512, 988)], fill=(12, 18, 28, 255), width=4)
    for x0, x1 in ((36, 500), (524, 988)):
        d.rectangle([x0, 36, x1, 988], outline=(150, 130, 90, 255), width=2)

    ink = (28, 38, 58, 255)
    faint = (110, 105, 85, 255)
    red = (150, 40, 35, 255)

    # ================================================= LEFT PAGE: data page
    f_title = font(SERIF_B, 25)
    f_sub = font(SERIF, 15)
    f_label = font(SANS_B, 11)
    f_value = font(SANS, 16)
    f_value_b = font(SANS_B, 16)
    f_mrz = font(MONO, 15)
    f_small = font(SANS, 11)

    # emblem: lighthouse in a circle
    cx, cy = 268, 92
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline=ink, width=2)
    d.polygon([(cx - 7, cy + 20), (cx - 4, cy - 12), (cx + 4, cy - 12),
               (cx + 7, cy + 20)], fill=ink)
    d.rectangle([cx - 8, cy - 18, cx + 8, cy - 10], fill=ink)
    d.line([(cx - 14, cy - 8), (cx - 26, cy - 16)], fill=ink, width=2)
    d.line([(cx + 14, cy - 8), (cx + 26, cy - 16)], fill=ink, width=2)
    d.line([(cx - 20, cy + 20), (cx + 20, cy + 20)], fill=ink, width=3)

    text(d, (268, 128), COUNTRY, f_title, ink, anchor="ma")
    text(d, (268, 160), COUNTRY_NATIVE + "  ·  PASSPORT", f_sub, ink,
         anchor="ma")
    rule(d, 60, 190, 476, ink, 2)

    # portrait, left; fields, right
    draw_portrait(d, (60, 210, 210, 360))
    text(d, (60, 366), "PHOTOGRAPH", f_label, faint, anchor="la")

    fields = [
        ("SURNAME / EFTERNAFN", HOLDER_SURNAME),
        ("GIVEN NAMES / FORNAFN", HOLDER_GIVEN),
        ("NATIONALITY / ÞJÓÐERNI", NATIONALITY),
        ("DATE OF BIRTH / FØÐINGARDAGUR", DOB),
        ("PLACE OF BIRTH / FØÐINGARSTAÐUR", POB),
        ("SEX / KYN", SEX),
        ("DATE OF ISSUE / ÚTGÁFUDAGUR", ISSUE),
        ("DATE OF EXPIRY / GILDISTÍMI", EXPIRY),
        ("AUTHORITY / ÚTGÁFUSTOÐ", AUTHORITY),
        ("PASSPORT No.", DOC_NO),
    ]
    y = 210
    for label, value in fields:
        text(d, (228, y), label, f_label, faint, anchor="la")
        text(d, (228, y + 15), value, f_value_b, ink, anchor="la")
        y += 40
    # signature line under the fields
    rule(d, 228, 610, 476, faint, 1)
    text(d, (228, 616), "HOLDER'S SIGNATURE / UNDIRSKRIFT", f_label, faint)

    # bilingual note
    text(d, (268, 660), "Entries in Skerryan and English.",
         font(SERIF, 14), ink, anchor="ma")
    text(d, (268, 682), "Allar færslur á skerrsku og ensku.",
         font(SERIF, 14), ink, anchor="ma")
    rule(d, 60, 712, 476, ink, 2)

    # machine-readable zone
    text(d, (60, 730), "MACHINE READABLE ZONE", f_label, faint)
    line1, line2 = mrz_lines()
    text(d, (60, 752), line1, f_mrz, ink)
    text(d, (60, 776), line2, f_mrz, ink)
    rule(d, 60, 812, 476, ink, 2)
    text(d, (268, 830),
         "This passport remains the property of the", f_small, faint,
         anchor="ma")
    text(d, (268, 848), "Republic of Skerrya.", f_small, faint, anchor="ma")
    text(d, (268, 884), "SKR 0842173", font(SANS_B, 13), ink, anchor="ma")
    text(d, (60, 950), "PAGE 2", f_label, faint)
    text(d, (476, 950), "2 / 32", f_label, faint, anchor="ra")

    # ============================================== RIGHT PAGE: visa pages
    f_page = font(SERIF_B, 22)
    f_stamp_big = font(SANS_B, 17)
    f_stamp = font(SANS_B, 14)
    f_stamp_sm = font(SANS_B, 12)
    f_cond = font(SANS, 14)
    f_cond_b = font(SANS_B, 14)

    text(d, (756, 64), "VISAS", f_page, ink, anchor="ma")
    text(d, (756, 94), "VEGABRÉF  ·  ENDORSEMENTS", f_sub, ink, anchor="ma")
    rule(d, 548, 126, 964, ink, 2)

    stamp_color = (38, 90, 60, 255)      # green ink
    stamp_color2 = (90, 50, 110, 255)    # violet ink
    stamp_color3 = (30, 70, 120, 255)    # blue ink

    # Trip 1: Nordmark, June 2022 (entry + exit)
    draw_stamp(img, 660, 230, 200, 92, [
        ("NORDMARK", f_stamp_big, 30),
        ("ENTRY  ·  HAVNOSTAD", f_stamp_sm, 22),
        ("03 JUN 2022", f_stamp, 24),
    ], stamp_color, -5)
    draw_stamp(img, 872, 230, 200, 92, [
        ("NORDMARK", f_stamp_big, 30),
        ("EXIT  ·  HAVNOSTAD", f_stamp_sm, 22),
        ("17 JUN 2022", f_stamp, 24),
    ], stamp_color, 4)

    # Trip 2: Tarn Isles, September 2023 (entry + exit)
    draw_stamp(img, 660, 360, 200, 92, [
        ("TARN ISLES", f_stamp_big, 30),
        ("ENTRY  ·  PORT TARN", f_stamp_sm, 22),
        ("09 SEP 2023", f_stamp, 24),
    ], stamp_color2, 3)
    draw_stamp(img, 872, 360, 200, 92, [
        ("TARN ISLES", f_stamp_big, 30),
        ("EXIT  ·  PORT TARN", f_stamp_sm, 22),
        ("24 SEP 2023", f_stamp, 24),
    ], stamp_color2, -4)

    # Trip 3: Nordmark again, May 2024 (entry + exit)
    draw_stamp(img, 660, 490, 200, 92, [
        ("NORDMARK", f_stamp_big, 30),
        ("ENTRY  ·  HAVNOSTAD", f_stamp_sm, 22),
        ("21 MAY 2024", f_stamp, 24),
    ], stamp_color3, -3)
    draw_stamp(img, 872, 490, 200, 92, [
        ("NORDMARK", f_stamp_big, 30),
        ("EXIT  ·  HAVNOSTAD", f_stamp_sm, 22),
        ("02 JUN 2024", f_stamp, 24),
    ], stamp_color3, 5)

    # Telling detail: Condition 7 — the fishing-boat work rule
    d.rectangle([548, 580, 964, 760], outline=red, width=2)
    text(d, (756, 596), "CONDITION 7", f_cond_b, red, anchor="ma")
    rule(d, 568, 622, 944, red, 1)
    cond_lines = [
        "Holder may not take paid work aboard",
        "fishing vessels without a permit from",
        "the Harbour Master of Veyhavn.",
        "Permits are issued only in the",
        "daylight months, April to September.",
    ]
    y = 634
    for s in cond_lines:
        text(d, (756, y), s, f_cond, ink, anchor="ma")
        y += 22

    # Harbour tax fee stamp, overlapping the condition box corner
    draw_stamp(img, 872, 812, 220, 76, [
        ("HARBOUR TAX", f_stamp, 26),
        ("40 KR  ·  PAID", f_stamp_big, 26),
        ("VEYHAVN  ·  12 JAN 2021", f_stamp_sm, 22),
    ], red, -6)

    text(d, (548, 900),
         "Ferry passage to the mainland is not a visa.",
         font(SERIF, 14), faint, anchor="la")
    text(d, (548, 924),
         "Ferjuflutningur til meginlandsins er ekki vegabréfsáritun.",
         font(SERIF, 13), faint, anchor="la")
    text(d, (548, 950), "PAGES 3–4", f_label, faint)
    text(d, (964, 950), "4 / 32", f_label, faint, anchor="ra")

    return img.convert("RGB")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        print("cannot create output dir: %s" % exc, file=sys.stderr)
        return 1
    img = build()
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG")
    return 0


if __name__ == "__main__":
    sys.exit(main())
