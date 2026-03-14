#!/usr/bin/env python3
"""
Genera data/vocabolario.json con 8000 parole da JLPT N1-N5 (open-anki-jlpt-decks).
Esegui: pip install requests pykakasi && python3 scripts/genera_vocabolario_8000.py
Scarica i CSV, converte in formato app (kanji, lettura, romaji, significato, livello, id_blocco).
"""

import csv
import json
import re
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = ROOT / "data" / "vocabolario.json"
PAROLE_PER_BLOCCO = 50
NUMERO_BLOCCHI = 160
TOTALE_PAROLE = PAROLE_PER_BLOCCO * NUMERO_BLOCCHI  # 8000

BASE_URL = "https://raw.githubusercontent.com/jamsinclair/open-anki-jlpt-decks/main/src"
SOURCES = [
    ("n1.csv", "N1"),
    ("n2.csv", "N2"),
    ("n3.csv", "N3"),
    ("n4.csv", "N4"),
    ("n5.csv", "N5"),
]


def kana_to_romaji(lettura: str) -> str:
    """Converte lettura (hiragana/katakana) in romaji. Usa pykakasi se disponibile."""
    if not lettura or not lettura.strip():
        return ""
    lettura = re.sub(r"\s*\([^)]*\)\s*", "", lettura).strip()  # rimuovi parentesi tipo (かん)
    try:
        import pykakasi
        kks = pykakasi.kakasi()
        result = kks.convert(lettura)
        return "".join(r["hepburn"] for r in result).strip() if result else ""
    except Exception:
        return ""


def fetch_csv(url: str) -> list[dict]:
    """Scarica CSV e restituisce lista di dict con expression, reading, meaning."""
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    lines = r.text.strip().split("\n")
    if not lines:
        return []
    reader = csv.DictReader(lines, fieldnames=["expression", "reading", "meaning", "tags", "guid"])
    next(reader, None)  # skip header if present
    rows = []
    for row in reader:
        expr = (row.get("expression") or "").strip()
        read = (row.get("reading") or "").strip()
        mean = (row.get("meaning") or "").strip()
        if expr and read:
            rows.append({"expression": expr, "reading": read, "meaning": mean})
    return rows


def main():
    print("Scarico e unisco i CSV JLPT N1-N5...", flush=True)
    tutte = []
    for filename, livello in SOURCES:
        url = f"{BASE_URL}/{filename}"
        rows = fetch_csv(url)
        for r in rows:
            r["livello"] = livello
        tutte.extend(rows)
        print(f"  {filename}: {len(rows)} parole", flush=True)

    if len(tutte) < TOTALE_PAROLE:
        print(f"Attenzione: trovate {len(tutte)} parole, ne servono {TOTALE_PAROLE}. Verranno usate tutte.", flush=True)
    else:
        tutte = tutte[:TOTALE_PAROLE]
        print(f"Usate le prime {TOTALE_PAROLE} parole.", flush=True)

    print("Conversione in romaji (pykakasi)...", flush=True)
    try:
        import pykakasi
    except ImportError:
        print("  pykakasi non installato: pip install pykakasi (romaji lasciato vuoto)", flush=True)

    vocabolario = []
    for i, row in enumerate(tutte):
        id_ = i + 1
        blocco = (i // PAROLE_PER_BLOCCO) + 1
        kanji = row["expression"]
        lettura = row["reading"]
        romaji = kana_to_romaji(lettura)
        significato = row["meaning"].replace('"', "'")[:200]
        voce = {
            "id": str(id_),
            "kanji": kanji,
            "lettura": lettura,
            "romaji": romaji or lettura,
            "significato": significato,
            "esempio": "",
            "esempio_traduzione": "",
            "curiosita": "",
            "livello": row["livello"],
            "id_blocco": blocco,
            "ultima_visualizzazione": "",
            "volte_questa_settimana": 0,
        }
        vocabolario.append(voce)

    ROOT.joinpath("data").mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(vocabolario, f, ensure_ascii=False, indent=2)

    print(f"Scritto {OUT_PATH} con {len(vocabolario)} voci.", flush=True)
    print("Imposta in config.py LIVELLO_VOCABOLI = \"all\" per usare tutte le parole (N1-N5).", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
