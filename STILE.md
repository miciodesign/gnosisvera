# Guida per il commento quotidiano

Questa guida è usata dall'attività automatica che ogni mattina scrive il commento al Vangelo del giorno. Vale anche per chi scrive a mano.

## File

`content/vangelo/AAAA-MM-GG.md`, con intestazione:

```
---
title: Titolo breve ed evocativo (3-6 parole, non il riferimento biblico)
date: AAAA-MM-GG
pericope: Luca 13,18-21
liturgia: Martedì della XXX settimana del Tempo Ordinario   (o la festa/solennità)
summary: Una frase di sintesi che compare nelle anteprime.
---
```

Il Vangelo è quello del lezionario della Chiesa cattolica di rito romano (Italia). Verificare sempre con una ricerca web il brano del giorno e la celebrazione (feste e solennità sostituiscono la feria). Indicare anche la prima lettura nell'ultima sezione.

## Struttura (600-800 parole, più il testo)

0. **Il testo** — subito dopo l'intestazione, una sezione `## Il testo` con il brano evangelico intero in blockquote, **tradotto dal greco dall'autore stesso** (traduzione propria, letterale dove possibile, in italiano sobrio). Non copiare la CEI né altre traduzioni moderne: sono protette da diritto d'autore. Chiudere il blocco con la riga `> <small>Dal Vangelo secondo X (riferimento). Traduzione dal greco a cura del sito, letterale dove possibile.</small>`.
1. **Il contesto** — dove siamo nel Vangelo, cosa è appena successo, chi sono gli interlocutori.
2. **Una o due sezioni sul testo** — titolate con un'immagine o una parola chiave del brano. Almeno un termine greco traslitterato (e in caratteri greci tra parentesi) spiegato con cura; riferimenti all'Antico Testamento dove illuminano.
3. **I Padri** — una o due letture patristiche (Ambrogio, Agostino, Crisostomo, Cirillo, Beda, Gregorio Magno, Origene…), in parafrasi, senza citazioni lunghe.
4. **Per la vita** — applicazione concreta, non moralistica; una domanda o un esercizio; collegamento in una riga alla prima lettura.
5. **Preghiera finale** — una sola riga in corsivo, in blockquote, in prima persona.

## Tono

Sobrio, colto, caldo. Frasi non troppo lunghe. Niente retorica devozionale, niente esclamativi, niente "cari fratelli". Il lettore è un adulto che vuole capire, non essere esortato. Il testo biblico si parafrasa o si cita in brevi frammenti in corsivo, mai per esteso.

## Dopo aver scritto

`git add content/vangelo/AAAA-MM-GG.md && git commit && git push origin main`. Il sito si ricostruisce da solo.
