# Script una tantum: arricchisce le voci del vocabolario con una curiosita generata da Gemini.
# Usa solo GEMINI_API_KEY da ambiente (es. in .env). Non committere la chiave.
# Esegui: python3 scripts/arricchisci_curiosita.py
# Le voci che hanno gia "curiosita" non vengono modificate (salvo --forza).

import json
import os
import sys
from pathlib import Path

# Aggiungi la root del progetto al path per importare config
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Carica .env dalla root (GEMINI_API_KEY)
try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
except ImportError:
    pass

import config


def genera_curiosita_con_gemini(voce, api_key):
    """Genera curiosita con Google Gemini. Restituisce stringa o None."""
    try:
        import google.generativeai as genai
    except ImportError:
        print("Installa: pip3 install google-generativeai", file=sys.stderr)
        return None
    kanji = voce.get("kanji", "")
    lettura = voce.get("lettura", "")
    significato = voce.get("significato", "")
    prompt = f"""Per la parola giapponese {kanji} ({lettura}), significato: {significato}.
Scrivi in italiano UNA sola frase breve (massimo 120 caratteri) di curiosita: origine del kanji, uso storico, aneddoto, o perche si usa in certi contesti.
Solo testo, niente emoji. Rispondi solo con la frase, senza virgolette o prefissi."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        resp = model.generate_content(prompt)
        testo = (resp.text or "").strip()
        return testo[:200] if testo else None
    except Exception as e:
        print(f"  Errore Gemini per {kanji}: {e}", file=sys.stderr)
        return None


def main():
    forza = "--forza" in sys.argv
    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not gemini_key:
        print("Imposta GEMINI_API_KEY nel file .env. Non committere la chiave.", file=sys.stderr)
        sys.exit(1)

    path = config.PERCORSO_VOCABOLARIO
    if not path.exists():
        print(f"File non trovato: {path}", file=sys.stderr)
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        vocaboli = json.load(f)

    print("Uso Gemini per generare le curiosita.", flush=True)
    modificate = 0
    for voce in vocaboli:
        if not forza and (voce.get("curiosita") or "").strip():
            continue
        kanji = voce.get("kanji", "?")
        print(f"Genero curiosita per {kanji}...", flush=True)
        curiosita = genera_curiosita_con_gemini(voce, gemini_key)
        if curiosita:
            voce["curiosita"] = curiosita
            modificate += 1

    with open(path, "w", encoding="utf-8") as f:
        json.dump(vocaboli, f, ensure_ascii=False, indent=2)

    print(f"Fatto. Curiosita aggiunte/aggiornate: {modificate}")


if __name__ == "__main__":
    main()
