# Setup GitHub: notifiche anche a PC spento

Segui questi passi una sola volta. Dopo, le notifiche partono da GitHub ogni 5 min (08:00-23:00, Europe/Rome).

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

(Opzionale: per l’icona personalizzata, aggiungi anche il secret `ICONA_NOTIFICA_URL` con l’URL raw di `assets/icona_notifica.png` dopo il push.)

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

## 4. Verifica

- Nella repo: **Actions** → dovresti vedere il workflow "Invia notifica vocabolario". Parte ogni 5 min; puoi anche lanciarlo a mano con **Run workflow**.
- Sul telefono: tieni l’app ntfy aperta sul topic scelto. Le notifiche arrivano a orari irregolari tra 08:00 e 23:00 (ora italiana).

Da questo momento puoi chiudere il PC: le notifiche continuano da GitHub.
