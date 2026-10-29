#!/usr/bin/env python3
"""
Gnosis Vera — generatore di sito statico.

Legge i file Markdown in content/ e produce HTML in site/.
Nessun framework: solo Python 3 e il pacchetto `markdown`.

    python3 build.py

Struttura dei contenuti:
    content/vangelo/YYYY-MM-DD.md         commento quotidiano
    content/studi/filosofia/*.md          studi filosofici
    content/studi/mistica/*.md            studi mistici
    content/studi/esegesi/*.md            esegesi e greco

Ogni file inizia con un'intestazione YAML minimale:
    ---
    title: Titolo
    date: 2026-10-27
    pericope: Lc 13,18-21          (solo vangelo)
    liturgia: Martedì XXX T.O.     (solo vangelo)
    summary: una riga di sintesi
    ---
"""
import os, re, shutil, datetime, html
from pathlib import Path
import markdown

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
STATIC = ROOT / "static"
OUT = ROOT / "site"
SITE_NAME = "Gnosis Vera"
SITE_URL = "https://gnosisvera.it"
TAGLINE = "La vera conoscenza del Vangelo: ogni giorno, con i Padri, i filosofi e i mistici"

SECTIONS = {
    "filosofia": ("Filosofia e Vangelo", "Quando il pensiero interroga la Parola: Agostino, Tommaso, Pascal, Kierkegaard, la fenomenologia."),
    "mistica":   ("Mistica", "La Parola vissuta nell'esperienza di Dio: Padri del deserto, Eckhart, Giovanni della Croce, Teresa d'Avila."),
    "esegesi":   ("Esegesi e greco", "Il testo da vicino: parole chiave, contesto storico, struttura letteraria."),
}

MESI = ["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio",
        "agosto","settembre","ottobre","novembre","dicembre"]
GIORNI = ["lunedì","martedì","mercoledì","giovedì","venerdì","sabato","domenica"]

def data_it(d: datetime.date, weekday=True) -> str:
    s = f"{d.day} {MESI[d.month-1]} {d.year}"
    return f"{GIORNI[d.weekday()]} {s}" if weekday else s

# ---------- lettura Markdown con frontmatter ----------
def parse(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    meta = {}
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
        text = text[m.end():]
    md = markdown.Markdown(extensions=["footnotes", "smarty", "tables", "attr_list"])
    meta["html"] = md.convert(text)
    meta["slug"] = path.stem
    if "date" in meta:
        meta["date_obj"] = datetime.date.fromisoformat(meta["date"])
    return meta

# ---------- template ----------
def page(title, body, depth=0, description="", rel="", article=None, noindex=False):
    base = "../" * depth
    canonical = f"{SITE_URL}/{rel}" if rel != "index.html" else f"{SITE_URL}/"
    ld = ""
    if article:
        import json
        ld = "<script type=\"application/ld+json\">" + json.dumps({
            "@context": "https://schema.org", "@type": "Article",
            "headline": article["title"], "description": description,
            "datePublished": article.get("date", ""), "inLanguage": "it",
            "author": {"@type": "Organization", "name": SITE_NAME},
            "publisher": {"@type": "Organization", "name": SITE_NAME, "url": SITE_URL},
            "mainEntityOfPage": canonical,
        }, ensure_ascii=False) + "</script>"
    robots = '<meta name="robots" content="noindex">' if noindex else ""
    nav = f"""
<header class="top">
  <a class="brand" href="{base}index.html"><img src="{base}static/logo.svg" alt="" class="logo">{SITE_NAME}</a>
  <nav>
    <a href="{base}index.html">Oggi</a>
    <a href="{base}vangelo/index.html">Archivio</a>
    <a href="{base}studi/filosofia/index.html">Filosofia</a>
    <a href="{base}studi/mistica/index.html">Mistica</a>
    <a href="{base}studi/esegesi/index.html">Esegesi</a>
    <a href="{base}chi-siamo.html">Il sito</a>
  </nav>
</header>"""
    return f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} · {SITE_NAME}</title>
