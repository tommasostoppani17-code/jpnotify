# Logica di selezione: carica dati, blocco corrente, pool attivo, scelta parola, aggiornamento contatori.
# Nessun I/O verso ntfy; solo calcoli e scelta. Riferimento: piano sezione 8bis (Extreme Passive Learning).

import json
import random
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

# 160 blocchi x 50 parole = 8000 parole totali (un blocco sbloccato a settimana)
NUMERO_BLOCCHI = 160


def carica_vocaboli(percorso):
    """
    Carica il file vocabolario e restituisce la lista di voci.
    Ogni voce è un dict con id, kanji, lettura, id_blocco, ultima_visualizzazione, volte_questa_settimana, ecc.
    """
    path = Path(percorso)
    if not path.exists():
        raise FileNotFoundError(f"File vocabolario non trovato: {percorso}")
    with open(path, "r", encoding="utf-8") as f:
        dati = json.load(f)
    if not isinstance(dati, list):
        raise ValueError("Il vocabolario deve essere una lista di voci.")
    return dati


def filtra_per_livello(vocaboli, livello):
    """Restituisce solo le voci con livello uguale al parametro (es. N1)."""
    return [v for v in vocaboli if v.get("livello") == livello]


def calcola_blocco_corrente(fuso_orario="Europe/Rome"):
    """
    Restituisce il numero di blocco (1-160) per la settimana corrente.
    Settimana dall'inizio di riferimento (2025-01-01) modulo 160, così ogni settimana sblocca un blocco nuovo.
    """
    ref = datetime(2025, 1, 1, tzinfo=ZoneInfo(fuso_orario))
    ora = datetime.now(ZoneInfo(fuso_orario))
    giorni_da_ref = (ora - ref).days
    settimane_da_ref = giorni_da_ref // 7
    blocco = (settimane_da_ref % NUMERO_BLOCCHI) + 1
    return blocco


def costruisci_pool_attivo(
    vocaboli_filtrati,
    blocco_corrente,
    percentuale_ripasso,
    parole_per_blocco,
):
    """
    Costruisce il pool attivo di 50 parole: circa 80% dal blocco corrente, 20% da blocchi precedenti da ripassare.
    Da ripassare: id_blocco < blocco_corrente, ordinati per ultima_visualizzazione più vecchia (o mai visti).
    """
    blocco_corrente_int = int(blocco_corrente)
    parole_blocco_corrente = [
        v for v in vocaboli_filtrati
        if v.get("id_blocco") == blocco_corrente_int
    ]
    parole_precedenti = [
        v for v in vocaboli_filtrati
        if isinstance(v.get("id_blocco"), (int, float)) and int(v.get("id_blocco")) < blocco_corrente_int
    ]

    # Ordina da ripassare: prima mai viste (ultima_visualizzazione null), poi per ultima_visualizzazione più vecchia
    def chiave_ripasso(voce):
        uv = voce.get("ultima_visualizzazione")
        if uv is None or uv == "":
            return ("", "1970-01-01")
        return (uv, uv)

    parole_precedenti.sort(key=chiave_ripasso)

    num_ripasso = max(0, int(parole_per_blocco * percentuale_ripasso))
    num_blocco = min(parole_per_blocco - num_ripasso, len(parole_blocco_corrente))
    num_ripasso = min(num_ripasso, len(parole_precedenti), parole_per_blocco - num_blocco)

    pool = []
    pool.extend(parole_blocco_corrente[: num_blocco])
    pool.extend(parole_precedenti[: num_ripasso])

    # Se il pool è ancora sotto 50 perché il blocco corrente ha poche parole, riempi con altre dal blocco o precedenti
    if len(pool) < parole_per_blocco and len(parole_blocco_corrente) > num_blocco:
        pool.extend(parole_blocco_corrente[num_blocco : num_blocco + (parole_per_blocco - len(pool))])
    if len(pool) < parole_per_blocco and len(parole_precedenti) > num_ripasso:
        pool.extend(parole_precedenti[num_ripasso : num_ripasso + (parole_per_blocco - len(pool))])

    return pool[:parole_per_blocco]


def scegli_parola(pool_attivo, max_ripetizioni_settimana):
    """
    Sceglie una parola dal pool: priorita a parole con volte_questa_settimana < max
    e ultima_visualizzazione più vecchia; un po' di random tra le candidate per variare.
    Restituisce un singolo dict (voce completa) o None se pool vuoto.
    """
    if not pool_attivo:
        return None

    # Candidate: sotto il limite di ripetizioni
    candidate = [
        v for v in pool_attivo
        if (v.get("volte_questa_settimana") or 0) < max_ripetizioni_settimana
    ]
    if not candidate:
        candidate = list(pool_attivo)

    # Ordina per ultima_visualizzazione più vecchia (priorità a chi non è stato visto da più tempo)
    def chiave(voce):
        uv = voce.get("ultima_visualizzazione")
        if uv is None or uv == "":
            return "1970-01-01T00:00:00"
        return uv or "1970-01-01T00:00:00"

    candidate.sort(key=chiave)

    # Prendi le prime N (es. 10) più "da ripassare" e scegli a caso tra quelle per non essere sempre uguale
    n = min(10, len(candidate))
    scelta = random.choice(candidate[:n])
    return scelta


def aggiorna_contatori(percorso, id_parola, fuso_orario="Europe/Rome"):
    """
    Dopo la scelta: incrementa volte_questa_settimana e imposta ultima_visualizzazione a ora
    per la voce con id_parola. Se è cambiata la settimana (rispetto a un marcatore opzionale),
    si potrebbe azzerare volte_questa_settimana per tutte; qui facciamo solo l'aggiornamento della singola voce.
    """
    path = Path(percorso)
    with open(path, "r", encoding="utf-8") as f:
        vocaboli = json.load(f)

    ora_iso = datetime.now(ZoneInfo(fuso_orario)).strftime("%Y-%m-%dT%H:%M:%S")
    for voce in vocaboli:
        if str(voce.get("id")) == str(id_parola):
            voce["ultima_visualizzazione"] = ora_iso
            voce["volte_questa_settimana"] = (voce.get("volte_questa_settimana") or 0) + 1
            break

    with open(path, "w", encoding="utf-8") as f:
        json.dump(vocaboli, f, ensure_ascii=False, indent=2)
