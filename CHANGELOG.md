# Changelog

Formato basato su [Keep a Changelog](https://keepachangelog.com/it/1.0.0/).

## [1.0.0] - 2026-03-12

### Aggiunto

- Notifiche push (ntfy) con vocaboli giapponesi N1: parola del momento (kanji, lettura, romaji, significato, esempio), curiosità, vocabolario Gen Z.
- Finestra invio 06:00–02:00 (ora italiana), intervallo casuale 5–10 min.
- Sistema a blocchi (160 × 50 = 8000 parole), spaced repetition con 20% ripasso.
- Esecuzione in locale (Python) e in cloud (GitHub Actions ogni 5 min).
- Icona notifiche personalizzabile (URL in `.env` o secret).
- Script `arricchisci_curiosita.py` per generare curiosità con Gemini.
- Documentazione: README, GITHUB_SETUP, AVVIO_AUTOMATICO, .env.example.
- Licenza MIT.

### Note

- Il file `data/vocabolario.json` va popolato con le voci (o usare un dataset esterno). Lo schema è documentato nel README e negli esempi in repo.
