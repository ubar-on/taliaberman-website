# taliaberman.com — Lift-and-Shift Design Spec

**Date:** 2026-06-25  
**Goal:** Migrate taliaberman.com from Wix to a static site hosted on GitHub Pages, with zero redesign and zero content loss.

---

## 1. Scope

### Pages (10 total, from sitemap)

| Hebrew path | Page title |
|---|---|
| `/` | Home |
| `/אודות-הדרך/` | אודות הדרך (About the Path) |
| `/אודות/` | בנימה אישית (Personal Note / Bio) |
| `/מרווקות-לזוגיות/` | מרווקות לזוגיות (From Single to Couple) |
| `/אימון-זוגי/` | אימון זוגי (Couples Coaching) |
| `/ייעוץ-אישי-עין-הבדולח/` | ייעוץ ואימון אישי — עין הבדולח |
| `/מתח/` | מתח |
| `/אחיזה/` | אחיזה |
| `/יחסים/` | יחסים |
| `/עצמי/` | עצמי |

### Out of scope
- Wix member/community profile pages (`/taliaberman1/profile`, etc.) — Wix platform feature, no content to migrate
- Blog/post functionality — the "שווה קריאה" section on the home page has no live linked posts; the 4 landing pages (מתח, אחיזה, יחסים, עצמי) are migrated as static HTML
- Contact form — none exists on the current site

---

## 2. Technology Stack

- **Plain HTML + CSS** — one `.html` file per page, no build tools, no frameworks
- **GitHub Pages** — serves the repo root on the `main` branch; no CI/CD needed
- **Google Fonts (self-hosted)** — `Assistant` font downloaded as WOFF2 and committed to `/fonts/`; no external font requests at runtime

---

## 3. File & Folder Structure

```
taliaberman-website/
├── index.html
├── אודות-הדרך/
│   └── index.html
├── אודות/
│   └── index.html
├── מרווקות-לזוגיות/
│   └── index.html
├── אימון-זוגי/
│   └── index.html
├── ייעוץ-אישי-עין-הבדולח/
│   └── index.html
├── מתח/
│   └── index.html
├── אחיזה/
│   └── index.html
├── יחסים/
│   └── index.html
├── עצמי/
│   └── index.html
├── css/
│   └── style.css
├── fonts/
│   ├── Assistant-Regular.woff2
│   ├── Assistant-SemiBold.woff2
│   └── Assistant-Bold.woff2
├── images/
│   └── [all downloaded images — see Section 5]
├── CNAME
└── docs/
    └── superpowers/specs/
        └── 2026-06-25-lift-and-shift-design.md
```

Hebrew directory names preserve the existing Wix URLs exactly, avoiding SEO disruption at DNS cutover.

---

## 4. HTML Template

Every page uses this skeleton:

```html
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>[Page Title] | טליה ברמן</title>
  <meta name="description" content="[Page meta description]">
  <meta name="google-site-verification" content="wvSyn234b7e5W_VghEFBSNyeBVhaJnIsU5LGIBHM6LA">
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>
  <nav><!-- shared navigation --></nav>
  <main><!-- page-specific content --></main>
  <footer><!-- shared footer --></footer>
</body>
</html>
```

`lang="he"` and `dir="rtl"` are set at the `<html>` level to handle all Hebrew text layout globally.

The Google Search Console verification meta tag is preserved on every page to avoid ownership disruption.

---

## 5. Visual Design Tokens

Extracted from the live site:

| Token | Value |
|---|---|
| Background | `#FFF8F1` |
| Text | `#000000` |
| Accent / links | `#39251C` |
| Font family | `Assistant` (weights 400, 600, 700) |
| Border radius | `0px` |

Font loaded via `@font-face` in `style.css`:

```css
@font-face {
  font-family: 'Assistant';
  src: url('/fonts/Assistant-Regular.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}
/* repeated for weight 600 and 700 */
```

CSS is hand-written to match the Wix layout. Pixel-level spacing may vary slightly from the Wix output; structure, colors, font, and all content will be exact.

---

## 6. Image Migration

All images are downloaded from `static.wixstatic.com` and committed to `/images/`. No Wix CDN URLs remain in the finished site.

Images to migrate (identified from page scrapes):

| File | Source page | Wix asset ID |
|---|---|---|
| `logo.png` | All pages (nav) | `a99131_16a547c833124b43a42601421ebe2464~mv2.png` |
| `hero-banner.jpg` | Home | `a99131_cbab58c1e37f4a34b8312a1fee5f6fbb~mv2.jpg` |
| `profile-photo.jpg` | Home, Bio | `a99131_2a2d2034f5734b5bbd8ef060ffebd13c~mv2.jpg` |
| `sunset-singles.jpg` | מרווקות לזוגיות | `a99131_dbc21f735307423ebc7666a4a0513b78~mv2.jpg` |
| `couples-hero.jpg` | אימון זוגי | `11062b_95d34f15761e4114a57b17823228948ef000.jpg` |
| `feather-counseling.jpg` | ייעוץ אישי | `a99131_e277ef345f914f4b882746af993cfbcf~mv2.jpg` |

Additional images (strip image, decorative) will be collected during implementation by scraping the full HTML source of each page.

---

## 7. GitHub Pages & Custom Domain

- Pages enabled on `main` branch, serving from the repo root
- `CNAME` file at repo root contains: `taliaberman.com`
- DNS cutover (at registrar): point `taliaberman.com` and `www.taliaberman.com` to GitHub Pages IPs (`185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`)
- DNS cutover is the final step, done only after the site is built and verified at the `github.io` preview URL — zero downtime risk

---

## 8. Navigation

The existing Wix navigation structure (extracted from page descriptions):

**אודות · בנימה אישית · ייעוץ ואימון · ייעוץ אישי - עין הבדולח · אימון זוגי · מרווקות לזוגיות · שווה קריאה**

The "שווה קריאה" nav item links to the 4 confirmed landing pages (מתח, אחיזה, יחסים, עצמי). Two labels visible on the home page (אל עצמי, רצון) have no corresponding pages in the sitemap and are not migrated. Navigation is duplicated in each HTML file (no templating engine).

---

## 9. What Is Not Replicated

- Wix animations and scroll effects — not replicated; static layout only
- Wix blog/members/comments infrastructure
- Wix SEO redirects — the URL structure is preserved so no redirects are needed
