# taliaberman.com Lift-and-Shift Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate taliaberman.com from Wix to a fully self-contained static site on GitHub Pages, with zero content loss and faithful visual reproduction.

**Architecture:** 10 plain HTML files (one per page), a single shared `style.css`, self-hosted fonts in `/fonts/`, and all images downloaded from Wix CDN into `/images/`. No build tools — GitHub Pages serves the repo root directly.

**Tech Stack:** HTML5, CSS3, vanilla JS (testimonials carousel only), GitHub Pages

---

## Site Inventory

**Navigation (RTL, right → left):**
- בית → `/`
- אודות → `/אודות-הדרך/`
- בנימה אישית → `/אודות/`
- ייעוץ ואימון (dropdown parent, no own page):
  - ייעוץ אישי - עין הבדולח → `/ייעוץ-אישי-עין-הבדולח/`
  - אימון זוגי → `/אימון-זוגי/`
  - מרווקות לזוגיות → `/מרווקות-לזוגיות/`
- ~~שווה קריאה~~ (removed per spec)
- ~~צור קשר~~ (removed — was a 404)

**Footer:** Phone `052-3238867` (→ `tel:052-3238867`), email `t@ilact.com`

**Design tokens:** Background `#FFF8F1`, text `#000000`, accent/links `#39251C`, font: Assistant (body) + Adler/cursive (testimonials), border-radius `0px`

**Testimonials (5 slides):**
1. "זכינו להכיר אישה מיוחדת,חזקה ומלאת אמונה,עם יכולת נדירה לגעת בכאב, ייאוש לא קיים אצלך בלקסיקון, לוחמת של אהבה ואמת שפיה וליבה שווים" — אריאלי
2. "תודה על אוזן קשבת, למדתי איתך וממך הרבה על עצמי, אני מאוד מעריכה אותך על האמת הפשוטה והכנות שבך" — ענבר
3. "טליה השיחות שלנו תמיד עושות רק טוב, אני רוצה להגיד תודה על התמיכה הרגשית והרוחנית, על הדרך שעברתי , בשבילי זה היה בום (כמו שהילי אומרת)" — שרון
4. "בהמלצת חבר הגעתי סקפטי לגמרי, לא היה פשוט עבורי להיפתח אבל הופתעתי מהאמון שנתתי בך, תודה על הסבלנות." — חגי
5. "הגעתי אלייך אחרי משבר בזוגיות, מצאתי את עצמי יושבת ובוכה, עם כאב פנימי ובלבול גדול. הושטת לי יד ומשכת אותי למעלה, מכל מפגש יצאתי חזקה יותר ומלאת תקווה. תודה לך טליה אהובה, אין לי ספק שזאת המתנה הכי טובה שיכלתי לתת לעצמי לגיל 38" — אפרת

---

## Task 1: Create Directory Structure

**Files:** Directory scaffold only

- [ ] **Create all Hebrew page directories and verify**

```powershell
cd "c:\Udi\Work\Entrepreneurship\TaliaWebsite\taliaberman-website"
New-Item -ItemType Directory -Force -Path "אודות-הדרך","אודות","מרווקות-לזוגיות","אימון-זוגי","ייעוץ-אישי-עין-הבדולח","מתח","אחיזה","יחסים","עצמי","css","fonts","images"
```

- [ ] **Verify structure**

```powershell
Get-ChildItem -Name
```

Expected: 12 directories listed (9 Hebrew page dirs + css, fonts, images)

- [ ] **Commit**

```bash
git add -A
git commit -m "feat: create directory structure for all pages and assets"
```

---

## Task 2: Download and Self-Host Fonts

**Files:**
- Create: `fonts/Assistant-Regular.woff2`
- Create: `fonts/Assistant-SemiBold.woff2`
- Create: `fonts/Assistant-Bold.woff2`
- Create: `fonts/Adler.woff2` (or note fallback if unavailable)

- [ ] **Download Assistant font weights from Google Fonts**

Visit `https://fonts.google.com/specimen/Assistant` → Download family → Extract the WOFF2 files for weights 400, 600, 700 and save to `fonts/`:
- `fonts/Assistant-Regular.woff2` (weight 400)
- `fonts/Assistant-SemiBold.woff2` (weight 600)
- `fonts/Assistant-Bold.woff2` (weight 700)

Alternatively, use google-webfonts-helper: visit `https://gwfh.mranftl.com/fonts/assistant?subsets=latin,hebrew` and download the woff2 files for Regular (400), SemiBold (600), Bold (700).

- [ ] **Attempt to download Adler font from Wix CDN**

```powershell
Invoke-WebRequest -Uri "https://static.parastorage.com/services/santa-resources/resources/viewer/user-site-fonts/fonts/Adler/v1/Adler.woff2" -OutFile "fonts/Adler.woff2"
```

If that returns a 404, try:
```powershell
Invoke-WebRequest -Uri "https://fonts.wixstatic.com/ufonts/adler_w26/fonts/adler_w26_regular.woff2" -OutFile "fonts/Adler.woff2"
```

