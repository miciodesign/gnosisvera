# Schede di lettura (una al mese)

Cartella: `content/letture/<slug>.md`. Copiare il formato di una scheda esistente (es. `eckhart-sermoni-tedeschi.md`).

Frontmatter: `title`, `autore`, `categoria` (una tra: Per cominciare, Padri e filosofia, Mistica — per una nuova categoria aggiungerla a `LETTURE_CATEGORIE` in build.py), `ordine` (numero successivo all'ultimo), `summary` (una frase), `edizione`, e `isbn` o `cerca`.

Sezioni: Perché leggerlo · Per chi è · Come leggerlo · Il nostro giudizio. Circa 250–350 parole. Link ai nostri studi collegati con percorso relativo (`../studi/...`).

## Regole di verità
- Prima di scrivere, VERIFICARE con ricerca web editore, collana, anno, curatore/traduttore dell'edizione italiana. Ciò che non si verifica si omette (niente traduttori o ISBN a memoria).
- Nessuna citazione dal libro, nessun numero di pagina del testo, nessuna copertina.
- Link Amazon: aggiungere nel frontmatter `isbn:` (solo se verificato) oppure `cerca:` (titolo e autore); build.py genera il link di affiliazione (tag gnosisvera-21) e la dichiarazione. Non scrivere link a mano e non cambiare il tono per vendere: il giudizio resta onesto (dire anche i limiti del libro).
- Libri con edizione italiana oggi reperibile.

## Candidati (verificare ogni volta)
Teresa d'Avila, *Castello interiore* · Gregorio di Nissa, *Vita di Mosè* · Pseudo-Dionigi, *Teologia mistica* · Detti dei Padri del deserto · Origene, *Omelie* · Tommaso d'Aquino (un'antologia) · Simone Weil, *Attesa di Dio* · Giovanni della Croce, *Salita del Monte Carmelo* · una grammatica o un lessico del greco del NT.

## Fatte
Nuovo Testamento greco-latino-italiano · Agostino, Confessioni · Clemente, Stromati · Kierkegaard, Timore e tremore · Eckhart, Sermoni tedeschi · Giovanni della Croce, Notte oscura · Pascal, Pensieri.
