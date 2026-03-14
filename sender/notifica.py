# Solo formattazione del messaggio e invio a ntfy. Nessuna logica su "quando" o "quale" parola.
# Body e titolo solo testo (nessuna emoji). Opzionale: icona personalizzata via header Icon (URL pubblico).

import requests


def formatta_messaggio(voce, tipo="dizionario"):
    """
    Una notifica = solo dizionario O solo curiosita, mai entrambi.
    La traduzione (significato) c'è sempre: in parola è esplicita; in curiosità è sempre presente prima della chicca.
    tipo: "dizionario" = parola, significato, esempio. "curiosita" = parola, significato, curiosità breve ad alto impatto.
    Restituisce (titolo, corpo).
    """
    kanji = voce.get("kanji", "")
    lettura = voce.get("lettura", "")
    romaji = voce.get("romaji", "")
    significato = voce.get("significato", "")
    esempio = voce.get("esempio", "")
    esempio_trad = voce.get("esempio_traduzione", "")
    curiosita = (voce.get("curiosita") or "").strip()

    # Riga parola sempre con translitterazione: kanji (lettura - romaji)
    riga_parola = f"{kanji} ({lettura} - {romaji})" if (lettura or romaji) else kanji

    # Curiosità: sempre parola + SIGNIFICATO (la traduzione ci deve essere sempre) + curiosità breve ad alto impatto
    if tipo == "curiosita" and curiosita:
        titolo = "Giapponese C1 - Curiosita"
        corpo = f"{riga_parola}\nSignificato: {significato}\n{curiosita}"
        return titolo, corpo.strip()

    # Parola del momento: sempre kanji + lettura + romaji, poi significato ed esempio
    titolo = "Giapponese C1 - Parola del momento"
    corpo = riga_parola + "\nSignificato: " + significato
    if esempio or esempio_trad:
        corpo += "\nEsempio: " + (esempio or "") + (" " + esempio_trad if esempio_trad else "")
    return titolo, corpo.strip()


def formatta_messaggio_genz(voce_genz):
    """
    Notifica breve per il vocabolario Gen Z (slang). Restituisce (titolo, corpo).
    """
    frase = voce_genz.get("frase", "")
    significato = voce_genz.get("significato", "")
    titolo = "Giapponese C1 - Ora del vocabolario Gen Z"
    corpo = f"{frase}\n{significato}".strip()
    return titolo, corpo


def invia_notifica(titolo, corpo, topic, url_icona=None):
    """
    Invia la notifica al topic ntfy. Icona personalizzata (URL pubblico PNG/JPG) mostrata
    su iPhone e MacBook al posto della miniatura standard ntfy. Se url_icona è None o vuoto
    non si invia l'header Icon (ntfy userà la sua icona grigia).
    """
    url = "https://ntfy.sh/" + topic.strip("/")
    headers = {"Title": titolo, "Tags": "jp"}
    icon_url = (url_icona or "").strip()
    if icon_url.startswith("http"):
        headers["Icon"] = icon_url
    response = requests.post(
        url,
        data=corpo.encode("utf-8"),
        headers=headers,
        timeout=10,
    )
    response.raise_for_status()