<meta name="description" content="{html.escape(description or TAGLINE)}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" type="application/rss+xml" title="{SITE_NAME}" href="{SITE_URL}/feed.xml">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:type" content="{'article' if article else 'website'}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description or TAGLINE)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="it_IT">
{robots}
{ld}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">
<link rel="icon" type="image/svg+xml" href="{base}static/favicon.svg">
<link rel="stylesheet" href="{base}static/style.css">
</head>
<body>
{nav}
<main>
{body}
</main>
<footer>
  <p>{SITE_NAME} · {html.escape(TAGLINE)} · <a href="{base}feed.xml">Feed RSS</a></p>
  <p class="small">I testi biblici sono citati o parafrasati per lo studio. Generato il {data_it(datetime.date.today(), False)}.</p>
</footer>
</body>
</html>"""

def card(href, kicker, title, summary):
    return f"""<a class="card" href="{href}">
  <span class="kicker">{html.escape(kicker)}</span>
  <h3>{html.escape(title)}</h3>
  <p>{html.escape(summary)}</p>
</a>"""

def write(rel, content):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")

# ---------- build ----------
def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(STATIC, OUT / "static")
    # file che devono stare nella radice del sito (verifiche Google ecc.)
    for f in (OUT / "static").glob("google*.html"):
        shutil.move(f, OUT / f.name)

    # --- commenti quotidiani ---
    # I commenti con data futura vengono generati (per avere le pagine pronte)
    # ma non compaiono in home né in archivio finché non è il loro giorno.
    # Variabile d'ambiente BUILD_DATE=AAAA-MM-GG per forzare "oggi".
    oggi = datetime.date.fromisoformat(os.environ["BUILD_DATE"]) if os.environ.get("BUILD_DATE") else datetime.date.today()
    tutti = sorted((parse(p) for p in (CONTENT / "vangelo").glob("*.md")),
                   key=lambda m: m["date_obj"], reverse=True)
    vangeli = [v for v in tutti if v["date_obj"] <= oggi]
    for v in tutti:
        body = f"""<article class="post">
  <p class="kicker">{html.escape(v.get('liturgia',''))} · {data_it(v['date_obj'])}</p>
  <h1>{html.escape(v['title'])}</h1>
  <p class="pericope">{html.escape(v.get('pericope',''))}</p>
  {v['html']}
</article>
<p class="back"><a href="index.html">← Tutti i commenti</a></p>"""
        write(f"vangelo/{v['slug']}.html", page(v["title"], body, 1, v.get("summary",""), rel=f"vangelo/{v['slug']}.html", article=v, noindex=v["date_obj"] > oggi))

    cards = "\n".join(card(f"{v['slug']}.html", f"{data_it(v['date_obj'])} · {v.get('pericope','')}",
                           v["title"], v.get("summary","")) for v in vangeli)
    write("vangelo/index.html", page("Archivio dei commenti",
          f"<h1>Il Vangelo giorno per giorno</h1><div class='grid'>{cards}</div>", 1, rel="vangelo/index.html"))

    # --- studi ---
    all_studi = {}
    for key, (name, desc) in SECTIONS.items():
        studi = sorted((parse(p) for p in (CONTENT / "studi" / key).glob("*.md")),
                       key=lambda m: m.get("date_obj", datetime.date.min), reverse=True)
        all_studi[key] = studi
        for s in studi:
            body = f"""<article class="post">
  <p class="kicker">{html.escape(name)}{' · ' + data_it(s['date_obj'], False) if 'date_obj' in s else ''}</p>
  <h1>{html.escape(s['title'])}</h1>
  {s['html']}
