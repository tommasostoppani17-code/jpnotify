# Solo formattazione del messaggio e invio a ntfy. Nessuna logica su "quando" o "quale" parola.
# Body e titolo solo testo (nessuna emoji). Opzionale: icona personalizzata via header Icon (URL pubblico).

import requests


def formatta_messaggio(voce, tipo="dizionario"):
    """
    Una notifica = solo dizionario O solo curiosita, mai entrambi (cosi si legge tutto).
    tipo: "dizionario" = parola, lettura, significato, esempio. "curiosita" = solo la curiosita (e il kanji per contesto).
    Restituisce (titolo, corpo).
    """
    kanji = voce.get("kanji", "")
    lettura = voce.get("lettura", "")
    romaji = voce.get("romaji", "")
    significato = voce.get("significato", "")
    esempio = voce.get("esempio", "")
    esempio_trad = voce.get("esempio_traduzione", "")
    curiosita = (voce.get("curiosita") or "").strip()

    # Titolo solo ASCII (evita errore encoding header HTTP); kanji nel corpo
    if tipo == "curiosita" and curiosita:
        titolo = "Giapponese C1 - Curiosita"
        corpo = f"{kanji}\n{curiosita}"
        return titolo, corpo.strip()

    # dizionario: solo parola, significato, esempio (nessuna curiosita)
    titolo = "Giapponese C1 - Parola"
    riga_parola = f"{kanji} - {lettura} ({romaji})"
    corpo = riga_parola + "\nSignificato: " + significato
    if esempio or esempio_trad:
        corpo += "\nEsempio: " + (esempio or "") + (" " + esempio_trad if esempio_trad else "")
    return titolo, corpo.strip()


def invia_notifica(titolo, corpo, topic, url_icona=None):
    """
    Invia la notifica al topic ntfy. Lo slash prima del topic è obbligatorio.
    Se url_icona è un URL pubblico (PNG/JPG), ntfy la usa come icona al posto di quella grigia.
    """
    url = "https://ntfy.sh/" + topic.strip("/")
    headers = {"Title": titolo, "Tags": "jp"}
    if url_icona and url_icona.strip().startswith("http"):
        headers["Icon"] = url_icona.strip()
    response = requests.post(
        url,
        data=corpo.encode("utf-8"),
        headers=headers,
        timeout=10,
    )
    response.raise_for_status()
