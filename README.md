# Giapponese C1 – Notifiche per imparare 8000 parole

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) · **v1.0.0**

Sistema che ti manda **notifiche push** sul telefono (e su Mac) con **vocaboli giapponesi** e curiosità. L’obiettivo è imparare **8000 parole** nel tempo, senza stare seduto a studiare: le notifiche arrivano da sole in momenti casuali e ti espongono alle parole in modo ripetuto (spaced repetition).

Se non hai mai usato GitHub, Python o ntfy: questo README spiega tutto da zero.

---

## Cosa fa questo progetto (in parole semplici)

- **Ricevi notifiche** sul telefono (e su computer) con parole giapponesi: kanji, lettura, significato, esempio.
- Le notifiche arrivano **in automatico** in orari casuali (circa ogni 5–10 minuti), **dalle 6:00 alle 2:00** (ora italiana), così le vedi durante la giornata senza dover aprire un’app.
- Il sistema è pensato per **8000 parole** divise in **blocchi da 50**: ogni settimana “sblocchi” un blocco nuovo e ripassi una parte delle parole già viste (spaced repetition).
- Può girare **sul tuo PC** oppure **su GitHub** (in cloud): se lo attivi su GitHub, le notifiche continuano anche con il PC spento.

Non devi essere esperto di programmazione: basta seguire i passi sotto.

---

## Cosa ti serve