</article>
<p class="back"><a href="index.html">← {html.escape(name)}</a></p>"""
            write(f"studi/{key}/{s['slug']}.html", page(s["title"], body, 2, s.get("summary",""), rel=f"studi/{key}/{s['slug']}.html", article=s))
        cards = "\n".join(card(f"{s['slug']}.html", name, s["title"], s.get("summary","")) for s in studi)
        write(f"studi/{key}/index.html", page(name,
              f"<h1>{html.escape(name)}</h1><p class='lede'>{html.escape(desc)}</p><div class='grid'>{cards}</div>", 2, desc, rel=f"studi/{key}/index.html"))

    # --- home: commento di oggi (o il più recente) + ultimi studi ---
    today = vangeli[0] if vangeli else None
    recent = []
    for key, studi in all_studi.items():
        for s in studi[:2]:
            recent.append(card(f"studi/{key}/{s['slug']}.html", SECTIONS[key][0], s["title"], s.get("summary","")))
    home = f"""<section class="hero">
  <p class="kicker">{html.escape(TAGLINE)}</p>
</section>"""
    if today:
        home += f"""<article class="post featured">
  <p class="kicker">{html.escape(today.get('liturgia',''))} · {data_it(today['date_obj'])}</p>
  <h1>{html.escape(today['title'])}</h1>
  <p class="pericope">{html.escape(today.get('pericope',''))}</p>
  {today['html']}
</article>"""
    if len(vangeli) > 1:
        prev = "\n".join(card(f"vangelo/{v['slug']}.html", f"{data_it(v['date_obj'])} · {v.get('pericope','')}",
                              v["title"], v.get("summary","")) for v in vangeli[1:4])
        home += f"<h2>Giorni precedenti</h2><div class='grid'>{prev}</div>"
    home += f"<h2>Studi</h2><div class='grid'>{''.join(recent)}</div>"
    write("index.html", page("Oggi", home, 0, rel="index.html"))

    # --- pagina del sito ---
    chi = (CONTENT / "chi-siamo.md")
    if chi.exists():
        c = parse(chi)
        write("chi-siamo.html", page(c["title"], f"<article class='post'><h1>{html.escape(c['title'])}</h1>{c['html']}</article>", 0, rel="chi-siamo.html"))

    # --- sitemap, robots, feed RSS ---
    urls = [("", oggi), ("vangelo/index.html", oggi), ("chi-siamo.html", None)]
    urls += [(f"vangelo/{v['slug']}.html", v["date_obj"]) for v in vangeli]
    for key, studi in all_studi.items():
        urls.append((f"studi/{key}/index.html", None))
        urls += [(f"studi/{key}/{st['slug']}.html", st.get("date_obj")) for st in studi]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, d in urls:
        sm.append(f"  <url><loc>{SITE_URL}/{u}</loc>" + (f"<lastmod>{d.isoformat()}</lastmod>" if d else "") + "</url>")
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm))
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")

    import email.utils, time
    def rfc(d): return email.utils.format_datetime(datetime.datetime(d.year, d.month, d.day, 5, 0, tzinfo=datetime.timezone.utc))
    items = []
    for v in vangeli[:30]:
        items.append(f"""  <item>
    <title>{html.escape(v['title'])} · {html.escape(v.get('pericope',''))}</title>
    <link>{SITE_URL}/vangelo/{v['slug']}.html</link>
    <guid>{SITE_URL}/vangelo/{v['slug']}.html</guid>
    <pubDate>{rfc(v['date_obj'])}</pubDate>
    <description>{html.escape(v.get('summary',''))}</description>
    <content:encoded><![CDATA[{v['html']}]]></content:encoded>
  </item>""")
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>{SITE_NAME}</title>
  <link>{SITE_URL}/</link>
  <atom:link href="{SITE_URL}/feed.xml" rel="self" type="application/rss+xml"/>
  <description>{html.escape(TAGLINE)}</description>
  <language>it</language>
{chr(10).join(items)}
</channel>
</rss>"""
    write("feed.xml", feed)

    print(f"Generati {len(vangeli)} commenti e {sum(len(s) for s in all_studi.values())} studi in {OUT}")

if __name__ == "__main__":
    build()
