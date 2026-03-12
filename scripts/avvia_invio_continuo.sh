#!/bin/bash
# Automazione: esegue main.py ogni 10 minuti. Le notifiche partono a intervalli random (5-10 min), con curiosita Gemini.
# Tieni aperto il terminale (o lancia in background con nohup). Ctrl+C per fermare.

cd "$(dirname "$0")/.."
# Controllo ogni 5 min cosi possono arrivare 1 o 2 notifiche in un periodo di 10 min (intervallo random 5-10 min)
INTERVALLO=300

echo "Avvio invio notifiche: controllo ogni 5 min (finestra 08:00-23:00, circa 1-2 notifiche ogni 10 min). Ctrl+C per fermare."
while true; do
  python3 main.py
  sleep "$INTERVALLO"
done
