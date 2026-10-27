# Gnosis Vera

Sito statico con il commento quotidiano al Vangelo e studi di filosofia, mistica ed esegesi.

## Come funziona

- I contenuti sono file Markdown in `content/`.
- `build.py` li trasforma in HTML dentro `site/` (richiede Python 3 e `pip install markdown`).
- Su GitHub, ogni `push` sul ramo `main` ricostruisce e pubblica automaticamente il sito (`.github/workflows/deploy.yml`).

```
content/
  vangelo/2026-10-27.md        ← un file per giorno
  studi/filosofia/*.md
  studi/mistica/*.md
  studi/esegesi/*.md
  chi-siamo.md
static/style.css
build.py
```

Ogni file inizia con un'intestazione:

```
---
title: Il seme e il lievito
date: 2026-10-27
pericope: Luca 13,18-21            (solo per il vangelo)
liturgia: Martedì della XXX settimana del Tempo Ordinario
summary: una riga che appare nelle anteprime
---
```

## Pubblicare su GitHub Pages (una volta sola)

1. Crea un repository su GitHub (es. `gnosis-vera`) e carica questi file sul ramo `main`.
2. Nel repository: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
3. Al primo push il sito sarà raggiungibile a `https://TUO-UTENTE.github.io/gnosis-vera/ e, una volta impostato il DNS, a https://gnosisvera.it`.
4. Per il dominio proprio: **Settings → Pages → Custom domain**, inserisci il dominio e aggiungi presso il tuo registrar un record `CNAME` che punta a `TUO-UTENTE.github.io` (o i record `A` di GitHub per il dominio nudo). Attiva poi **Enforce HTTPS**.

In alternativa funziona anche su Netlify o Cloudflare Pages: comando di build `pip install markdown && python3 build.py`, cartella di pubblicazione `site`.

## Aggiornamento quotidiano automatico

Un'attività programmata di Claude ogni mattina scrive `content/vangelo/AAAA-MM-GG.md` con il commento al Vangelo del giorno e lo invia al repository; GitHub Actions fa il resto. Per attivarla serve che Claude abbia accesso al repository (Settings → Connectors → GitHub su claude.ai).

## Anteprima locale

```
pip install markdown
python3 build.py
python3 -m http.server -d site 8000
```

poi apri http://localhost:8000.
