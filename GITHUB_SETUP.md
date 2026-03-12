# Setup GitHub: notifiche anche a PC spento

**Le notifiche partono da GitHub**, non dal tuo computer. Puoi **chiudere Cursor**, **spegnere il PC** e le notifiche continuano (dalle **6:00** alle **2:00** ora italiana, ogni 5–10 min). Obiettivo: **8000 vocaboli** in blocchi da 50 con spaced repetition, così nel tempo copri tutte le parole.

Segui questi passi una sola volta. Dopo, il workflow gira da solo ogni 5 minuti.

---

## 1. Crea il repository su GitHub

1. Vai su [github.com/new](https://github.com/new).
2. Nome (es. `spaced-repetition-giapponese`), visibilità **Private** o Public.
3. **Non** spuntare "Add a README" (il progetto esiste gia).
4. Clicca **Create repository**.

---

## 2. Aggiungi il secret per ntfy

1. Nel repo: **Settings** → **Secrets and variables** → **Actions**.
2. **New repository secret**.
3. Nome: `NTFY_TOPIC`  
   Valore: il tuo topic ntfy (es. `mio_giapponese_extreme_8000` – quello che usi nell’app ntfy sull’iPhone).
4. Salva.

**Icona notifiche personalizzata:**  
Aggiungi il secret `ICONA_NOTIFICA_URL` con l’**URL pubblico della tua immagine** (PNG/JPG). ntfy la userà per tutte le notifiche.  
Esempi: URL raw di un’immagine su GitHub, link da Imgur o da un tuo sito. Se non lo imposti, si usa l’icona del repo (pagoda).
```
https://raw.githubusercontent.com/tommasostoppani17-code/jpnotify/main/assets/icona_notifica.png
```

---

## 3. Collega e pusha il progetto

Nel terminale, dalla cartella del progetto:

```bash
cd "/Users/tommaso/Desktop/Spaced Repetition"
git remote add origin https://github.com/TUO_USERNAME/TUO_REPO.git
git branch -M main
git push -u origin main
```

Sostituisci `TUO_USERNAME` e `TUO_REPO` con i tuoi (es. `mionome` e `spaced-repetition-giapponese`). Se GitHub chiede login, usa le tue credenziali o un token.

---

## 4. Verifica e primo test

1. **Actions** → workflow **"Invia notifica vocabolario"**.
2. Clicca **Run workflow** (dropdown) → spunta **"Invia subito (test)"** → **Run workflow**.
3. Quando il run è finito (icona verde), apri il run e nella step **"Esegui main"** controlla l’exit code: `0` = notifica inviata, nessun output dopo = non era ancora ora (normale con lo schedule).
4. Sul telefono/MacBook: apri l’app ntfy e iscriviti al **topic** uguale al valore che hai messo in `NTFY_TOPIC` (es. `mio_giapponese_extreme_8000`). Dovresti ricevere una notifica entro pochi secondi dal run con "Invia subito" attivo.

Se non arriva nulla: controlla nel run la riga **"Topic ntfy impostato: si"** (se vedi **NO**, aggiungi il secret `NTFY_TOPIC`). Le notifiche automatiche partono ogni 5 min tra le 06:00 e le 02:00 (ora italiana).

Da questo momento puoi chiudere il PC: le notifiche continuano da GitHub.
