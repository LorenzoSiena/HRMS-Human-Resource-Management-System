from datetime import datetime, time, timedelta

# Orario lavorativo
ORARIO_INIZIO_LAVORO = time(9, 0)   # 09:00
ORARIO_FINE_LAVORO = time(18, 0)    # 18:00
PAUSA_PRANZO_INIZIO = time(13, 0)   # 13:00
PAUSA_PRANZO_FINE = time(14, 0)     # 14:00

# Giorni lavorativi sono immutabili! in caso fixami
GIORNI_LAVORATIVI = {
    1: 'Lunedi',
    2: 'Martedi',
    3: 'Mercoledi',
    4: 'Giovedi',
    5: 'Venerdi',
}
    
#TODO VA TESTATO 
def ore_lavorative_tra_date(start, end):
    """
    Calcola le ore lavorative tra due datetime, escludendo sabato e domenica 
    e considerando solo l'orario lavorativo 09:00-13:00 e 14:00-18:00.
    """

    total_work_seconds = 0  # Conteggio totale dei secondi lavorativi
    current = start

    while current.date() <= end.date():
        # Se è sabato o domenica, passiamo al giorno successivo
        if current.weekday() in [5, 6]:  # 5=Sabato, 6=Domenica
            current += timedelta(days=1)
            current = datetime.combine(current.date(), ORARIO_INIZIO_LAVORO)
            continue

        # Convertiamo l'orario di lavoro in datetime per il giorno corrente
        work_morning_start = datetime.combine(current.date(), ORARIO_INIZIO_LAVORO)
        work_morning_end = datetime.combine(current.date(), PAUSA_PRANZO_INIZIO)
        work_afternoon_start = datetime.combine(current.date(), PAUSA_PRANZO_FINE)
        work_afternoon_end = datetime.combine(current.date(), ORARIO_FINE_LAVORO)

        # Se `current` è prima dell'orario lavorativo, lo spostiamo all'inizio del lavoro
        if current < work_morning_start:
            current = work_morning_start

        # Se il giorno di inizio è lo stesso del giorno di fine
        if current.date() == end.date():
            if current < work_morning_end and end > work_morning_start:
                total_work_seconds += (min(end, work_morning_end) - current).total_seconds()

            if current < work_afternoon_end and end > work_afternoon_start:
                total_work_seconds += (min(end, work_afternoon_end) - max(current, work_afternoon_start)).total_seconds()

            break  # Uscita perché abbiamo finito il calcolo

        # Se siamo in un giorno intermedio tra start e end
        if current.date() > start.date() and current.date() < end.date():
            total_work_seconds += (work_morning_end - work_morning_start).total_seconds()
            total_work_seconds += (work_afternoon_end - work_afternoon_start).total_seconds()
        else:  # Giorno iniziale parziale
            if current < work_morning_end:
                total_work_seconds += (work_morning_end - max(current, work_morning_start)).total_seconds()
            if current < work_afternoon_end:
                total_work_seconds += (work_afternoon_end - max(current, work_afternoon_start)).total_seconds()

        # Passiamo al giorno successivo, reimpostando l'orario all'inizio della fascia lavorativa
        current += timedelta(days=1)
        current = datetime.combine(current.date(), ORARIO_INIZIO_LAVORO)

    # Convertiamo i secondi in ore
    total_work_hours = total_work_seconds / 3600
    return total_work_hours


























def formatta_ore(ore_float):
        ore = int(ore_float)  # Parte intera = ore
        minuti = round((ore_float - ore) * 60)  # Parte decimale convertita in minuti
        return f"{ore}h {minuti}m"


def calcola_giorni_totali(data_inizio,data_fine):

    if not data_inizio or not data_fine:
        return 0
    giorni_totali = 0
    giorno_corrente = data_inizio

    while giorno_corrente <= data_fine:
        if giorno_corrente.weekday() < 5:  # 0 = lunedì, ..., 4 = venerdì
            giorni_totali += 1
        giorno_corrente += timedelta(days=1)

    return giorni_totali


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