If neither works, the testimonials will fall back to `cursive` (acceptable — it's a decorative quote section). Note the outcome and continue.

- [ ] **Verify font files exist**

```powershell
Get-ChildItem fonts\
```

Expected: 3 Assistant .woff2 files (minimum); Adler.woff2 if download succeeded.

- [ ] **Commit**

```bash
git add fonts/
git commit -m "feat: add self-hosted font files"
```

---

## Task 3: Download All Images

**Files:** All under `images/`

- [ ] **Download images from Wix CDN**

```powershell
$imgs = @{
  "logo.png"                = "https://static.wixstatic.com/media/a99131_16a547c833124b43a42601421ebe2464~mv2.png"
  "hero-banner.jpg"         = "https://static.wixstatic.com/media/a99131_cbab58c1e37f4a34b8312a1fee5f6fbb~mv2.jpg"
  "profile-photo.jpg"       = "https://static.wixstatic.com/media/a99131_2a2d2034f5734b5bbd8ef060ffebd13c~mv2.jpg"
  "sunset-singles.jpg"      = "https://static.wixstatic.com/media/a99131_dbc21f735307423ebc7666a4a0513b78~mv2.jpg"
  "couples-hero.jpg"        = "https://static.wixstatic.com/media/11062b_95d34f15761e4114a57b17823228948ef000.jpg"
  "feather-counseling.jpg"  = "https://static.wixstatic.com/media/a99131_e277ef345f914f4b882746af993cfbcf~mv2.jpg"
}
foreach ($name in $imgs.Keys) {
  Invoke-WebRequest -Uri $imgs[$name] -OutFile "images\$name"
  Write-Host "Downloaded: $name"
}
```

- [ ] **Verify all 6 images downloaded and are non-zero**

```powershell
Get-ChildItem images\ | Select-Object Name, Length
```

Expected: 6 files, each > 10KB

- [ ] **Commit**

```bash
git add images/
git commit -m "feat: download all site images from Wix CDN"
```

---

## Task 4: Write Shared CSS

**Files:**
- Create: `css/style.css`

- [ ] **Write `css/style.css`**

```css
/* ── Fonts ── */
@font-face {
  font-family: 'Assistant';
  src: url('/fonts/Assistant-Regular.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}
@font-face {
  font-family: 'Assistant';
  src: url('/fonts/Assistant-SemiBold.woff2') format('woff2');
  font-weight: 600;
  font-style: normal;
  font-display: swap;
}
@font-face {
  font-family: 'Assistant';
  src: url('/fonts/Assistant-Bold.woff2') format('woff2');
  font-weight: 700;
  font-style: normal;
  font-display: swap;
}
@font-face {
  font-family: 'Adler';
  src: url('/fonts/Adler.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html {
  direction: rtl;
  lang: he;
}

body {
  font-family: 'Assistant', Arial, Helvetica, sans-serif;
  font-size: 18px;
  line-height: 1.6;
  color: #000000;
  background-color: #FFF8F1;
}

a { color: #39251C; text-decoration: none; }
a:hover { text-decoration: underline; }

img { max-width: 100%; height: auto; display: block; }

/* ── Layout ── */
.container {
  max-width: 980px;
  margin: 0 auto;
  padding: 0 24px;
}

/* ── Navigation ── */
.site-nav {
  background-color: #FFF8F1;
  border-bottom: 1px solid #e8ddd4;
  position: sticky;
  top: 0;
  z-index: 100;
}

.site-nav .container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
}

.nav-logo img {
  height: 48px;
  width: auto;
}

.nav-links {
  list-style: none;
  display: flex;
  align-items: center;
  gap: 8px;
  flex-direction: row-reverse;
}

.nav-links > li {
  position: relative;
}

.nav-links a,
.nav-links .dropdown-toggle {
  display: block;
  padding: 8px 12px;
  font-size: 16px;
  font-weight: 600;
  color: #000;
  white-space: nowrap;
  cursor: pointer;
  background: none;
  border: none;
  font-family: inherit;
}

.nav-links a:hover,
.nav-links .dropdown-toggle:hover { color: #39251C; text-decoration: none; }

/* Dropdown */
.nav-links .has-dropdown { position: relative; }

.nav-links .dropdown {
  display: none;
  position: absolute;
  top: 100%;
  right: 0;
  background: #FFF8F1;
  border: 1px solid #e8ddd4;
  list-style: none;
  min-width: 200px;
  z-index: 200;
}

.nav-links .has-dropdown:hover .dropdown,
.nav-links .has-dropdown.open .dropdown { display: block; }

.nav-links .dropdown li a {
  padding: 10px 16px;
  font-weight: 400;
  display: block;
}

.nav-links .dropdown li a:hover { background: #f0e8e0; }

/* ── Page Hero / Banner ── */
.page-hero {
  width: 100%;
  max-height: 320px;
  overflow: hidden;
}

.page-hero img {
  width: 100%;
  object-fit: cover;
}

/* ── Page Content ── */
.page-content {
  padding: 48px 0;
}

.page-content h1 {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 24px;
  color: #39251C;
}

.page-content h2 {
  font-size: 24px;
  font-weight: 700;
  margin: 32px 0 16px;
  color: #39251C;
}

.page-content p {
  margin-bottom: 16px;
  font-size: 18px;
}

.page-content ul {
  margin: 0 24px 16px 0;
}

.page-content ul li {
  margin-bottom: 8px;
}

/* ── Home Hero ── */
.home-hero {
  position: relative;
  text-align: center;
}

.home-hero-banner {
  width: 100%;
  max-height: 320px;
  object-fit: cover;
}

.home-logo {
  display: block;
  margin: 32px auto 16px;
  max-width: 280px;
}

.home-poem {
  font-size: 22px;
  line-height: 2;
  color: #39251C;
  text-align: center;
  padding: 16px 24px 32px;
}

/* ── Home Service Sections ── */
.service-section {
  display: flex;
  align-items: center;
  gap: 40px;
  padding: 48px 0;
  border-bottom: 1px solid #e8ddd4;
}

.service-section:nth-child(even) { flex-direction: row-reverse; }

.service-section img {
  width: 360px;
  flex-shrink: 0;
  object-fit: cover;
}

.service-section .service-text h2 {
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 16px;
  color: #39251C;
}

.service-section .service-text p { font-size: 17px; margin-bottom: 12px; }

.read-more {
  display: inline-block;
  margin-top: 12px;
  color: #39251C;
  font-weight: 600;
  text-decoration: underline;
}

/* ── Testimonials Carousel ── */
.testimonials {
  background: #39251C;
  color: #FFF8F1;
  padding: 64px 24px;
  text-align: center;
}

.testimonials h2 {
  color: #FFF8F1;
  margin-bottom: 32px;
  font-size: 24px;
}

.testimonial-slide {
  display: none;
  max-width: 700px;
  margin: 0 auto;
  opacity: 0;
  transition: opacity 0.6s ease;
}

.testimonial-slide.active {
  display: block;
  opacity: 1;
}

.testimonial-slide blockquote {
  font-family: 'Adler', cursive;
  font-size: 26px;
  line-height: 1.6;
  margin-bottom: 24px;
  color: #FFF8F1;
}

.testimonial-slide cite {
  font-style: normal;
  font-weight: 600;
  font-size: 18px;
}

.testimonial-dots {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 32px;
}

.testimonial-dots button {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: none;
  background: rgba(255,248,241,0.4);
  cursor: pointer;
  padding: 0;
}

.testimonial-dots button.active { background: #FFF8F1; }

/* ── שווה קריאה (hidden, preserved for future) ── */
.shave-kriya { display: none; }

/* ── Footer ── */
.site-footer {
  background: #39251C;
  color: #FFF8F1;
  padding: 40px 0;
  text-align: center;
  font-size: 16px;
}

.site-footer a { color: #FFF8F1; }
.site-footer a:hover { text-decoration: underline; }

.footer-contact {
  display: flex;
  justify-content: center;
  gap: 32px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}

/* ── Responsive ── */
@media (max-width: 768px) {
  .service-section { flex-direction: column !important; }
  .service-section img { width: 100%; }
  .nav-links { gap: 0; }
  .nav-links a, .nav-links .dropdown-toggle { padding: 8px 8px; font-size: 14px; }
  .home-poem { font-size: 18px; }
  .testimonial-slide blockquote { font-size: 20px; }
}
```

- [ ] **Open in browser to verify no syntax errors and base styles look correct**

Start a local server:
```powershell
python -m http.server 8080
```
Navigate to `http://localhost:8080` — page should show `#FFF8F1` background. (index.html doesn't exist yet so you'll see a directory listing — that's fine.)

- [ ] **Commit**

```bash
git add css/style.css
git commit -m "feat: add shared CSS with RTL layout, tokens, nav, testimonials, footer"
```

---

## Task 5: Shared Nav & Footer Snippet (Reference)

This is a **reference task** — the HTML below is copy-pasted into every page file. No files created here.

**Nav HTML** (goes inside `<body>`, before `<main>`):

```html
<nav class="site-nav">
  <div class="container">
    <a href="/" class="nav-logo"><img src="/images/logo.png" alt="טליה ברמן לוגו"></a>
    <ul class="nav-links">
      <li><a href="/">בית</a></li>
      <li><a href="/אודות-הדרך/">אודות</a></li>
      <li><a href="/אודות/">בנימה אישית</a></li>
      <li class="has-dropdown">
        <button class="dropdown-toggle" aria-expanded="false" aria-haspopup="true">ייעוץ ואימון ▾</button>
        <ul class="dropdown">
          <li><a href="/ייעוץ-אישי-עין-הבדולח/">ייעוץ אישי - עין הבדולח</a></li>
          <li><a href="/אימון-זוגי/">אימון זוגי</a></li>
          <li><a href="/מרווקות-לזוגיות/">מרווקות לזוגיות</a></li>
        </ul>
      </li>
    </ul>
  </div>
</nav>
```

**Footer HTML** (goes after `</main>`, before `</body>`):

```html
<footer class="site-footer">
  <div class="container">
    <div class="footer-contact">
      <span><a href="tel:052-3238867">052-3238867</a></span>
      <span><a href="mailto:t@ilact.com">t@ilact.com</a></span>
    </div>
    <p>טליה ברמן ייעוץ ואימון אישי זוגי | רמת השרון</p>
  </div>
</footer>

<script>
/* Mobile dropdown toggle */
document.querySelectorAll('.dropdown-toggle').forEach(btn => {
  btn.addEventListener('click', () => {
    const li = btn.closest('.has-dropdown');
    const open = li.classList.toggle('open');
    btn.setAttribute('aria-expanded', open);
  });
});
</script>
```

---

## Task 6: Home Page

**Files:**
- Create: `index.html`

- [ ] **Create `index.html`**

```html
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>טליה ברמן ייעוץ ואימון אישי זוגי | עין הבדולח | רמת השרון</title>
  <meta name="description" content="טליה ברמן ייעוץ ואימון אישי זוגי, מאמינה ביכולת של כל אדם לצמוח ולקחת אחריות על חייו.">
  <meta name="google-site-verification" content="wvSyn234b7e5W_VghEFBSNyeBVhaJnIsU5LGIBHM6LA">
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>

<!-- NAV (copy from Task 5) -->
<nav class="site-nav">
  <div class="container">
    <a href="/" class="nav-logo"><img src="/images/logo.png" alt="טליה ברמן לוגו"></a>
    <ul class="nav-links">
      <li><a href="/">בית</a></li>
      <li><a href="/אודות-הדרך/">אודות</a></li>
      <li><a href="/אודות/">בנימה אישית</a></li>
      <li class="has-dropdown">
        <button class="dropdown-toggle" aria-expanded="false" aria-haspopup="true">ייעוץ ואימון ▾</button>
        <ul class="dropdown">
          <li><a href="/ייעוץ-אישי-עין-הבדולח/">ייעוץ אישי - עין הבדולח</a></li>
          <li><a href="/אימון-זוגי/">אימון זוגי</a></li>
          <li><a href="/מרווקות-לזוגיות/">מרווקות לזוגיות</a></li>
        </ul>
      </li>
    </ul>
  </div>
</nav>

<main>
  <!-- Hero Banner -->
  <div class="home-hero">
    <img class="home-hero-banner" src="/images/hero-banner.jpg" alt="">
  </div>

  <!-- Logo + Poem -->
  <div style="text-align:center; padding: 40px 24px 0;">
    <img class="home-logo" src="/images/logo.png" alt="טליה ברמן">
    <p class="home-poem">
      בהגיעי תפתח הדלת<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;אל היד המושטת<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;אל חום לבבך<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;אל שמחת משכנך
    </p>
  </div>

  <!-- Service Sections -->
  <div class="container">

    <!-- אודות הדרך -->
    <section class="service-section">
      <div class="service-text">
        <h2>אודות הדרך</h2>
        <p>בכל אדם קיים טוב וחבוי פוטנציאל פנימי שרק רוצה להתעורר ולממש את הטוב שבו, להוציא מן הכוח אל הפועל, זהו הבסיס לכל תהליך בו אני מלווה אנשים.</p>
        <p>אני מאמינה ביכולת של כל אדם לצמוח ולקחת אחריות על חייו, דרך התבוננות כנה ורצון לפעול בהתמדה.</p>
        <a class="read-more" href="/אודות-הדרך/">קרא עוד</a>
      </div>
    </section>

    <!-- בנימה אישית -->
    <section class="service-section">
      <img src="/images/profile-photo.jpg" alt="טליה ברמן">
      <div class="service-text">
        <h2>בנימה אישית</h2>
        <p>נעים להכיר, שמי טליה ברמן, בת למשפחה אוהבת, נשואה באהבה למיכאל. יועצת בכירה לבריאות הנפש עין הבדולח, מאמנת זוגית, מלווה תהליכי צמיחה והתפתחות אישיים וזוגיים.</p>
        <a class="read-more" href="/אודות/">קרא עוד</a>
      </div>
    </section>

    <!-- מרווקות לזוגיות -->
    <section class="service-section">
      <img src="/images/sunset-singles.jpg" alt="שקיעה">
      <div class="service-text">
        <h2>צעדים מרווקות לזוגיות</h2>
        <p>הייאוש לא נעשה יותר נח, הרגשה מוכרת? כולם מאד רוצים זוגיות אבל חוששים לעבור שינוי כי לפעמים הוא כרוך בכאב.</p>
        <p>את/ה רוצה למצוא את בן/בת הזוג המתאים/ה לך. הדרך מתחילה קודם כל בתוכך.</p>
        <a class="read-more" href="/מרווקות-לזוגיות/">קרא עוד</a>
      </div>
    </section>

    <!-- אימון זוגי -->
    <section class="service-section">
      <img src="/images/couples-hero.jpg" alt="אימון זוגי">
      <div class="service-text">
        <h2>אימון זוגי</h2>
        <p>זוגיות טובה היא דבר מרכזי בבריאות הנפשית של האדם ומשפיעה על אושרו. כולנו רוצים להרגיש אהובים ומקובלים, גם בחלקים הפגיעים שלנו.</p>
        <p>רוצים זוגיות שמחה? היא זקוקה לתחזוקה, היא דורשת מחויבות, מוטיבציה ועשייה.</p>
        <a class="read-more" href="/אימון-זוגי/">קרא עוד</a>
      </div>
    </section>

    <!-- ייעוץ אישי -->
    <section class="service-section">
      <img src="/images/feather-counseling.jpg" alt="ייעוץ אישי">
      <div class="service-text">
        <h2>ייעוץ ואימון אישי</h2>
        <p>בריאות הנפש בדרך היהדות - עין הבדולח, היא עבודה שורשית ועמוקה המתמקדת במפגש של האדם עם האתגרים והאירועים בהווה.</p>
        <p>חכמת החסידות מגלה לנו את הקשר בין גוף לנפש ובין הנסתר לגלוי השזורים זה בזה במעגל החיים.</p>
        <a class="read-more" href="/ייעוץ-אישי-עין-הבדולח/">קרא עוד</a>
      </div>
    </section>

  </div><!-- /container -->

  <!-- Testimonials Carousel -->
  <section class="testimonials">
    <div class="testimonial-slide active">
      <blockquote>"זכינו להכיר אישה מיוחדת,חזקה ומלאת אמונה,עם יכולת נדירה לגעת בכאב, ייאוש לא קיים אצלך בלקסיקון, לוחמת של אהבה ואמת שפיה וליבה שווים"</blockquote>
      <cite>אריאלי</cite>
    </div>
    <div class="testimonial-slide">
      <blockquote>"תודה על אוזן קשבת, למדתי איתך וממך הרבה על עצמי, אני מאוד מעריכה אותך על האמת הפשוטה והכנות שבך"</blockquote>
      <cite>ענבר</cite>
    </div>
    <div class="testimonial-slide">
      <blockquote>"טליה השיחות שלנו תמיד עושות רק טוב, אני רוצה להגיד תודה על התמיכה הרגשית והרוחנית, על הדרך שעברתי , בשבילי זה היה בום (כמו שהילי אומרת)"</blockquote>
      <cite>שרון</cite>
    </div>
    <div class="testimonial-slide">
      <blockquote>"בהמלצת חבר הגעתי סקפטי לגמרי, לא היה פשוט עבורי להיפתח אבל הופתעתי מהאמון שנתתי בך, תודה על הסבלנות."</blockquote>
      <cite>חגי</cite>
    </div>
    <div class="testimonial-slide">
      <blockquote>"הגעתי אלייך אחרי משבר בזוגיות, מצאתי את עצמי יושבת ובוכה, עם כאב פנימי ובלבול גדול. הושטת לי יד ומשכת אותי למעלה, מכל מפגש יצאתי חזקה יותר ומלאת תקווה. תודה לך טליה אהובה, אין לי ספק שזאת המתנה הכי טובה שיכלתי לתת לעצמי לגיל 38"</blockquote>
      <cite>אפרת</cite>
    </div>
    <div class="testimonial-dots" aria-hidden="true">
      <button class="active" aria-label="עדות 1"></button>
      <button aria-label="עדות 2"></button>
      <button aria-label="עדות 3"></button>
      <button aria-label="עדות 4"></button>
      <button aria-label="עדות 5"></button>
    </div>
  </section>

  <!-- שווה קריאה — HIDDEN, preserved for future use -->
  <section class="shave-kriya">
    <div class="container">
      <h2>שווה קריאה</h2>
      <ul>
        <li><a href="/אחיזה/">אחיזה</a></li>
        <li><a href="/מתח/">מתח</a></li>
        <li><a href="/יחסים/">יחסים</a></li>
        <li><a href="/עצמי/">עצמי</a></li>
      </ul>
    </div>
  </section>

</main>

<!-- FOOTER (copy from Task 5) -->
<footer class="site-footer">
  <div class="container">
    <div class="footer-contact">
      <span><a href="tel:052-3238867">052-3238867</a></span>
      <span><a href="mailto:t@ilact.com">t@ilact.com</a></span>
    </div>
    <p>טליה ברמן ייעוץ ואימון אישי זוגי | רמת השרון</p>
  </div>
</footer>

<script>
/* Mobile dropdown toggle */
document.querySelectorAll('.dropdown-toggle').forEach(btn => {
  btn.addEventListener('click', () => {
    const li = btn.closest('.has-dropdown');
    const open = li.classList.toggle('open');
    btn.setAttribute('aria-expanded', open);
  });
});

/* Testimonials carousel */
(function() {
  const slides = document.querySelectorAll('.testimonial-slide');
  const dots = document.querySelectorAll('.testimonial-dots button');
  let current = 0;

  function show(n) {
    slides[current].classList.remove('active');
    dots[current].classList.remove('active');
    current = (n + slides.length) % slides.length;
    slides[current].classList.add('active');
    dots[current].classList.add('active');
  }

  dots.forEach((dot, i) => dot.addEventListener('click', () => show(i)));

  setInterval(() => show(current + 1), 5000);
})();
</script>

</body>
</html>
```

- [ ] **Open `http://localhost:8080` and verify:**
  - Nav shows: בית, אודות, בנימה אישית, ייעוץ ואימון (dropdown)
  - Hero banner image loads
  - Logo appears
  - Poem text is centered
  - 5 service sections visible with images and "קרא עוד" links
  - Testimonials section shows dark background with quote, auto-advances every 5 sec
  - שווה קריאה section is invisible
  - Footer shows phone as clickable link and email

- [ ] **Commit**

```bash
git add index.html
git commit -m "feat: add home page with hero, services, testimonials carousel, hidden blog section"
```

---

## Task 7: אודות הדרך Page

**Files:**
- Create: `אודות-הדרך/index.html`

- [ ] **Create `אודות-הדרך/index.html`**

```html
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>אודות | טליה ברמן</title>
  <meta name="google-site-verification" content="wvSyn234b7e5W_VghEFBSNyeBVhaJnIsU5LGIBHM6LA">
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>

<nav class="site-nav">
  <div class="container">
    <a href="/" class="nav-logo"><img src="/images/logo.png" alt="טליה ברמן לוגו"></a>
    <ul class="nav-links">
      <li><a href="/">בית</a></li>
      <li><a href="/אודות-הדרך/" aria-current="page">אודות</a></li>
      <li><a href="/אודות/">בנימה אישית</a></li>
      <li class="has-dropdown">
        <button class="dropdown-toggle" aria-expanded="false" aria-haspopup="true">ייעוץ ואימון ▾</button>
        <ul class="dropdown">
          <li><a href="/ייעוץ-אישי-עין-הבדולח/">ייעוץ אישי - עין הבדולח</a></li>
          <li><a href="/אימון-זוגי/">אימון זוגי</a></li>
          <li><a href="/מרווקות-לזוגיות/">מרווקות לזוגיות</a></li>
        </ul>
      </li>
    </ul>
  </div>
</nav>

<main class="container page-content">
  <h1>אודות הדרך</h1>
  <p>בכל אדם קיים טוב וחבוי פוטנציאל פנימי שרק רוצה להתעורר ולממש את הטוב שבו, להוציא מן הכוח אל הפועל, זהו הבסיס לכל תהליך בו אני מלווה אנשים.</p>
  <p>אני מאמינה ביכולת של כל אדם לצמוח ולקחת אחריות על חייו, דרך התבוננות כנה ורצון לפעול בהתמדה. להיפרד מסערות הנפש, להיטיב עם עצמנו והסובבים אותנו, לתת את תרומתנו לעולם, מתוך אמונה שהחיים טובים והם ניתנו לנו כמתנה.</p>
  <p>בכל מפגש נעבוד על האתגר איתו אתם מתמודדים בהווה. נפסיק לראות את עצמנו כ"קורבנות" של נסיבות חיצוניות ושל עברנו, נרפה מאמונות מגבילות ותגובות אוטומטיות, נתוודע אל מהות חיינו וייעודנו מתוך מודעות וכוונה להיות באמת "בעלי-הבית" של חיינו. נלמד כלים ונתרגל אותם יחד על מנת שתוכלו לעשות זאת בעצמכם ללא ליווי ולהמשיך לצמוח בחייכם.</p>

  <h2>הליווי שלי מתאים</h2>
  <p>למי שמתמודד עם קושי רגשי בחייו האישיים או הזוגיים, ורוצה ליווי על מנת לאזן ולווסת מצבים רגשיים אלה. תהליך הליווי ממוקד ומסייע בבירור הרצון ומטרות החיים, דרך שימוש בחוזקות והעוצמות של האדם.</p>

  <h2>האתגרים שאני עובדת עם אנשים</h2>
  <ul>
    <li>חוסר איזון נפשי</li>
    <li>בעיה בתקשורת ובמערכות יחסים עם בני זוג / משפחה / חברים / עבודה</li>
    <li>כאב רגשי / אבל או פרידה מאדם קרוב</li>
    <li>פרידה מזוגיות קשה, נטישה, פגיעה</li>
    <li>מחשבות מטרידות</li>
    <li>פחדים / חרדות</li>
    <li>חוסר מיקוד</li>
    <li>קושי בקבלת החלטות</li>
    <li>חוסר יכולת להביע רגשות</li>
  </ul>

  <p>לבקש עזרה לא תמיד קל, אבל חשוב כדי לחיות חיים מלאים מתוך איזון.</p>
  <p>מחכה לפגוש אותך</p>

  <h2>תעודות והסמכות</h2>
  <ul>
    <li>B.A בניהול, האוניברסיטה פתוחה</li>
    <li>יועצת בכירה לרפואת הנפש בדרך היהדות, מכללת אילמה</li>
    <li>אימון זוגי, מכון טוב ומיטיב</li>
    <li>התמחות מתקדמת באימון לאהבה וזוגיות, BLUEBIRD ACADEMY</li>
    <li>מנטורית בעמותת "חיבורים" ליווי למציאת זוגיות</li>
    <li>רייקי, העבודה, דמיון מודרך, הו'אופונופונו וכלים נוספים</li>
  </ul>
</main>

<footer class="site-footer">
  <div class="container">
    <div class="footer-contact">
      <span><a href="tel:052-3238867">052-3238867</a></span>
      <span><a href="mailto:t@ilact.com">t@ilact.com</a></span>
    </div>
    <p>טליה ברמן ייעוץ ואימון אישי זוגי | רמת השרון</p>
  </div>
</footer>

<script>
document.querySelectorAll('.dropdown-toggle').forEach(btn => {
  btn.addEventListener('click', () => {
    const li = btn.closest('.has-dropdown');
    const open = li.classList.toggle('open');
    btn.setAttribute('aria-expanded', open);
  });
});
</script>
</body>
</html>
```

- [ ] **Verify at `http://localhost:8080/אודות-הדרך/`** — page loads, nav highlights "אודות", all content visible
- [ ] **Commit**
```bash
git add "אודות-הדרך/"
git commit -m "feat: add אודות הדרך page"
```

---

## Task 8: בנימה אישית Page

**Files:**
- Create: `אודות/index.html`

- [ ] **Create `אודות/index.html`**

```html
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>בנימה אישית | טליה ברמן</title>
  <meta name="google-site-verification" content="wvSyn234b7e5W_VghEFBSNyeBVhaJnIsU5LGIBHM6LA">
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>

<nav class="site-nav">
  <div class="container">
    <a href="/" class="nav-logo"><img src="/images/logo.png" alt="טליה ברמן לוגו"></a>
    <ul class="nav-links">
      <li><a href="/">בית</a></li>
      <li><a href="/אודות-הדרך/">אודות</a></li>
      <li><a href="/אודות/" aria-current="page">בנימה אישית</a></li>
      <li class="has-dropdown">
        <button class="dropdown-toggle" aria-expanded="false" aria-haspopup="true">ייעוץ ואימון ▾</button>
        <ul class="dropdown">
          <li><a href="/ייעוץ-אישי-עין-הבדולח/">ייעוץ אישי - עין הבדולח</a></li>
          <li><a href="/אימון-זוגי/">אימון זוגי</a></li>
          <li><a href="/מרווקות-לזוגיות/">מרווקות לזוגיות</a></li>
        </ul>
      </li>
    </ul>
  </div>
</nav>

<main class="container page-content">
  <div style="display:flex; gap:40px; align-items:flex-start; flex-wrap:wrap;">
    <div style="flex:1; min-width:260px;">
      <h1>בנימה אישית</h1>
      <p>נעים להכיר, שמי טליה ברמן, בת למשפחה אוהבת, נשואה באהבה למיכאל. יועצת בכירה לבריאות הנפש עין הבדולח, מאמנת זוגית, מלווה תהליכי צמיחה והתפתחות אישיים וזוגיים.</p>
      <p>מאחוריי קריירה ארוכה של ניהול בתחום ההפקות, בה הייתה לי הזכות לתמוך וללוות אנשים בזמנים שונים בחייהם באופן אישי ומקצועי. באותן שנים עברתי טיפולי פוריות שלוו בטלטלה וציפייה, בין קושי לתקווה, שהובילו אותי להיענות לקריאה פנימית שהגיע זמני לצאת אל "המסע" לניהול הנפש שלי.</p>
      <p>הדרך הובילה אותי אל המקום בו אני נמצאת היום, להושיט יד לאנשים במסע חייהם, מתוך אמונה ואופטימיות שכולנו צועדים באותה דרך ולכל אחד השביל הייחודי לו, ניסיון חייו ואישיותו.</p>
      <p>מתוך סקרנות ורצון להבין את העולם שמעבר, שתמיד ריתק אותי, אני לומדת ומתעמקת בתורת החסידות והקבלה, המעניקה לי ראייה רחבה ובהירה בעבודתי אשר התפתחה מתוך תהליך אישי ולימוד גישות שונות.</p>
      <p>במה שונה במהותה הדרך בה אני עובדת? הנגיעה בהיבט הרגשי רוחני של הכאב עד לשורשו.</p>
      <p>אני עוד "יד" מושטת בצידי הדרך, מיני רבות וטובות. אם זה מרגיש לך נכון ומתאים אשמח לפגוש אותך.</p>

      <h2>תעודות והסמכות</h2>
      <ul>
        <li>B.A בניהול, האוניברסיטה פתוחה</li>
        <li>יועצת בכירה לרפואת הנפש בדרך היהדות, מכללת אילמה</li>
        <li>אימון זוגי, מכון טוב ומיטיב</li>
        <li>התמחות מתקדמת באימון לאהבה וזוגיות, BLUEBIRD ACADEMY</li>
        <li>מנטורית בעמותת "חיבורים" ליווי למציאת זוגיות</li>
        <li>רייקי, העבודה, דמיון מודרך, הו'אופונופונו וכלים נוספים</li>
      </ul>
    </div>
    <img src="/images/profile-photo.jpg" alt="טליה ברמן" style="width:260px; flex-shrink:0; object-fit:cover;">
  </div>
</main>

<footer class="site-footer">
  <div class="container">
    <div class="footer-contact">
      <span><a href="tel:052-3238867">052-3238867</a></span>
      <span><a href="mailto:t@ilact.com">t@ilact.com</a></span>
    </div>
    <p>טליה ברמן ייעוץ ואימון אישי זוגי | רמת השרון</p>
  </div>
</footer>

<script>
document.querySelectorAll('.dropdown-toggle').forEach(btn => {
  btn.addEventListener('click', () => {
    const li = btn.closest('.has-dropdown');
    const open = li.classList.toggle('open');
    btn.setAttribute('aria-expanded', open);
  });
});
</script>
</body>
</html>
```

- [ ] **Verify at `http://localhost:8080/אודות/`** — photo appears beside text, nav highlights "בנימה אישית"
- [ ] **Commit**
```bash
git add "אודות/"
git commit -m "feat: add בנימה אישית page"
```

---

## Task 9: מרווקות לזוגיות Page

**Files:**
- Create: `מרווקות-לזוגיות/index.html`

- [ ] **Create `מרווקות-לזוגיות/index.html`**

```html
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>מרווקות לזוגיות | טליה ברמן</title>
  <meta name="google-site-verification" content="wvSyn234b7e5W_VghEFBSNyeBVhaJnIsU5LGIBHM6LA">
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>

<nav class="site-nav">
  <div class="container">
    <a href="/" class="nav-logo"><img src="/images/logo.png" alt="טליה ברמן לוגו"></a>
    <ul class="nav-links">
      <li><a href="/">בית</a></li>
      <li><a href="/אודות-הדרך/">אודות</a></li>
      <li><a href="/אודות/">בנימה אישית</a></li>
      <li class="has-dropdown">
        <button class="dropdown-toggle" aria-expanded="false" aria-haspopup="true">ייעוץ ואימון ▾</button>
        <ul class="dropdown">
          <li><a href="/ייעוץ-אישי-עין-הבדולח/">ייעוץ אישי - עין הבדולח</a></li>
          <li><a href="/אימון-זוגי/">אימון זוגי</a></li>
          <li><a href="/מרווקות-לזוגיות/" aria-current="page">מרווקות לזוגיות</a></li>
        </ul>
      </li>
    </ul>
  </div>
</nav>

<main>
  <div class="page-hero">
    <img src="/images/sunset-singles.jpg" alt="שקיעה">
  </div>
  <div class="container page-content">
    <h1>ביקשתי את שאהבה נפשי</h1>
    <h1>צעדים מרווקות לזוגיות</h1>
    <p>הייאוש לא נעשה יותר נח, הרגשה מוכרת?</p>
    <p>התדמית שסיגלתי לעצמי עוזרת לי להסתיר את העולם הפנימי ואת הרגשות שלי, היא עוזרת לי לחוש בטחון אבל היא מביאה איתה גם בדידות כואבת, כזאת שלא מאפשרת לי לשתף עם אף אחד.</p>
    <p>כולם מאד רוצים זוגיות אבל חוששים לעבור שינוי כי לפעמים הוא כרוך בכאב. לא תמיד קל להתמודד עם כל הרעשים והלחצים מהמשפחה והסביבה בעוד שקולך הפנימי הולך ונעלם, אבל כשמגיעים לזה בתהליך הנכון זה קצת פחות מפחיד ואפילו מרגש.</p>
    <p>את/ה רוצה למצוא את בן/בת הזוג המתאים/ה לך, שתוכל/י לסמוך עליו/ה ולבנות איתו/ה יחד בית יציב ומשפחה שמחה. הדרך למציאת בן/בת הזוג המתאים עבורך, מתחילה קודם כל בתוכך.</p>
    <p>משפט פופולרי ברווקות: "אני לא רוצה להתפשר על משיכה, אהבה..."</p>
    <p>שינוי הוא לא פשרה, שינוי הוא תובנות חדשות.</p>
    <p>לתת צ'אנס ל-3 דייטים זה לא בזבוז זמן, זה זמן לימוד, לפגוש את עצמך בתוך זוגיות. ייתכן ובהתחלה לא יהיו הפרפרים שתמיד חיפשת, אהבה ומשיכה מתעוררות בהדרגה, אבל יהיה שם משהו נכון שיוביל אותך לזוגיות המיוחלת למרות הספקות שבדרך.</p>
    <p>איך באמת אפשר להצליח להקשיב לקול הפנימי שלך שיודע מה באמת טוב עבורך?</p>
    <p>ליווי אישי ומתן כלים שיאפשרו לך להיפתח, להקשיב ולגלות מה באמת נכון עבורך, אילו תכונות ומאפיינים באמת חשובים לך אצל בן/בת הזוג ועל מה אפשר וכדאי להתגמש. בתום התהליך יפחתו כאבי הלב מאכזבות ובחירות שגויות, הפחדים ייעלמו, הביטחון שלך בעצמך יגדל, קשרים יתפתחו ויעמיקו, תקבל/י יותר הצעות להיכרויות, כי מסביבך יבינו מה את/ה רוצה.</p>
    <p>להגיד כן, להתקדם הלאה ולהיפתח לזוגיות בריאה ונכונה עבורך, זוגיות מבוססת אמון, אינטימיות וצמיחה הדדית.</p>
    <p>אני לא לבד בעולם, הכל בסדר איתי, אני אהוב/ה בדיוק כמו שאני.</p>
    <p><strong>אני כאן עבורך, בוא/י נדבר.</strong></p>
  </div>
</main>

<footer class="site-footer">
  <div class="container">
    <div class="footer-contact">
      <span><a href="tel:052-3238867">052-3238867</a></span>
      <span><a href="mailto:t@ilact.com">t@ilact.com</a></span>
    </div>
    <p>טליה ברמן ייעוץ ואימון אישי זוגי | רמת השרון</p>
  </div>
</footer>

<script>
document.querySelectorAll('.dropdown-toggle').forEach(btn => {
  btn.addEventListener('click', () => {
    const li = btn.closest('.has-dropdown');
    const open = li.classList.toggle('open');
    btn.setAttribute('aria-expanded', open);
  });
});
</script>
</body>
</html>
```

- [ ] **Verify at `http://localhost:8080/מרווקות-לזוגיות/`** — sunset image hero, full content, dropdown highlights "מרווקות לזוגיות"
- [ ] **Commit**
```bash
git add "מרווקות-לזוגיות/"
git commit -m "feat: add מרווקות לזוגיות page"
```

---

## Task 10: אימון זוגי Page

**Files:**
- Create: `אימון-זוגי/index.html`

- [ ] **Create `אימון-זוגי/index.html`**

```html
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>אימון זוגי | טליה ברמן</title>
  <meta name="google-site-verification" content="wvSyn234b7e5W_VghEFBSNyeBVhaJnIsU5LGIBHM6LA">
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>

<nav class="site-nav">
  <div class="container">
    <a href="/" class="nav-logo"><img src="/images/logo.png" alt="טליה ברמן לוגו"></a>
    <ul class="nav-links">
      <li><a href="/">בית</a></li>
      <li><a href="/אודות-הדרך/">אודות</a></li>
      <li><a href="/אודות/">בנימה אישית</a></li>
      <li class="has-dropdown">
        <button class="dropdown-toggle" aria-expanded="false" aria-haspopup="true">ייעוץ ואימון ▾</button>
        <ul class="dropdown">
          <li><a href="/ייעוץ-אישי-עין-הבדולח/">ייעוץ אישי - עין הבדולח</a></li>
          <li><a href="/אימון-זוגי/" aria-current="page">אימון זוגי</a></li>
          <li><a href="/מרווקות-לזוגיות/">מרווקות לזוגיות</a></li>
        </ul>
      </li>
    </ul>
  </div>
</nav>

<main>
  <div class="page-hero">
    <img src="/images/couples-hero.jpg" alt="אימון זוגי">
  </div>
  <div class="container page-content">
    <h1>כַּמַּיִם הַפָּנִים לַפָּנִים כֵּן לֵב הָאָדָם לָאָדָם</h1>
    <h1>אימון זוגי</h1>
    <p>זוגיות טובה היא דבר מרכזי בבריאות הנפשית של האדם ומשפיעה על אושרו, היא מאפשרת לנו לעבוד על עצמנו ולגדול בתוך הקשר הזוגי. כולנו רוצים להרגיש אהובים ומקובלים, גם בחלקים הפגיעים והפחות "מחמיאים" שלנו, כולנו רוצים לדעת שאנחנו יכולים להיות חלשים וחשופים מול בן הזוג שלנו, בלי שזה יגרור ביקורת או זלזול.</p>
    <p>הפצעים והמשברים בזוגיות משותפים לרובנו, והם דורשים התבוננות פנימה, בתוכי. המציאות החיצונית היא מראה לעולם הפנימי "כמים הפנים לפנים כך לב האדם לאדם".</p>
    <p>זוגות יכולים לחיות בסבל שנים בלי לבקש עזרה, כי קל יותר להתנתק ולתת למערכת היחסים לדעוך. אף אחד לא אוהב מריבות וכעסים, ההימנעות מלדבר על הקשיים מייצר כאב שלאט לאט צף עד שהוא מתפרץ.</p>
    <p>עבודת אימון זוגית מזמנת לעיתים פגישות קשות, בתהליך מסודר ולמידה ניתן להגיע לזוגיות שמחה ושלום בית למרות המחלוקות. היכולת של בני הזוג לפתור משברים ולדבר על מה שכואב להם עוברת דרך תקשורת טובה והקשבה, ללמוד לבטא את הרצונות ולשוחח ממקום נקי, זה המפתח למערכת יחסים בריאה ומוצלחת.</p>
    <p>קשר זוגי במהותו הוא חיבור פנימי ועמוק שמביא למימוש וביטוי את החלקים הטובים והחיוביים של כל אחד מבני הזוג, להיות שמח בנוכחותו של האחר בחייו, לשים אותו במרכז ולהיות שם עבורו. המחויבות אחד כלפי השנייה היא הדבר הטוב ביותר שהם יכולים לתת זה לזו, מה שיוביל לקשר של אמון, ביטחון והשקעה מתוך הנאה והתלהבות.</p>
    <p>רוצים זוגיות שמחה? היא זקוקה לתחזוקה, היא דורשת מחויבות, מוטיבציה ועשייה, להבין את האחר ולהיות שם עבורו, עבודה העוברת דרך השכל והרגש וממלאת אותנו בחיות, עבודה על הזוגיות היא זכות הכרחית.</p>
    <p>בשניים זה נכון, אבל גם שינוי אצל אחד מבני הזוג יכול לייצר שינוי משמעותי במערכת היחסים.</p>
    <p>תאמינו, אם אפשר לקלקל אפשר גם לתקן.</p>
    <p><strong>אל תחכו בואו נדבר</strong></p>
  </div>
</main>

<footer class="site-footer">
  <div class="container">
    <div class="footer-contact">
      <span><a href="tel:052-3238867">052-3238867</a></span>
      <span><a href="mailto:t@ilact.com">t@ilact.com</a></span>
    </div>
    <p>טליה ברמן ייעוץ ואימון אישי זוגי | רמת השרון</p>
  </div>
</footer>

<script>
document.querySelectorAll('.dropdown-toggle').forEach(btn => {
  btn.addEventListener('click', () => {
    const li = btn.closest('.has-dropdown');
    const open = li.classList.toggle('open');
    btn.setAttribute('aria-expanded', open);
  });
});
</script>
</body>
</html>
```

- [ ] **Verify at `http://localhost:8080/אימון-זוגי/`**
- [ ] **Commit**
```bash
git add "אימון-זוגי/"
git commit -m "feat: add אימון זוגי page"
```

---

## Task 11: ייעוץ אישי - עין הבדולח Page

**Files:**
- Create: `ייעוץ-אישי-עין-הבדולח/index.html`

- [ ] **Create `ייעוץ-אישי-עין-הבדולח/index.html`**

```html
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ייעוץ אישי - עין הבדולח | טליה ברמן</title>
  <meta name="google-site-verification" content="wvSyn234b7e5W_VghEFBSNyeBVhaJnIsU5LGIBHM6LA">
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>

<nav class="site-nav">
  <div class="container">
    <a href="/" class="nav-logo"><img src="/images/logo.png" alt="טליה ברמן לוגו"></a>
    <ul class="nav-links">
      <li><a href="/">בית</a></li>
      <li><a href="/אודות-הדרך/">אודות</a></li>
      <li><a href="/אודות/">בנימה אישית</a></li>
      <li class="has-dropdown">
        <button class="dropdown-toggle" aria-expanded="false" aria-haspopup="true">ייעוץ ואימון ▾</button>
        <ul class="dropdown">
          <li><a href="/ייעוץ-אישי-עין-הבדולח/" aria-current="page">ייעוץ אישי - עין הבדולח</a></li>
          <li><a href="/אימון-זוגי/">אימון זוגי</a></li>
          <li><a href="/מרווקות-לזוגיות/">מרווקות לזוגיות</a></li>
        </ul>
      </li>
    </ul>
  </div>
</nav>

<main>
  <div class="page-hero">
    <img src="/images/feather-counseling.jpg" alt="כנפי רוח">
  </div>
  <div class="container page-content">
    <h1>יש לך כנפי רוח</h1>
    <h1>ייעוץ ואימון אישי - עין הבדולח</h1>
    <p>בריאות הנפש בדרך היהדות - עין הבדולח, היא עבודה שורשית ועמוקה המתמקדת במפגש של האדם עם האתגרים והאירועים בהווה, היא מסייעת בהסרת החסמים הרגשיים, ביציאה ממשברים ושחרור מגורמי סטרס אחרים, נועדה לעזור לנו למצוא כוח ותקווה לחיים.</p>
    <p>חכמת החסידות מגלה לנו את הקשר בין גוף לנפש ובין הנסתר לגלוי השזורים זה בזה במעגל החיים. לכל אדם יש את היכולת והזכות ללמוד את חכמת הבריאה, את הכוחות הפועלים במציאות ולהנהיג את חייו בחכמה ובתבונה מתוך תכלית ומשמעות.</p>
    <p>"החופש" ומציאת הייעוד מתחילים בהכרת הרצונות האמיתיים, המוסתרים והסותרים שלנו, דרך עבודת התבוננות מודעת המאפשרת לנו להסתכל גבוה יותר מהמקום בו אנו נמצאים, למרות הקושי והכאב. הרצון להסתכל, לדמיין ולשאוף למצב מתוקן יותר מתוך בחירה ואחריות אישית לחיים מתקיים בנו תמיד.</p>
    <p>זהו תהליך של היזכרות "רשימו" מתוך שלום פנימי. תחילתו של תהליך הריפוי הוא בהפסקת תנועת ההרעלה הרגשית, תהליך בו נדרשת סבלנות וענווה, תנועה של התפתחות והתעלות.</p>
    <p>האירועים והניסיונות שאנו חווים מפגישים אותנו עם "השליחים" (הורים/בני זוג/ילדים/חברים ועוד) שעוזרים לנו במסע. לעיתים נכעס, נתנתק, נברח או נאשים את האחר מתוך ניסיון לשלוט במה שקורה בחוץ, בעוד שהתשובה לכך מצויה בתוכנו.</p>
    <p>התוצאה היא חיים מתוך שמחה, שלווה ובהירות.</p>

    <h2>התהליך</h2>
    <p>הדרך בה אנחנו חושבים ומפרשים את מה שקורה לנו מייצר את התגובות הרגשיות שלנו. ברוב האירועים בהם אנו חווים משהו רגשי, קשה להגיד מה בא קודם, הרגש או המחשבה, מכיוון שהם שזורים זה בזה ומשפיעים זה על זה. לקוגניציה חשיבות רבה והיא הכלי היעיל להבנה ולמידה. בעזרתה יש לנו את האפשרות והיכולת לשנות ולהסיר חסמים, במטרה לקדם בריאות נפשית וגופנית.</p>

    <h2>איך בנוי תהליך הייעוץ</h2>
    <ul>
      <li>תחילת התהליך כולל היכרות, הסבר על הייעוץ והליווי, הגדרת מטרות</li>
      <li>הקניית כלים להתמודדות בריאה ויעילה עם אתגרי החיים</li>
      <li>שחרור ו/או צמצום השפעת אירועי עבר</li>
      <li>שינוי דפוסים רגשיים ותבניות תגובה אוטומטיות</li>
      <li>העצמת הכוחות החיוביים ורתימתם להשפעה</li>
      <li>"ניקוי רעלים" בנפש</li>
      <li>נשימה והשקטה</li>
    </ul>

    <h2>למה לצפות?</h2>
    <p>להיות שותפים פעילים בתהליך, לדבר בפתיחות ובכנות, לתרגל את הכלים ולהיות מוכנים לבצע שינויים שיסייעו להביא את מירב הפוטנציאל החיובי שלכם לידי ביטוי.</p>

    <h2>הייעוץ והליווי מתאים</h2>
    <p>לאנשים שמתמודדים עם רגשות שליליים כמו כעס, צער, כאב רגשי, אשמה, דאגת יתר, מצבי משבר, פחדים וחרדות, ולמי שמעוניין לשפר מערכות יחסים בכל מעגלי החיים.</p>

    <p>אין מי שיחליף אותי במסע חיי</p>
    <p><strong>אני כאן להושיט יד, בוא/י נדבר</strong></p>
  </div>
</main>

<footer class="site-footer">
  <div class="container">
    <div class="footer-contact">
      <span><a href="tel:052-3238867">052-3238867</a></span>
      <span><a href="mailto:t@ilact.com">t@ilact.com</a></span>
    </div>
    <p>טליה ברמן ייעוץ ואימון אישי זוגי | רמת השרון</p>
  </div>
</footer>

<script>
document.querySelectorAll('.dropdown-toggle').forEach(btn => {
  btn.addEventListener('click', () => {
    const li = btn.closest('.has-dropdown');
    const open = li.classList.toggle('open');
    btn.setAttribute('aria-expanded', open);
  });
});
</script>
</body>
</html>
```

- [ ] **Verify at `http://localhost:8080/ייעוץ-אישי-עין-הבדולח/`**
- [ ] **Commit**
```bash
git add "ייעוץ-אישי-עין-הבדולח/"
git commit -m "feat: add ייעוץ אישי עין הבדולח page"
```

---

## Task 12: Four Landing Pages (מתח, אחיזה, יחסים, עצמי)

All four pages have the same content and structure. Create each one.

**Files:**
- Create: `מתח/index.html`
- Create: `אחיזה/index.html`
- Create: `יחסים/index.html`
- Create: `עצמי/index.html`

**Shared content for all four pages** (the text is identical across them — confirmed from live site):

```
Title: [page name] | טליה ברמן

Content:
את לא לבד בעולם והכל בסדר איתך, את שלמה ואהובה בדיוק כמו שאת, חייך עשירים ומלאים במשפחה, עבודה, חברים, עיסוקים ועוד, הרצון בזוגיות והרצון לבנות את ביתך ומשפחתך ממלא את מחשבותייך ולפעמים גם את הכרית בדמעותייך אבל זה רק זמני!

משפטים כמו: איך את עדיין רווקה, אולי את בררנית, אולי את לא יודעת לבחור נכון, את תמיד נעלבת, שוב פעם את עם בחור שלא מתאים לך, ועוד שלל משפטים, גורמים לך להרגיש פחות טובה וראויה, פחות אהובה ושלמה. הם מהווים מחסום ומחלישים אותך, מה שגורם לך להסתכל על המציאות מתוך חוסר ביטחון עצמי, פחד ותסכול, ביקורתיות וחוסר אמון.

וזה גם לא תמיד קל להתמודד עם כל הרעשים והלחצים מהמשפחה והסביבה, שרוצים לתת עצות ולהשמיע את דעתם בעוד שקולך הפנימי הולך ונעלם, הקול הייחודי שיודע מה באמת טוב עבורך וייעשה אותך מאושרת.

את רוצה למצוא את בן הזוג המתאים לך, זה שתוכלי לסמוך עליו ולבנות איתו יחד בית יציב ומשפחה שמחה! התשובות נמצאות אצלך והדרך למציאת בן הזוג המתאים עבורך, מתחילה קודם כל בתוכך!

אז איך באמת, אפשר להצליח להקשיב לעצמי ולהבין מה טוב לי?!

ליווי אישי וכלים ברורים שיאפשרו לך להיפתח ולהקשיב לעצמך, לדייק ולגלות מה באמת נכון עבורך, איזה תכונות ומאפיינים באמת חשובים לך אצל בן הזוג, ועל מה את יכולה להתגמש. להבין מה מסתתר מאחורי "רשימת המכולת" מהי המשמעות העמוקה שמאחורי הרצונות והחלומות שלך. לגלות מי בן הזוג שמתאים לך, זה שתהיי מאושרת איתו ותוכלי לסמוך עליו, לבנות איתו בית ומשפחה.

בתום התהליך של צעדים מרווקות לזוגיות תחסכי מעצמך כאבי לב ואכזבות בחירות שגויות, פחדים ייעלמו, הביטחון שלך בעצמך יגדל, קשרים יתפתחו ויעמיקו, תקבלי יותר הצעות להיכרויות, כי מסביבך יבינו מה את רוצה. תהיי מאושרת להגיד כן, להתקדם הלאה ולהיפתח לזוגיות בריאה ונכונה.
```

- [ ] **Create `מתח/index.html`**

```html
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>מתח | טליה ברמן</title>
  <meta name="google-site-verification" content="wvSyn234b7e5W_VghEFBSNyeBVhaJnIsU5LGIBHM6LA">
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>
<nav class="site-nav">
  <div class="container">
    <a href="/" class="nav-logo"><img src="/images/logo.png" alt="טליה ברמן לוגו"></a>
    <ul class="nav-links">
      <li><a href="/">בית</a></li>
      <li><a href="/אודות-הדרך/">אודות</a></li>
      <li><a href="/אודות/">בנימה אישית</a></li>
      <li class="has-dropdown">
        <button class="dropdown-toggle" aria-expanded="false" aria-haspopup="true">ייעוץ ואימון ▾</button>
        <ul class="dropdown">
          <li><a href="/ייעוץ-אישי-עין-הבדולח/">ייעוץ אישי - עין הבדולח</a></li>
          <li><a href="/אימון-זוגי/">אימון זוגי</a></li>
          <li><a href="/מרווקות-לזוגיות/">מרווקות לזוגיות</a></li>
        </ul>
      </li>
    </ul>
  </div>
</nav>
<main class="container page-content">
  <h1>מתח</h1>
  <p>את לא לבד בעולם והכל בסדר איתך, את שלמה ואהובה בדיוק כמו שאת, חייך עשירים ומלאים במשפחה, עבודה, חברים, עיסוקים ועוד, הרצון בזוגיות והרצון לבנות את ביתך ומשפחתך ממלא את מחשבותייך ולפעמים גם את הכרית בדמעותייך אבל זה רק זמני!</p>
  <p>משפטים כמו: איך את עדיין רווקה, אולי את בררנית, אולי את לא יודעת לבחור נכון, את תמיד נעלבת, שוב פעם את עם בחור שלא מתאים לך, ועוד שלל משפטים, גורמים לך להרגיש פחות טובה וראויה, פחות אהובה ושלמה. הם מהווים מחסום ומחלישים אותך, מה שגורם לך להסתכל על המציאות מתוך חוסר ביטחון עצמי, פחד ותסכול, ביקורתיות וחוסר אמון.</p>
  <p>וזה גם לא תמיד קל להתמודד עם כל הרעשים והלחצים מהמשפחה והסביבה, שרוצים לתת עצות ולהשמיע את דעתם בעוד שקולך הפנימי הולך ונעלם, הקול הייחודי שיודע מה באמת טוב עבורך וייעשה אותך מאושרת.</p>
  <p>את רוצה למצוא את בן הזוג המתאים לך, זה שתוכלי לסמוך עליו ולבנות איתו יחד בית יציב ומשפחה שמחה! התשובות נמצאות אצלך והדרך למציאת בן הזוג המתאים עבורך, מתחילה קודם כל בתוכך!</p>
  <p>אז איך באמת, אפשר להצליח להקשיב לעצמי ולהבין מה טוב לי?!</p>
  <p>ליווי אישי וכלים ברורים שיאפשרו לך להיפתח ולהקשיב לעצמך, לדייק ולגלות מה באמת נכון עבורך, איזה תכונות ומאפיינים באמת חשובים לך אצל בן הזוג, ועל מה את יכולה להתגמש. להבין מה מסתתר מאחורי "רשימת המכולת" מהי המשמעות העמוקה שמאחורי הרצונות והחלומות שלך. לגלות מי בן הזוג שמתאים לך, זה שתהיי מאושרת איתו ותוכלי לסמוך עליו, לבנות איתו בית ומשפחה.</p>
  <p>בתום התהליך של צעדים מרווקות לזוגיות תחסכי מעצמך כאבי לב ואכזבות בחירות שגויות, פחדים ייעלמו, הביטחון שלך בעצמך יגדל, קשרים יתפתחו ויעמיקו, תקבלי יותר הצעות להיכרויות, כי מסביבך יבינו מה את רוצה. תהיי מאושרת להגיד כן, להתקדם הלאה ולהיפתח לזוגיות בריאה ונכונה.</p>
</main>
<footer class="site-footer">
  <div class="container">
    <div class="footer-contact">
      <span><a href="tel:052-3238867">052-3238867</a></span>
      <span><a href="mailto:t@ilact.com">t@ilact.com</a></span>
    </div>
    <p>טליה ברמן ייעוץ ואימון אישי זוגי | רמת השרון</p>
  </div>
</footer>
<script>
document.querySelectorAll('.dropdown-toggle').forEach(btn => {
  btn.addEventListener('click', () => {
    const li = btn.closest('.has-dropdown');
    const open = li.classList.toggle('open');
    btn.setAttribute('aria-expanded', open);
  });
});
</script>
</body>
</html>
```

- [ ] **Copy `מתח/index.html` to the other three pages, changing only the `<title>` and `<h1>`:**
  - `אחיזה/index.html` → title: `אחיזה | טליה ברמן`, h1: `אחיזה`
  - `יחסים/index.html` → title: `יחסים | טליה ברמן`, h1: `יחסים`
  - `עצמי/index.html` → title: `עצמי | טליה ברמן`, h1: `עצמי`

- [ ] **Verify all four pages at localhost**
- [ ] **Commit**
```bash
git add "מתח/" "אחיזה/" "יחסים/" "עצמי/"
git commit -m "feat: add four landing pages (מתח, אחיזה, יחסים, עצמי)"
```

---

## Task 13: CNAME File

**Files:**
- Create: `CNAME`

- [ ] **Create `CNAME`**

File must contain exactly one line with no trailing spaces:
```
taliaberman.com
```

- [ ] **Verify contents**
```powershell
Get-Content CNAME
```
Expected: `taliaberman.com`

- [ ] **Commit**
```bash
git add CNAME
git commit -m "feat: add CNAME for custom domain"
```

---

## Task 14: Push to GitHub and Enable Pages

- [ ] **Add GitHub remote**

```bash
git remote add origin https://github.com/ubar-on/taliaberman-website.git
```

- [ ] **Push to GitHub**

```bash
git push -u origin master
```

- [ ] **Enable GitHub Pages** (do this in the browser):
  - Go to `https://github.com/ubar-on/taliaberman-website/settings/pages`
  - Source: Deploy from a branch
  - Branch: `master`, folder: `/ (root)`
  - Click Save
  - Wait ~60 seconds, then visit `https://ubar-on.github.io/taliaberman-website/`

- [ ] **Verify the site at `https://ubar-on.github.io/taliaberman-website/`**

Note: some asset paths use absolute `/` roots which won't resolve correctly at the github.io subdirectory URL. That's expected — they'll work correctly once the custom domain is set. Verify the HTML is rendering at least (text, layout) and images will load correctly after DNS cutover.

---

## Task 15: DNS Cutover

Do this **only after** verifying the site looks correct at localhost and structure is confirmed on github.io.

- [ ] **At your domain registrar, update DNS for `taliaberman.com`:**

Remove existing Wix A records and add:
```
A  @  185.199.108.153
A  @  185.199.109.153
A  @  185.199.110.153
A  @  185.199.111.153
CNAME  www  ubar-on.github.io
```

- [ ] **Wait for DNS propagation (up to 24 hours, usually ~30 min)**

Check propagation at `https://dnschecker.org/#A/taliaberman.com`

- [ ] **Once DNS resolves, verify `https://www.taliaberman.com`:**
  - Home page loads with correct fonts, colors, images
  - All nav links work
  - Testimonials carousel auto-advances
  - Footer phone is a `tel:` link
  - שווה קריאה section is invisible
  - All 10 pages accessible at their Hebrew URLs
  - HTTPS (GitHub Pages provides it automatically after DNS propagation)
