from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from datetime import datetime,date

#this is a test!!!!



class Dipendenti(models.Model):
    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    data_assunzione = models.DateField()
    ruolo = models.ForeignKey("Ruoli", on_delete=models.SET_NULL, null=True)
    stipendio = models.DecimalField(max_digits=10, decimal_places=2)
    documento_contratto = models.BinaryField() #oppure filefield?
    def __str__(self):
        return f"{self.nome} {self.cognome}" 



class Permessi(models.Model):
    nome=models.CharField(max_length=100,unique=True) #: 'gestione_dipendenti', 'approva_ferie'
    descrizione=models.TextField()
    # aggiungere una lista di permessi predefiniti?

class Ruoli(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    livello_accesso = models.IntegerField(validators=[MinValueValidator(1)]) #solo positivi
    descrizione = models.TextField()
    permessi = models.ManyToManyField(Permessi)


class Ferie(models.Model):
    

    STATI_CHOICES = [
        ('In attesa', 'In attesa'),
        ('Approvata', 'Approvata'),
        ('Rifiutata', 'Rifiutata'),
    ]
    dipendente = models.ForeignKey('Dipendenti', on_delete=models.CASCADE)
    data_inizio=models.DateField()
    data_fine=models.DateField()
    stato = models.CharField(max_length=20, choices=STATI_CHOICES, default=STATI_CHOICES[0][0]) # DA TESTARE 



#DA TESTARE    
class Presenze(models.Model):

    data = models.DateField()
    ora_ingresso=models.TimeField()
    ora_uscita=models.TimeField(null=True)

    @property
    def ore_lavorate(self):
        if self.ora_uscita and self.ora_ingresso:
            delta = datetime.combine(date.min, self.ora_uscita) - datetime.combine(date.min, self.ora_ingresso)
            return delta.total_seconds() / 3600  # Converti in ore
        return None
    
class Bacheca(models.Model):
    titolo=models.CharField(max_length=100)
    messaggio=models.TextField()
    data_pubblicazione=models.DateTimeField(auto_now_add=True)


class ReportPresenze(models.Model):
    dipendente = models.ForeignKey('Dipendenti', on_delete=models.CASCADE)
    mese =  models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    anno = models.IntegerField(validators=[MinValueValidator(2000)])
    ore_totali = models.DecimalField(max_digits=5, decimal_places=2) #999.99

    #BUG CONTROLLARE!!! SE POI QUANDO LE VADO A SOMMARE ROMPONO TUTTO sum(Presenze.ore_lavorate)

class BustePaga(models.Model):
    dipendente = models.ForeignKey('Dipendenti', on_delete=models.CASCADE)
    mese =  models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    anno = models.IntegerField(validators=[MinValueValidator(2000)])
    importo = models.DecimalField(max_digits=8, decimal_places=2) #max 999 999.99
    data_emissione=models.DateField(auto_now_add=True)
    documento=models.BinaryField() #oppure filefield?

class Notifiche(models.Model):
    dipendente = models.ForeignKey('Dipendenti', on_delete=models.CASCADE)
    messaggio=models.TextField()
    data_invio=models.DateTimeField(auto_now_add=True)
    letto=models.BooleanField(default=False)

    
""" 

CREATE TABLE notifiche (
    id SERIAL PRIMARY KEY,
    dipendente_id INT REFERENCES dipendenti(id) ON DELETE CASCADE,
    messaggio TEXT NOT NULL,
    data_invio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    letto BOOLEAN DEFAULT FALSE
);




CREATE TABLE buste_paga (
    id SERIAL PRIMARY KEY,
    dipendente_id INT REFERENCES dipendenti(id) ON DELETE CASCADE,
    mese INT CHECK (mese BETWEEN 1 AND 12),
    anno INT CHECK (anno >= 2000),
    importo DECIMAL(10,2) NOT NULL,
    data_emissione DATE DEFAULT CURRENT_DATE,
    documento BYTEA
);
CREATE TABLE report_presenze (
    id SERIAL PRIMARY KEY,
    dipendente_id INT REFERENCES dipendenti(id) ON DELETE CASCADE,
    mese INT CHECK (mese BETWEEN 1 AND 12),
    anno INT CHECK (anno >= 2000),
    ore_totali DECIMAL(6,2)
);


CREATE TABLE bacheca (
    id SERIAL PRIMARY KEY,
    titolo VARCHAR(100) NOT NULL,
    messaggio TEXT NOT NULL,
    data_pubblicazione TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE presenze (
    id SERIAL PRIMARY KEY,
    dipendente_id INT REFERENCES dipendenti(id) ON DELETE CASCADE,
    data DATE NOT NULL,
    ora_ingresso TIME NOT NULL,
    ora_uscita TIME,
    ore_lavorate DECIMAL(4,2)
);
CREATE TABLE ferie (
    id SERIAL PRIMARY KEY,
    dipendente_id INT REFERENCES dipendenti(id) ON DELETE CASCADE,
    data_inizio DATE NOT NULL,
    data_fine DATE NOT NULL,
    stato VARCHAR(20) CHECK (stato IN ('In attesa', 'Approvata', 'Rifiutata'))
);
 """



""" 
CREATE TABLE ruoli (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,
    livello_accesso INT NOT NULL CHECK (livello_accesso BETWEEN 1 AND 10), -- 1 = base, 10 = admin
    descrizione TEXT
);




CREATE TABLE dipendenti (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    cognome VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    data_assunzione DATE NOT NULL,
    ruolo_id INT REFERENCES ruoli(id) ON DELETE SET NULL,
    stipendio DECIMAL(10,2),
    documento_contratto BYTEA
); """