1. **Un telefono** (iPhone o Android) e/o **un Mac** (le notifiche possono arrivare su entrambi, vedi sotto).
2. **L’app ntfy** (gratuita) per ricevere le notifiche.  
   - **iPhone/Android**: App Store o Google Play.  
   - **MacBook**: stessa app ntfy (App Store su Mac) oppure da [ntfy.sh](https://ntfy.sh) — apri l’app, iscriviti allo **stesso topic** che usi sul telefono: le notifiche (con la stessa icona personalizzata) compaiono anche su Mac.  
   - ntfy è un servizio push: ti “iscrivi” a un **topic** (un nome segreto) e il progetto invia le parole a quel topic; tutti i dispositivi iscritti ricevono la notifica.
3. **Un account GitHub** (gratuito) se vuoi che le notifiche partano **anche a PC spento**. Se vuoi solo provare sul PC, GitHub non è obbligatorio.
4. **Python 3** sul computer solo se vuoi far girare il progetto in locale (vedi sotto).

---

## Tipi di notifiche

Ogni notifica è **una sola** di queste tre cose (mai tutto insieme, così resta breve):

| Tipo | Cosa vedi | A cosa serve |
|------|-----------|--------------|
| **Parola del momento** | Kanji, lettura (hiragana), romaji, significato in italiano, esempio con traduzione. | È la notifica principale per **imparare** la parola. |
| **Curiosità** | Stessa parola (kanji + lettura + romaji) + una frase breve su origine, uso o aneddoto (generata con AI). | Per dare contesto e rendere la parola più memorabile. |
| **Ora del vocabolario Gen Z** | Frasi slang giapponese (tipo 草, とりま, エモい) con spiegazione breve. | Variante divertente, ogni tanto. |

La maggior parte delle notifiche sono **Parola del momento** (per imparare); meno spesso **Curiosità** e **Gen Z**.

---

## Come funziona il “piano” delle 8000 parole

- Le parole sono organizzate in **160 blocchi** da **50 parole** → 160 × 50 = **8000 parole**.
- **Ogni settimana** il sistema considera “attivo” **un blocco** (50 parole nuove) + circa **20% del pool** preso da blocchi precedenti (ripasso).
- Così in una settimana vedi soprattutto le 50 parole del blocco corrente, ma ti riappaiono anche parole già viste (spaced repetition).
- Settimana dopo settimana avanzi di blocco: nel tempo copri tutte le 8000 parole e le rivedi più volte.

Non devi fare nulla tu: il programma sceglie quale parola mandare in base al blocco della settimana e al ripasso.

---

## Due modi per usarlo

### A) Solo sul tuo PC (per provare)

Le notifiche partono **solo quando il tuo computer è acceso** e sta eseguendo il programma.

1. Installa **Python 3** (da [python.org](https://www.python.org/downloads/) o con `brew install python3` su Mac).
2. Nella cartella del progetto crea un file `.env` (puoi copiare `.env.example`) e scrivi dentro:
   ```bash
   NTFY_TOPIC=un_nome_segreto_a_tua_scelta
   ```
   Sostituisci `un_nome_segreto_a_tua_scelta` con un nome che userai anche nell’app ntfy (es. `mio_giapponese_8000`). Non usare spazi.
3. Sul telefono apri **ntfy**, iscriviti allo **stesso topic** (es. `mio_giapponese_8000`).
4. Nel terminale, dalla cartella del progetto:
   ```bash
   pip3 install -r requirements.txt
   python3 main.py
   ```
   Se sei nell’orario 06:00–02:00 (ora italiana), può partire subito una notifica. Per inviarne una subito a comando:
   ```bash
   FORCE_INVIO=1 python3 main.py
   ```

Per far girare il controllo ogni 5 minuti in automatico (sempre con PC acceso) vedi **AVVIO_AUTOMATICO.md**.

---

### B) Su GitHub (notifiche anche a PC spento) – consigliato

Le notifiche le invia **GitHub** ogni 5 minuti. Puoi chiudere il PC e spegnere tutto: continuano ad arrivare dalle 6:00 alle 2:00 (ora italiana).

1. **Crea un repository su GitHub**  
   - Vai su [github.com/new](https://github.com/new).  
   - Scegli un nome (es. `jpnotify`), repo **Private** o Public.  
   - **Non** aggiungere README o altro. Clicca **Create repository**.

2. **Aggiungi i “secret”** (dati che solo GitHub userà, non visibili a nessuno)  
   - Nel repo: **Settings** → **Secrets and variables** → **Actions**.  
   - **New repository secret**.  
   - Nome: `NTFY_TOPIC`  
   - Valore: il **topic** a cui sei iscritto nell’app ntfy (es. `mio_giapponese_8000`).  
   - Salva.  
   - (Opzionale) Aggiungi un altro secret `ICONA_NOTIFICA_URL` con l’URL pubblico di un’immagine (PNG/JPG) se vuoi un’icona personalizzata per le notifiche.

3. **Carica il progetto su GitHub**  
   - Nel terminale, dalla cartella del progetto:
   ```bash
   git remote add origin https://github.com/TUO_USERNAME/TUO_REPO.git
   git branch -M main
   git push -u origin main
   ```
   Sostituisci `TUO_USERNAME` e `TUO_REPO` con i tuoi (es. `mionome` e `jpnotify`). Se ti chiede login, usa le tue credenziali GitHub.

4. **Verifica**  
   - Nel repo vai in **Actions**. Dovresti vedere il workflow “Invia notifica vocabolario” che parte ogni 5 minuti.  
   - Per una prova immediata: **Run workflow** → spunta **“Invia subito (test)”** → **Run workflow**. Controlla che sul telefono arrivi una notifica.

Da quel momento le notifiche partono da GitHub: puoi chiudere Cursor e spegnere il PC.

Per i dettagli passo-passo vedi **GITHUB_SETUP.md**.

---

## Struttura del progetto (per chi vuole capire o modificare)

```
.
├── main.py              # Punto di ingresso: controlla se è ora di inviare, sceglie parola/tipo, invia, aggiorna stato
├── config.py            # Tutta la configurazione (orari, percorsi, topic, icona, blocchi, ripasso)
├── requirements.txt     # Dipendenze Python (requests, python-dotenv, google-generativeai)
├── .env.example         # Esempio di .env (topic, icona, chiave Gemini). Copia in .env e compila
├── .env                 # I tuoi dati (topic, ecc.) – non va su GitHub (è in .gitignore)
│
├── data/
│   ├── vocabolario.json       # Le 8000 parole (o quante ne hai): kanji, lettura, significato, esempio, curiosità, blocco
│   ├── vocabolario_genz.json  # Frasi slang Gen Z per le notifiche "Ora del vocabolario Gen Z"
│   ├── prossimo_invio.txt     # Timestamp del prossimo invio (usato dal programma)
│   └── log.txt                # Log degli invii (opzionale)
│
├── logic/
│   └── selezionatore.py  # Carica vocabolario, calcola blocco settimana, costruisce pool, sceglie parola, aggiorna contatori
│
├── sender/
│   └── notifica.py       # Formatta il messaggio (parola / curiosità / Gen Z) e lo invia a ntfy
│
├── scripts/
│   ├── genera_vocabolario_8000.py  # Genera data/vocabolario.json con 8000 parole da JLPT N1-N5 (open-anki-jlpt-decks)
│   ├── arricchisci_curiosita.py    # Aggiunge "curiosità" alle voci con Gemini (GEMINI_API_KEY)
│   ├── avvia_invio_continuo.sh    # Lancia main.py ogni 5 min in locale (PC acceso)
│   └── avvia_invio_continuo_nohup.sh  # Come sopra, in background
│
├── .github/workflows/
│   └── invia-notifica.yml  # Workflow GitHub: ogni 5 min esegue main.py, poi fa commit dello stato
│
├── assets/
│   └── icona_notifica.png  # Icona usata per le notifiche (puoi sostituirla o usare un URL in ICONA_NOTIFICA_URL)
│
├── README.md             # Questo file
├── GITHUB_SETUP.md       # Guida dettagliata per attivare le notifiche su GitHub
└── AVVIO_AUTOMATICO.md   # Come far girare il sistema in locale (script, cron, nohup)
```

- **main.py** legge la config, controlla se è nell’orario 06:00–02:00 e se è ora di inviare (intervallo 5–10 min), carica il vocabolario, sceglie il tipo (parola / curiosità / Gen Z) e la parola (o la voce Gen Z), formatta, invia la notifica a ntfy e aggiorna file e contatori.
- **config.py** definisce topic, icona, orari, fuso orario, numero di blocchi, parole per blocco, percentuale di ripasso, ecc. Per cambiare orari o parametri si modifica lì.
- **logic/selezionatore.py** gestisce blocchi, pool attivo e spaced repetition (quale parola mandare e quando).
- **sender/notifica.py** costruisce titolo e corpo del messaggio e fa la richiesta HTTP a ntfy.
- Il **workflow** su GitHub esegue periodicamente `main.py` e fa commit di `vocabolario.json`, `prossimo_invio.txt` e `log.txt` così lo stato resta sincronizzato.

---

## Personalizzazione

- **Topic ntfy**  
  In `.env` (locale) o nel secret `NTFY_TOPIC` (GitHub): il nome del “canale” a cui sei iscritto nell’app ntfy. Deve essere uguale su tutti i dispositivi (iPhone, MacBook, ecc.).

- **Icona / miniatura delle notifiche (al posto di quella standard ntfy)**  
  In `.env` o nel secret `ICONA_NOTIFICA_URL`: metti l’**URL pubblico** di un’immagine (PNG/JPG). Quella immagine viene usata come miniatura della notifica **su iPhone e su MacBook** (e ovunque tu abbia ntfy aperto con quel topic). Se non lo imposti, si usa l’icona predefinita del repo (`assets/icona_notifica.png`). Es.: URL raw su GitHub, o link da Imgur.

- **Orari**  
  In `config.py`: `ORA_INIZIO` e `ORA_FINE`. Di default: 06:00–02:00 (ora italiana). La finestra “attraversa” la mezzanotte (da 6 del mattino alle 2 di notte).

- **Vocabolario e curiosità**  
  Le parole stanno in `data/vocabolario.json`. Per aggiungere “curiosità” alle voci puoi usare lo script `scripts/arricchisci_curiosita.py` (serve una chiave API Gemini in `GEMINI_API_KEY` nel `.env`). Vedi i commenti nello script.

---

## Domande frequenti

**Le notifiche non arrivano.**  
- Controlla di essere iscritto al **topic giusto** nell’app ntfy (stesso nome che hai messo in `NTFY_TOPIC`).  
- Se usi GitHub: in **Actions** → ultimo run → step “Esegui main”: verifica che ci sia “Topic ntfy impostato: si” e che l’exit code di `main.py` sia 0 quando invia.  
- Le notifiche partono solo tra **06:00 e 02:00** (ora italiana). Per un test immediato: `FORCE_INVIO=1 python3 main.py` (locale) oppure **Run workflow** con “Invia subito (test)” (GitHub).

**Posso usare solo il telefono?**  
Sì. Basta installare ntfy, iscriversi al topic e (se vuoi notifiche a PC spento) configurare GitHub come in **GITHUB_SETUP.md**. Non serve tenere aperto il PC.

**Come faccio comparire le notifiche anche su MacBook?**  
Installa l’app ntfy su Mac (App Store o da ntfy.sh), aprila e iscriviti allo **stesso topic** che usi sull’iPhone. Le notifiche (con la stessa icona personalizzata, non quella standard ntfy) arrivano su tutti i dispositivi iscritti.

**Da dove vengono le 8000 parole?**  
Il file `data/vocabolario.json` è generato con **scripts/genera_vocabolario_8000.py**: scarica i vocaboli JLPT N1–N5 dal progetto [open-anki-jlpt-decks](https://github.com/jamsinclair/open-anki-jlpt-decks), li converte nel formato dell’app (con romaji) e produce 8000 voci in 160 blocchi. I **significati** sono in inglese (fonte originale); puoi lasciarli così o tradurli. Lo script **arricchisci_curiosita.py** aggiunge il campo “curiosità” in italiano con Gemini.

**Vedo sempre le stesse parole e troppo poco spesso.**  
Se nel vocabolario hai poche voci (es. 5–10), è normale che si ripetano: il sistema sceglie dal pool del blocco. Aggiungi più parole a `data/vocabolario.json` (stesso schema delle esistenti) per avere più varietà. Le notifiche sono state rese più frequenti (circa ogni 3–6 minuti invece di 5–10); in `config.py` puoi modificare `INTERVALLO_MIN_MINUTI` e `INTERVALLO_MAX_MINUTI` per regolare ancora.

**Cosa significa “spaced repetition” qui?**  
Il sistema non è un’app tipo Anki: ogni settimana ha un blocco “nuovo” (50 parole) e ripropone una parte delle parole dei blocchi precedenti (20% del pool). Così le parole ti riappaiono nel tempo senza che tu debba schedulare le ripetizioni a mano.

---

## Riepilogo per chi non ne sa niente

1. **Scarica ntfy** sul telefono e iscriviti a un **topic** (un nome segreto).
2. **Decidi** se vuoi solo provare sul PC (segui “A) Solo sul tuo PC”) o avere notifiche sempre (segui “B) Su GitHub” e **GITHUB_SETUP.md**).
3. **Imposta** `NTFY_TOPIC` (e se vuoi `ICONA_NOTIFICA_URL`) nel `.env` o nei secret di GitHub.
4. Da lì in poi ricevi notifiche con parole giapponesi (e curiosità / Gen Z) in orari casuali tra le 6 e le 2 di notte, e nel tempo il sistema copre 8000 parole con ripasso automatico.

Se qualcosa non torna, controlla **GITHUB_SETUP.md** (per il cloud) e **AVVIO_AUTOMATICO.md** (per l’avvio in locale).

---

## Requisiti tecnici

- **Python** 3.9+ (per esecuzione in locale).
- **Dipendenze**: `requests`, `python-dotenv`; opzionale `google-generativeai` per lo script curiosità (vedi `requirements.txt`).
- **ntfy**: servizio pubblico [ntfy.sh](https://ntfy.sh); nessun account obbligatorio, solo il topic.

---

## Licenza

Questo progetto è rilasciato sotto licenza **MIT**. Vedi [LICENSE](LICENSE).
