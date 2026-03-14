# Configurazione centrale: modificare solo qui senza toccare il resto del codice.
# Legge da variabili d'ambiente dove sensibile (es. topic ntfy).

import os
from pathlib import Path

__version__ = "1.0.0"

# Directory base del progetto (dove si trova config.py)
BASE_DIR = Path(__file__).resolve().parent

# Topic ntfy: chi si iscrive nell'app riceve le notifiche. Preferire .env per non committere.
_DEFAULT_TOPIC = "mio_giapponese_extreme_8000"
NTFY_TOPIC = (os.getenv("NTFY_TOPIC") or _DEFAULT_TOPIC).strip() or _DEFAULT_TOPIC

# Icona notifica personalizzata: URL pubblico della TUA immagine (PNG/JPG). ntfy la mostra al posto di quella grigia.
# Imposta in .env (locale) o nel secret ICONA_NOTIFICA_URL (GitHub). Vuoto = usa icona predefinita del repo.
_DEFAULT_ICONA = "https://raw.githubusercontent.com/tommasostoppani17-code/jpnotify/main/assets/icona_notifica.png"
ICONA_NOTIFICA_URL = (os.getenv("ICONA_NOTIFICA_URL") or _DEFAULT_ICONA).strip() or _DEFAULT_ICONA

# Cartella dati (creata automaticamente se mancante)
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Percorso del file vocabolario
PERCORSO_VOCABOLARIO = DATA_DIR / "vocabolario.json"

# Vocabolario Gen Z (frasi slang, notifiche brevi "Ora del vocabolario Gen Z")
PERCORSO_VOCABOLARIO_GENZ = DATA_DIR / "vocabolario_genz.json"

# File in cui persistere il prossimo istante di invio (per intervalli irregolari)
PERCORSO_PROSSIMO_INVIO = DATA_DIR / "prossimo_invio.txt"

# File log opzionale per statistiche a fine settimana
PERCORSO_LOG = DATA_DIR / "log.txt"

# Fuso orario e finestra: 06:00-02:00 (ora italiana, fino alle 2 di notte)
FUSO_ORARIO = "Europe/Rome"

# Finestra giornaliera: invio dalle 6:00 alle 2:00 del mattino dopo (finestra che attraversa mezzanotte)
ORA_INIZIO = "06:00"
ORA_FINE = "02:00"

# Circa ogni 10 min una notifica, a volte due in periodi random (intervallo 5-10 min tra un invio e l'altro)
NOTIFICHE_PER_GIORNO_MIN = 50
NOTIFICHE_PER_GIORNO_MAX = 90

# Intervallo in minuti tra un invio e il prossimo: più breve = notifiche più frequenti
INTERVALLO_MIN_MINUTI = 3
INTERVALLO_MAX_MINUTI = 6

# Livello vocaboli: "all" = tutte le 8000 (N1-N5), "N1" = solo N1, ecc.
LIVELLO_VOCABOLI = "all"

# Un blocco a settimana, 50 parole per blocco. 160 blocchi x 50 = 8000 parole totali (spaced repetition)
PAROLE_PER_BLOCCO = 50

# Percentuale del pool riservata a parole da ripassare da blocchi precedenti
PERCENTUALE_RIPASSO = 0.20

# Limite ripetizioni per parola nella settimana (con più notifiche/ora, serve un tetto più alto per il pool)
MAX_RIPETIZIONI_SETTIMANA = 6
