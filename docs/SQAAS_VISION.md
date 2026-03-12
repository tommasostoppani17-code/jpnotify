# SQaaS – Side Quest as a Service (visione prodotto)

Micro-SaaS iper-focalizzato: notifiche passive di vocaboli giapponesi senza aprire app. Per livelli avanzati (C1/N1) che non hanno tempo per studio attivo.

---

## 1. Modello di business (subscription)

- **Tier Base**: ~10 notifiche/giorno, livello N3/N2.
- **Tier Extreme (C1/N1)**: 20+ notifiche/giorno, curiosita generate da Gemini, frasi business/letterario.
- **Tier Custom**: l’utente carica il suo file di parole (es. da un libro) e il sistema inizia a bombardarlo.

---

## 2. Architettura scalabile (multi-utente)

- **Database centrale**: PostgreSQL o MongoDB – utenti, topic ntfy, livello, parole gia’ viste, prossimo invio per utente.
- **Dashboard web**: pagina minimale: inserimento ntfy topic (o generazione topic casuale), scelta livello/intensita (notifiche/giorno).
- **Cron unico**: uno script che gira ogni minuto (o ogni 5 min), controlla chi deve ricevere una notifica in quel momento e invia via ntfy. Niente uno script per utente.

---

## 3. Punti di forza per il marketing

- **Zero friction**: “Impara il C1 mentre guardi l’ora. Niente app da aprire, niente esercizi.”
- **Contenuto curato**: “8000 parole N1, arricchite da AI con curiosita etimologiche.”
- **Anti-oblio**: “Ripetizione spaziata invisibile.”

---

## 4. Aspetti critici

- **Privacy ntfy**: topic univoco per utente (es. generato: `user_823_jp_72`) per evitare che altri leggano le notifiche.
- **Costi API**: Gemini 1.5 Flash per curiosita – batch di generazione per migliaia di parole/utenti; gestire limiti e cache (curiosita generate una volta, riusate).
- **Legale**: termini di servizio, privacy policy, gestione dati (topic, preferenze).

---

## 5. Stato attuale vs SQaaS

| Oggi (script singolo) | SQaaS (futuro) |
|------------------------|----------------|
| Un vocabolario JSON, un topic | DB utenti + parole per utente |
| main.py + cron locale / GitHub Actions | Cron unico + query “chi deve ricevere ora?” |
| Curiosita in batch su file locale | Curiosita in batch per livello, cache per parola |
| Nessuna UI | Dashboard minimale (topic, intensita) |

Questo progetto resta lo script single-user; il documento serve da blueprint per una versione “Side Quest” vendibile (minima UI, massima logica).
