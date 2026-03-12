# Configurazione centrale: modificare solo qui senza toccare il resto del codice.
# Legge da variabili d'ambiente dove sensibile (es. topic ntfy).

import os
from pathlib import Path

# Directory base del progetto (dove si trova config.py)
BASE_DIR = Path(__file__).resolve().parent

# Topic ntfy: chi si iscrive nell'app riceve le notifiche. Preferire .env per non committere.
NTFY_TOPIC = os.getenv("NTFY_TOPIC", "mio_giapponese_extreme_8000")

# Icona notifica: URL pubblico (pagoda giapponese). Se vuoto, usa quella del repo su GitHub.
ICONA_NOTIFICA_URL = os.getenv(
    "ICONA_NOTIFICA_URL",
    "https://raw.githubusercontent.com/tommasostoppani17-code/jpnotify/main/assets/icona_notifica.png",
).strip()

# Percorso del file vocabolario
PERCORSO_VOCABOLARIO = BASE_DIR / "data" / "vocabolario.json"

# Vocabolario Gen Z (frasi slang, notifiche brevi "Ora del vocabolario Gen Z")
PERCORSO_VOCABOLARIO_GENZ = BASE_DIR / "data" / "vocabolario_genz.json"

# File in cui persistere il prossimo istante di invio (per intervalli irregolari)
PERCORSO_PROSSIMO_INVIO = BASE_DIR / "data" / "prossimo_invio.txt"

# File log opzionale per statistiche a fine settimana
PERCORSO_LOG = BASE_DIR / "data" / "log.txt"

# Fuso orario per "questa settimana" e finestra 08:00-23:00
FUSO_ORARIO = "Europe/Rome"

# Finestra giornaliera: invio solo tra ora_inizio e ora_fine
ORA_INIZIO = "08:00"
ORA_FINE = "23:00"

# Circa ogni 10 min una notifica, a volte due in periodi random (intervallo 5-10 min tra un invio e l'altro)
NOTIFICHE_PER_GIORNO_MIN = 50
NOTIFICHE_PER_GIORNO_MAX = 90

# Intervallo casuale in minuti tra un invio e il prossimo: 5-10 min (puo arrivare 1 o 2 ogni 10 min)
INTERVALLO_MIN_MINUTI = 5
INTERVALLO_MAX_MINUTI = 10

# Livello vocaboli da usare (N1 = C1)
LIVELLO_VOCABOLI = "N1"

# Un blocco a settimana, 50 parole per blocco. 160 blocchi x 50 = 8000 parole totali (spaced repetition)
PAROLE_PER_BLOCCO = 50

# Percentuale del pool riservata a parole da ripassare da blocchi precedenti
PERCENTUALE_RIPASSO = 0.20

# Limite ripetizioni per parola nella settimana (con più notifiche/ora, serve un tetto più alto per il pool)
MAX_RIPETIZIONI_SETTIMANA = 6
