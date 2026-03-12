#!/bin/bash
# Avvia l'invio notifiche in background: non si ferma se chiudi il terminale.
# Si ferma solo quando spegni il Mac. Per non fermarsi mai (neanche a PC spento) usa GitHub Actions (vedi AVVIO_AUTOMATICO.md).

cd "$(dirname "$0")/.."
INTERVALLO=300
LOG="data/invio_continuo.log"

echo "Avvio in background. Log: $LOG"
echo "Per fermare: pkill -f 'python3 main.py' oppure kill il processo sotto."
nohup bash -c "while true; do python3 main.py >> $LOG 2>&1; sleep $INTERVALLO; done" &
echo "PID: $!"
echo "Controllo ogni 5 min, finestra 08:00-23:00. Per vedere il log: tail -f $LOG"
