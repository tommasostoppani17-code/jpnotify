# Orchestratore: legge config, controlla se è ora di inviare, carica dati, filtra, pool, sceglie, formatta, invia, aggiorna stato.
# Flusso: Leggi -> Filtra -> Formatta -> Invia (piano sezione 6). Gira in cloud (GitHub Actions) o in locale.

import random
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import config
from logic import selezionatore
from sender import notifica


def _ora_in_finestra(ora, ora_inizio, ora_fine):
    """Verifica se l'ora (datetime con timezone) è nella finestra ora_inizio--ora_fine (stringhe HH:MM)."""
    h_i, m_i = map(int, ora_inizio.split(":"))
    h_f, m_f = map(int, ora_fine.split(":"))
    inizio = ora.replace(hour=h_i, minute=m_i, second=0, microsecond=0)
    fine = ora.replace(hour=h_f, minute=m_f, second=0, microsecond=0)
    return inizio <= ora <= fine


def _leggi_prossimo_invio(percorso):
    """Legge il timestamp del prossimo invio (ISO) dal file. Se vuoto o mancante, restituisce None (invia subito)."""
    path = Path(percorso)
    if not path.exists():
        return None
    testo = path.read_text(encoding="utf-8").strip()
    if not testo:
        return None
    try:
        return datetime.fromisoformat(testo.replace("Z", "+00:00"))
    except ValueError:
        return None


def _scrivi_prossimo_invio(percorso, dt):
    """Scrive il timestamp del prossimo invio in ISO."""
    Path(percorso).write_text(dt.isoformat(), encoding="utf-8")


def _calcola_prossimo_istante(fuso_orario, ora_inizio, ora_fine, min_minuti, max_minuti):
    """
    Calcola il prossimo istante di invio: ora + intervallo casuale (min_max minuti).
    Se cade dopo ora_fine, imposta al giorno dopo a ora_inizio + un po' di random.
    """
    tz = ZoneInfo(fuso_orario)
    ora = datetime.now(tz)
    minuti = random.randint(min_minuti, max_minuti)
    prossimo = ora + timedelta(minutes=minuti)
    h_f, m_f = map(int, ora_fine.split(":"))
    fine_oggi = ora.replace(hour=h_f, minute=m_f, second=0, microsecond=0)
    if prossimo > fine_oggi:
        h_i, m_i = map(int, ora_inizio.split(":"))
        domani = (ora + timedelta(days=1)).replace(hour=h_i, minute=m_i, second=0, microsecond=0)
        prossimo = domani + timedelta(minutes=random.randint(0, 30))
    return prossimo


def _deve_inviare_ora():
    """
    True se siamo nella finestra 08:00-23:00 e l'ora corrente è >= prossimo_invio.
    Se prossimo_invio non c'è o è nel passato, considera "invia ora" se siamo in finestra.
    """
    tz = ZoneInfo(config.FUSO_ORARIO)
    ora = datetime.now(tz)
    if not _ora_in_finestra(ora, config.ORA_INIZIO, config.ORA_FINE):
        return False
    prossimo = _leggi_prossimo_invio(config.PERCORSO_PROSSIMO_INVIO)
    if prossimo is None:
        return True
    # prossimo potrebbe essere naive o aware; confronto in UTC o in local
    if prossimo.tzinfo is None:
        prossimo = prossimo.replace(tzinfo=tz)
    return ora >= prossimo


def _scrivi_log(riga):
    """Append opzionale su file log per statistiche."""
    if not config.PERCORSO_LOG:
        return
    path = Path(config.PERCORSO_LOG)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(riga + "\n")


def main():
    # 1. Controllo scheduler: invio solo se siamo in finestra e e ora di inviare
    if not _deve_inviare_ora():
        return 0

    # 2. Carica e filtra
    try:
        vocaboli = selezionatore.carica_vocaboli(config.PERCORSO_VOCABOLARIO)
    except (FileNotFoundError, ValueError) as e:
        print(f"Errore caricamento vocabolario: {e}", file=sys.stderr)
        return 1

    vocaboli_filtrati = selezionatore.filtra_per_livello(vocaboli, config.LIVELLO_VOCABOLI)
    if not vocaboli_filtrati:
        print("Nessun vocabolo per il livello configurato.", file=sys.stderr)
        return 1

    # 3. Blocco e pool attivo
    blocco = selezionatore.calcola_blocco_corrente(config.FUSO_ORARIO)
    pool_attivo = selezionatore.costruisci_pool_attivo(
        vocaboli_filtrati,
        blocco,
        config.PERCENTUALE_RIPASSO,
        config.PAROLE_PER_BLOCCO,
    )
    if not pool_attivo:
        print("Pool attivo vuoto.", file=sys.stderr)
        return 1

    # 4. Scegli parola
    parola = selezionatore.scegli_parola(pool_attivo, config.MAX_RIPETIZIONI_SETTIMANA)
    if not parola:
        print("Nessuna parola disponibile nel pool.", file=sys.stderr)
        return 1

    # 5. Formatta e invia: una notifica = solo dizionario O solo curiosita (scelta casuale)
    tipo = random.choice(["dizionario", "curiosita"])
    if tipo == "curiosita" and not (parola.get("curiosita") or "").strip():
        tipo = "dizionario"
    titolo, corpo = notifica.formatta_messaggio(parola, tipo=tipo)
    try:
        notifica.invia_notifica(titolo, corpo, config.NTFY_TOPIC, url_icona=config.ICONA_NOTIFICA_URL or None)
    except Exception as e:
        print(f"Errore invio notifica: {e}", file=sys.stderr)
        return 1

    # 6. Aggiorna contatori e prossimo istante
    selezionatore.aggiorna_contatori(
        config.PERCORSO_VOCABOLARIO,
        parola["id"],
        config.FUSO_ORARIO,
    )
    prossimo = _calcola_prossimo_istante(
        config.FUSO_ORARIO,
        config.ORA_INIZIO,
        config.ORA_FINE,
        config.INTERVALLO_MIN_MINUTI,
        config.INTERVALLO_MAX_MINUTI,
    )
    _scrivi_prossimo_invio(config.PERCORSO_PROSSIMO_INVIO, prossimo)

    # 7. Log opzionale
    riga_log = f"{datetime.now(ZoneInfo(config.FUSO_ORARIO)).isoformat()} id={parola['id']} kanji={parola.get('kanji', '')}"
    _scrivi_log(riga_log)

    print("Notifica inviata:", parola.get("kanji"), parola.get("romaji"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
