from datetime import datetime, time, timedelta

# Orario lavorativo
ORARIO_INIZIO_LAVORO = time(9, 0)   # 09:00
ORARIO_FINE_LAVORO = time(18, 0)    # 18:00
PAUSA_PRANZO_INIZIO = time(13, 0)   # 13:00
PAUSA_PRANZO_FINE = time(14, 0)     # 14:00

    
def formatta_ore(ore_float):
        ore = int(ore_float)  # Parte intera = ore
        minuti = round((ore_float - ore) * 60)  # Parte decimale convertita in minuti
        return f"{ore}h {minuti}m"


def calcola_ore_lavorate(ora_ingresso, ora_uscita):
    """Calcola il tempo lavorato escludendo pause e orari non lavorativi."""
    if not ora_ingresso or not ora_uscita:
        return 0

    dt_ingresso = datetime.combine(datetime.today(), ora_ingresso)
    dt_uscita = datetime.combine(datetime.today(), ora_uscita)

    totale_ore = timedelta()

    while dt_ingresso < dt_uscita:
        # Se prima dell'orario di lavoro → sposta all'orario di inizio
        if dt_ingresso.time() < ORARIO_INIZIO_LAVORO:
            dt_ingresso = dt_ingresso.replace(hour=ORARIO_INIZIO_LAVORO.hour, minute=ORARIO_INIZIO_LAVORO.minute)
        
        # Se dentro l'orario di pausa → sposta dopo la pausa
        elif PAUSA_PRANZO_INIZIO <= dt_ingresso.time() < PAUSA_PRANZO_FINE:
            dt_ingresso = dt_ingresso.replace(hour=PAUSA_PRANZO_FINE.hour, minute=PAUSA_PRANZO_FINE.minute)

        # Se è dopo l'orario di lavoro → fine
        elif dt_ingresso.time() >= ORARIO_FINE_LAVORO:
            break

        # Calcola il tempo fino al prossimo step (pausa o fine lavoro)
        prossimo_step = min(
            datetime.combine(datetime.today(), ORARIO_FINE_LAVORO),
            datetime.combine(datetime.today(), PAUSA_PRANZO_INIZIO) if dt_ingresso.time() < PAUSA_PRANZO_INIZIO else dt_uscita
        )

        # Aggiungi tempo lavorato
        tempo_lavorato = min(prossimo_step, dt_uscita) - dt_ingresso
        totale_ore += tempo_lavorato
        dt_ingresso += tempo_lavorato  # Avanza il tempo

    return totale_ore.total_seconds() / 3600  # Converti in ore
