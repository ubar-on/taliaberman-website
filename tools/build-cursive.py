"""Regenerate the cursive artwork in images/cursive/.

Live Wix sets its cursive text in two commercial Masterfont faces we can't
self-host -- Gulash MF (Wix name: gulash-w26-regular) for the hero verses and
poem, Adler (adler-w26-regular) for the testimonial quotes. Substituting other
script fonts never matched, and left the sizing unresolvable. Instead we extract
the real glyph outlines and ship them as SVG paths.

Both fonts are downloaded from Wix's CDN at build time and are deliberately NOT
committed.

Single-line items: the SVG's box is the text's *advance* box (width = shaped
advance, height = OS/2 usWinAscent+usWinDescent), so it drops into exactly the
rectangle Chrome gave the original text run. That is what makes the CSS offsets
in style.css line up with positions measured on live.

Wrapped blocks (testimonials): lines are wrapped greedily at WRAP_PX using the
shaped advances, then stacked at LINE_STEP and centred, reproducing live's
layout. The wrap is asserted against the line breaks measured on live. Slides
that live styles differently carry their own size/wrap/step, and may pin their
line breaks outright, via OVERRIDES.

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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "images", "cursive")
WORK = os.path.join(ROOT, ".cursive-build")

CDN = "https://static.parastorage.com/fonts/v2"
GULASH = (f"{CDN}/3f40e55e-2058-46b3-b644-b5861701dd6c/v1/gulash-w26-regular", "gulash")
ADLER = (f"{CDN}/b08d1c5b-42ed-44e4-8ba4-4197d1906235/v1/adler-w26-regular", "adler")
# hebrew carries the letters, latin the punctuation (comma, period, quote, parens, digits)
SUBSETS = ("hebrew", "latin")

BLACK, BROWN, CREAM, TAUPE = "#000000", "#39251C", "#FFF8F1", "#5B4D43"

# slug, text, font-size, colour -- all measured on taliaberman.com at 1440x900
LINES = [
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

# Testimonials, in DOM order -- live carries all five in a rotating carousel.
QUOTE_SIZE = 50
WRAP_PX = 776.8      # live's blockquote text column
LINE_STEP = 68.6     # live's rendered line spacing at 50px (its block strut, not the font's normal)

# Live gives its longest testimonial its own treatment: 45px in a 926px column,
# which is how it fits three lines instead of four. Live also splits it across two
# paragraphs, so a single greedy wrap cannot reproduce the breaks -- they are taken
# verbatim from live (measured at 1440x900), as are the size and the 61.3px step.
OVERRIDES = {
    "testimonial-5": dict(
        size=45, wrap=923.9, step=61.3,
        lines=[
            '"הגעתי אלייך אחרי משבר בזוגיות, מצאתי את עצמי יושבת ובוכה, עם כאב פנימי',
            "ובלבול גדול. הושטת לי יד ומשכת אותי למעלה, מכל מפגש יצאתי חזקה יותר ומלאת תקווה.",
            'תודה לך טליה אהובה, אין לי ספק שזאת המתנה הכי טובה שיכלתי לתת לעצמי לגיל 38"',
        ],
    ),
}
TESTIMONIALS = [
    ("testimonial-1", "\"זכינו להכיר אישה מיוחדת,חזקה ומלאת אמונה,עם יכולת נדירה לגעת בכאב, ייאוש לא קיים אצלך בלקסיקון, לוחמת של אהבה ואמת שפיה וליבה שווים\""),
    ("testimonial-2", "\"תודה על אוזן קשבת, למדתי איתך וממך הרבה על עצמי, אני מאוד מעריכה אותך על האמת הפשוטה והכנות שבך\""),
    ("testimonial-3", "\"טליה השיחות שלנו תמיד עושות רק טוב, אני רוצה להגיד תודה על התמיכה הרגשית והרוחנית, על הדרך שעברתי , בשבילי זה היה בום (כמו שהילי אומרת)\""),
    ("testimonial-4", "\"בהמלצת חבר הגעתי סקפטי לגמרי, לא היה פשוט עבורי להיפתח אבל הופתעתי מהאמון שנתתי בך, תודה על הסבלנות.\""),
    ("testimonial-5", "\"הגעתי אלייך אחרי משבר בזוגיות, מצאתי את עצמי יושבת ובוכה, עם כאב פנימי ובלבול גדול. הושטת לי יד ומשכת אותי למעלה, מכל מפגש יצאתי חזקה יותר ומלאת תקווה. תודה לך טליה אהובה, אין לי ספק שזאת המתנה הכי טובה שיכלתי לתת לעצמי לגיל 38\""),
]

# The one quote live also shows: its wrap must reproduce live's measured breaks.
LIVE_WRAP = [
    "\"זכינו להכיר אישה מיוחדת,חזקה ומלאת אמונה,עם יכולת נדירה לגעת",
    "בכאב, ייאוש לא קיים אצלך בלקסיקון, לוחמת של אהבה ואמת שפיה",
    "וליבה שווים\"",
]


class Face:
    """A merged Wix webfont subset set, ready to shape and draw."""

    def __init__(self, base_url, name):
        os.makedirs(WORK, exist_ok=True)
        parts = []
        for sub in SUBSETS:
            raw = os.path.join(WORK, f"{name}-{sub}.woff2")
            if not os.path.exists(raw):
                urllib.request.urlretrieve(f"{base_url}.{sub}.woff2", raw)
            ttf = os.path.join(WORK, f"{name}-{sub}.ttf")
            f = TTFont(raw)
            f.flavor = None
            f.save(ttf)
            parts.append(ttf)
        path = os.path.join(WORK, f"{name}-merged.ttf")
        Merger().merge(parts).save(path)

        self.tt = TTFont(path)
        self.gs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()
        self.upem = self.tt["head"].unitsPerEm
        self.asc = self.tt["OS/2"].usWinAscent
        self.desc = self.tt["OS/2"].usWinDescent
        with open(path, "rb") as fh:
            self.hb = hb.Font(hb.Face(fh.read()))

    def shape(self, text):
        """-> (path_commands, advance_units)"""
        buf = hb.Buffer()
        buf.add_str(text)
        buf.direction, buf.script, buf.language = "rtl", "Hebr", "he"
        hb.shape(self.hb, buf, {"kern": True, "liga": True, "mark": True, "mkmk": True})
        pen = SVGPathPen(self.gs, ntos=lambda v: str(int(round(v))))
        x = y = 0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            self.gs[self.order[info.codepoint]].draw(
                TransformPen(pen, Offset(x + pos.x_offset, y + pos.y_offset)))
            x += pos.x_advance
            y += pos.y_advance
        return pen.getCommands(), x

    def advance_px(self, text, size):
        return self.shape(text)[1] * size / self.upem

    def wrap(self, text, size, max_px):
        """Greedy word wrap on shaped advances -- the same rule the browser applies."""
        lines, cur = [], ""
        for word in text.split(" "):
            trial = word if not cur else cur + " " + word
            if cur and self.advance_px(trial, size) > max_px:
                lines.append(cur)
                cur = word
            else:
                cur = trial
        if cur:
            lines.append(cur)
        return lines


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")


def svg_line(face, text, size, colour):
    d, adv = face.shape(text)
    scale = size / face.upem
    box_h = face.asc + face.desc
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {adv} {box_h}" '
            f'width="{adv * scale:.2f}" height="{box_h * scale:.2f}" overflow="visible" '
            f'role="img" aria-label="{esc(text)}">'
            f'<path fill="{colour}" transform="translate(0,{face.asc}) scale(1,-1)" '
            f'd="{d}"/></svg>'), adv * scale


def svg_block(face, text, size, colour, wrap_px, step_px, lines=None):
    """Centred, wrapped block -- reproduces live's testimonial layout.
    `lines` overrides the greedy wrap when live's own breaks are known."""
    lines = lines or face.wrap(text, size, wrap_px)
    scale = size / face.upem
    content_h = (face.asc + face.desc) * scale
    h_px = (len(lines) - 1) * step_px + content_h
    paths = []
    for i, line in enumerate(lines):
        d, adv = face.shape(line)
        x_px = (wrap_px - adv * scale) / 2
        baseline_px = i * step_px + face.asc * scale
        paths.append(f'<path fill="{colour}" '
                     f'transform="translate({x_px / scale:.0f},{baseline_px / scale:.0f}) scale(1,-1)" '
                     f'd="{d}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {wrap_px / scale:.0f} {h_px / scale:.0f}" '
            f'width="{wrap_px:.2f}" height="{h_px:.2f}" '
            f'role="img" aria-label="{esc(text)}">{"".join(paths)}</svg>'), lines


