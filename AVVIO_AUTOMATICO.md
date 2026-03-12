# Come ricevere le notifiche in automatico

Le notifiche **non partono da sole**: qualcosa deve eseguire `main.py` a intervalli regolari.  
Curiosita generate con Gemini. Icona: vedi sotto (GitHub + `ICONA_NOTIFICA_URL`).

**Per non fermarsi mai**  
- **Chiudi il terminale ma tieni il Mac acceso**: usa **Opzione 1b** (nohup in background).  
- **Spegni il Mac**: usa **Opzione 3** (GitHub Actions in cloud).

---

## Opzione 1a: Mac acceso – script in loop (terminale aperto)

Apri il terminale nella cartella del progetto ed esegui:

```bash
cd "/Users/tommaso/Desktop/Spaced Repetition"
chmod +x scripts/avvia_invio_continuo.sh
./scripts/avvia_invio_continuo.sh
```

Lo script lancia `main.py` ogni 5 minuti. Circa 1-2 notifiche ogni 10 min. Tieni il terminale aperto (Ctrl+C per fermare). Finestra 08:00-23:00 (ora italiana).

---

## Opzione 1b: Mac acceso – in background (chiudi pure il terminale)

Se vuoi che **non si fermi quando chiudi il terminale** (il Mac resta acceso):

```bash
cd "/Users/tommaso/Desktop/Spaced Repetition"
chmod +x scripts/avvia_invio_continuo_nohup.sh
./scripts/avvia_invio_continuo_nohup.sh
```

Il processo gira in background; il log va in `data/invio_continuo.log`. Per fermarlo: `pkill -f "python3 main.py"` (o chiudi il Mac).

---

## Opzione 2: Mac acceso – cron (sempre in background)

Esegui `crontab -e` e aggiungi (adatta il percorso se serve):

```bash
*/5 * * * * cd "/Users/tommaso/Desktop/Spaced Repetition" && /usr/bin/python3 main.py
```

Salva e esci. Ogni 5 minuti il sistema esegue `main.py`; le notifiche partono solo se il Mac è acceso e sveglio (finestra 08:00-23:00).

---

## Opzione 3: Computer spento – GitHub Actions (cloud)

Le notifiche partono anche a Mac spento, da GitHub.

1. Crea un repository su GitHub (anche privato) e carica questo progetto.
2. Nel repo: **Settings → Secrets and variables → Actions**. Aggiungi un secret:
   - Nome: `NTFY_TOPIC`  
   - Valore: il tuo topic ntfy (es. `mio_giapponese_extreme_8000`).
3. Il workflow in `.github/workflows/invia-notifica.yml` è già configurato: parte **ogni 5 minuti**, esegue `main.py` e fa commit dello stato (vocabolario, prossimo invio, log). Circa 1–2 notifiche ogni 10 min, tra 08:00 e 23:00 (Europe/Rome).

Non serve fare altro: le notifiche arrivano a orari irregolari. Per l’icona personalizzata imposta anche il secret `ICONA_NOTIFICA_URL` (URL raw di `assets/icona_notifica.png` su GitHub).

---

## Verifica

- Controlla che nell’app ntfy sull’iPhone sei iscritto allo **stesso topic** usato dallo script (in `config.py` o in `.env`: `NTFY_TOPIC`).
- Per una prova immediata: dalla cartella del progetto esegui `python3 main.py`. Se sei nella fascia oraria 08:00–23:00, parte una notifica subito.
