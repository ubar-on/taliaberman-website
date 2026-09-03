"""Regenerate the cursive SVGs in images/cursive/.

Live Wix sets these lines in Gulash MF (Wix name: gulash-w26-regular), a commercial
Masterfont face we can't self-host. Instead of substituting another script font --
which never matched, and left the size question unresolvable -- we extract the real
glyph outlines and ship them as SVG paths.

The font is downloaded from Wix's CDN at build time and is deliberately NOT committed.

Each SVG's box is the text's *advance* box (width = shaped advance, height =
OS/2 usWinAscent+usWinDescent), so it drops into exactly the rectangle Chrome gave
the original text run. That is what makes the CSS offsets in style.css line up with
positions measured on live.

Usage:  pip install uharfbuzz fonttools brotli  &&  python tools/build-cursive.py
"""
import os
import urllib.request

import uharfbuzz as hb
from fontTools.merge import Merger
from fontTools.misc.transform import Offset
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

CDN = ("https://static.parastorage.com/fonts/v2/"
       "3f40e55e-2058-46b3-b644-b5861701dd6c/v1/gulash-w26-regular")
# hebrew carries the letters, latin the comma/period/slash the poem and closing lines use
SUBSETS = ("hebrew", "latin")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "images", "cursive")

BLACK, BROWN, CREAM = "#000000", "#39251C", "#FFF8F1"

# slug, text, font-size, colour -- all measured on taliaberman.com at 1440x900
ITEMS = [
    ("poem-1",             "בהגיעי תפתח הדלת",                                65, CREAM),
    ("poem-2",             "אל היד המושטת",                                   65, CREAM),
    ("poem-3",             "אל חום לבבך",                                     65, CREAM),
    ("poem-4",             "אל שמחת משכנך",                                   65, CREAM),
    ("coaching-verse",     "כַּמַּיִם הַפָּנִים לַפָּנִים כֵּן לֵב הָאָדָם לָאָדָם",              70, BLACK),
    ("coaching-closing",   "תאמינו, אם אפשר לקלקל אפשר גם לתקן.",             60, BROWN),
    ("counseling-verse",   "יש לך כנפי רוח",                                  70, BLACK),
    ("counseling-closing", "אין מי שיחליף אותי במסע חיי",                     65, BROWN),
    ("singles-verse",      "ביקשתי את שאהבה נפשי",                            90, BLACK),
    ("singles-closing",    "אני לא לבד בעולם, הכל בסדר איתי, אני אהוב/ה בדיוק כמו שאני.", 60, BROWN),
]

# Rendered widths measured on live; the shaped advance must reproduce them.
EXPECTED = {"poem-1": 186.4, "poem-2": 152.8, "poem-3": 138.5, "poem-4": 166.3,
            "coaching-verse": 443.7, "coaching-closing": 376.3,
            "counseling-verse": 159.7, "counseling-closing": 285.4,
            "singles-verse": 333.1, "singles-closing": 610.0}


def build_font(workdir):
    """Download both subsets and merge them into one shapeable font."""
    parts = []
    for name in SUBSETS:
        raw = os.path.join(workdir, name + ".woff2")
        if not os.path.exists(raw):
            urllib.request.urlretrieve(f"{CDN}.{name}.woff2", raw)
        ttf = os.path.join(workdir, name + ".ttf")
        f = TTFont(raw)
        f.flavor = None
        f.save(ttf)
        parts.append(ttf)
    merged = os.path.join(workdir, "gulash-merged.ttf")
    Merger().merge(parts).save(merged)
    return merged


def main():
    workdir = os.path.join(ROOT, ".cursive-build")
    os.makedirs(workdir, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    path = build_font(workdir)

    tt = TTFont(path)
    gs, order = tt.getGlyphSet(), tt.getGlyphOrder()
    upem = tt["head"].unitsPerEm
    asc, desc = tt["OS/2"].usWinAscent, tt["OS/2"].usWinDescent
    with open(path, "rb") as fh:
        hbfont = hb.Font(hb.Face(fh.read()))

    for slug, text, size, colour in ITEMS:
        buf = hb.Buffer()
        buf.add_str(text)
        buf.direction, buf.script, buf.language = "rtl", "Hebr", "he"
        hb.shape(hbfont, buf, {"kern": True, "liga": True, "mark": True, "mkmk": True})

        pen = SVGPathPen(gs, ntos=lambda v: str(int(round(v))))
        x = y = 0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            gs[order[info.codepoint]].draw(
                TransformPen(pen, Offset(x + pos.x_offset, y + pos.y_offset)))
            x += pos.x_advance
            y += pos.y_advance

        scale = size / upem
        w_px, h_px = x * scale, (asc + desc) * scale
        want = EXPECTED[slug]
        assert abs(w_px - want) < 0.5, f"{slug}: live {want}px vs shaped {w_px:.2f}px"

        esc = text.replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {x} {asc + desc}" '
               f'width="{w_px:.2f}" height="{h_px:.2f}" overflow="visible" '
               f'role="img" aria-label="{esc}">'
               f'<path fill="{colour}" transform="translate(0,{asc}) scale(1,-1)" '
               f'd="{pen.getCommands()}"/></svg>')
        with open(os.path.join(OUT, slug + ".svg"), "w", encoding="utf-8") as fh:
            fh.write(svg)
        print(f"  {slug:20} {size:>3}px  {w_px:>7.2f}px wide  (live {want})")

    print(f"\n{len(ITEMS)} files written to images/cursive/; all widths match live.")


if __name__ == "__main__":
    main()