def main():
    os.makedirs(OUT, exist_ok=True)
    gulash = Face(*GULASH)
    print("Gulash single lines:")
    for slug, text, size, colour in LINES:
        svg, w_px = svg_line(gulash, text, size, colour)
        want = EXPECTED[slug]
        assert abs(w_px - want) < 0.5, f"{slug}: live {want}px vs shaped {w_px:.2f}px"
        with open(os.path.join(OUT, slug + ".svg"), "w", encoding="utf-8") as fh:
            fh.write(svg)
        print(f"  {slug:20} {size:>3}px  {w_px:>7.2f}px wide  (live {want})")

    adler = Face(*ADLER)
    print("\nAdler testimonial blocks:")
    for slug, text in TESTIMONIALS:
        o = OVERRIDES.get(slug, {})
        size, wrap = o.get("size", QUOTE_SIZE), o.get("wrap", WRAP_PX)
        step, forced = o.get("step", LINE_STEP), o.get("lines")
        if forced:
            assert " ".join(forced) == text, f"{slug}: forced lines do not rejoin to the source text"
        svg, lines = svg_block(adler, text, size, TAUPE, wrap, step, forced)
        if slug == "testimonial-1":
            assert lines == LIVE_WRAP, f"wrap drifted from live:\n{lines}\n{LIVE_WRAP}"
        with open(os.path.join(OUT, slug + ".svg"), "w", encoding="utf-8") as fh:
            fh.write(svg)
        h = (len(lines) - 1) * step + (adler.asc + adler.desc) * size / adler.upem
        print(f"  {slug:20} {size}px  {len(lines)} lines  {h:6.1f}px tall")

    n = len(LINES) + len(TESTIMONIALS)
    print(f"\n{n} files written to images/cursive/; widths and live's wrap both verified.")


if __name__ == "__main__":
    main()
