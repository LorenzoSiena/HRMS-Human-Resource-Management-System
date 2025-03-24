from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from datetime import datetime,date
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from django.db.models import Sum
from .utils import calcola_ore_lavorate,formatta_ore,calcola_giorni_totali,ore_lavorative_tra_date  # Importiamo la funzione per il calcolo delle ore lavorate


#BUG NOTI

#ReportPermessi
#Funziona solo se non sforo il mese , altrimenti sballa il conto

#utils.py viene usato ma
#calcola_ore_lavorate va letto bene se funziona

class Dipendenti(AbstractUser):
    #email == username!!!
    username = None
    #telefono

    telefono = models.CharField(max_length=20)
    data_assunzione = models.DateField(default=date.today)
    superiore = models.ForeignKey("Dipendenti", on_delete=models.SET_NULL, null=True,blank=True)
    ruolo = models.ForeignKey("Ruoli", on_delete=models.SET_NULL, null=True)
    stipendio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    documento_contratto = models.FileField( upload_to='media/documenti_contratti/', null=True, blank=True)

    codice_fiscale = models.CharField(max_length=16)
    indirizzo_completo = models.CharField(max_length=128)
    data_nascita = models.DateField(null=True, blank=True)


    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'  # Usiamo l'email come username
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']  # Campi obbligatori oltre a `email`

    #Per comoditá [username->email]  [first_name->nome] [last_name->cognome]
    @property
    def nome(self):
        return self.first_name

    @nome.setter
    def nome(self, value):
        self.first_name = value

    @property
    def cognome(self):
        return self.last_name

    @cognome.setter
    def cognome(self, value):
        self.last_name = value

    @property
    def indirizzo_email(self):
        return self.email

    @indirizzo_email.setter
    def indirizzo_email(self, value):
        self.email = value
    def __str__(self):
        return f"{self.nome} {self.cognome} ({self.email})"


#Riconvertire in group e in permessi
#https://docs.djangoproject.com/en/3.2/topics/auth/default/#default-permissions
# LI DEVO TOGLIERE E SOSTITUIRE CON GROUP E PERMISSIONS


class Autorizzazioni(models.Model):
    nome=models.CharField(max_length=100,unique=True) #: 'gestione_dipendenti', 'approva_ferie'
    descrizione=models.TextField()
    def __str__(self): 
        return self.nome

class Ruoli(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    livello_accesso = models.IntegerField(validators=[MinValueValidator(1)]) #solo positivi
    descrizione = models.TextField()
    autorizzazioni = models.ManyToManyField(Autorizzazioni)
    def __str__(self):
        return self.nome



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
    giorni_totali_previsti=models.IntegerField(default=0)    

    def save(self, *args, **kwargs):
        self.giorni_totali_previsti = calcola_giorni_totali(self.data_inizio, self.data_fine)
        super().save(*args, **kwargs)

    @property
    def giorni_totali_approvati(self):
        if self.stato == 'Approvata':
            giorni_totali_approvati = calcola_giorni_totali(self.data_inizio, self.data_fine)
        else:
            giorni_totali_approvati = 0
        return giorni_totali_approvati
    def __str__(self):
        
        return  f" ({self.stato}) - ({self.data_inizio} - {self.data_fine})"



class ReportFerie(models.Model):
    dipendente = models.ForeignKey('Dipendenti', on_delete=models.CASCADE)
    mese =  models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    anno = models.IntegerField(validators=[MinValueValidator(2000)])
    giorni_totali = models.DecimalField(max_digits=5, decimal_places=2)
    
    def save(self, *args, **kwargs):
        giorni_totali = Ferie.objects.filter(
            dipendente=self.dipendente,
            data_inizio__year=self.anno,
            data_inizio__month=self.mese
        ).aggregate(Sum('giorni_totali_previsti'))['giorni_totali_previsti__sum'] or 0

        self.giorni_totali = giorni_totali 
        super().save(*args, **kwargs)

#---------------------------------------------------------------------------------------


class Permessi(models.Model): 
    
    STATI_CHOICES = [
        ('In attesa', 'In attesa'),
        ('Approvata', 'Approvata'),
        ('Rifiutata', 'Rifiutata'),
    ]
    
    dipendente = models.ForeignKey('Dipendenti', on_delete=models.CASCADE)
    data_ora_inizio=models.DateTimeField()
    data_ora_fine=models.DateTimeField()
    stato = models.CharField(max_length=20, choices=STATI_CHOICES, default=STATI_CHOICES[0][0]) # DA TESTARE 
    retribuito=models.BooleanField()
    motivo=models.TextField()
    ore_totali_permesso_previste_float=models.FloatField() # in ore e giorni
    
    def save(self, *args, **kwargs):
        self.ore_totali_permesso_previste_float = ore_lavorative_tra_date(self.data_ora_inizio, self.data_ora_fine)
        super().save(*args, **kwargs)


    @property
    def ore_totali_permesso_approvate_float(self) -> float:
        if self.stato == 'Approvata':
            ore_totali_permesso_approvate = self.ore_totali_permesso_previste_float
        else:
            ore_totali_permesso_approvate = 0
        return ore_totali_permesso_approvate
    @property
    def ore_totali_permesso_approvate(self) -> str:
        return formatta_ore(self.ore_totali_permesso_approvate_float or 0)

    def __str__(self):
        return  f" ({self.stato}) - ({self.data_ora_inizio} - {self.data_ora_fine} - sono previste {formatta_ore(self.ore_totali_permesso_previste_float)} ore)"


#BUG! Funziona solo se non sforo il mese @.@
class ReportPermessi(models.Model):
    dipendente = models.ForeignKey('Dipendenti', on_delete=models.CASCADE)
    mese =  models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    anno = models.IntegerField(validators=[MinValueValidator(2000)])

    ore_totali_permessi_float = models.DecimalField(max_digits=5, decimal_places=2) #999.99

    def save(self, *args, **kwargs):
        ore_totali_permessi = Permessi.objects.filter(
            dipendente=self.dipendente,
            data_ora_inizio__year=self.anno, 
            data_ora_inizio__month=self.mese #BUG!
        ).aggregate(Sum('ore_totali_permesso_approvate_float'))['ore_totali_permesso_approvate_float__sum'] or 0

        self.ore_totali_permessi_float = ore_totali_permessi
        super().save(*args, **kwargs)   
    @property
    def ore_totali_permessi(self):
        return formatta_ore(self.ore_totali_permessi_float or 0)

class Presenze(models.Model):

    data = models.DateField()
    ora_ingresso=models.TimeField()  #'14:30:00'
    ora_uscita=models.TimeField(null=True,blank=True) #'17:30:00'
    dipendente = models.ForeignKey('Dipendenti', on_delete=models.CASCADE)
    ore_lavorate_float = models.FloatField(null=True, blank=True) 

    def save(self, *args, **kwargs):
        self.ore_lavorate_float = calcola_ore_lavorate(self.ora_ingresso, self.ora_uscita) 
        #arrotondo a due decimali
        self.ore_lavorate_float = round(self.ore_lavorate_float, 2)
        super().save(*args, **kwargs)
    @property
    def ore_lavorate(self):
        return formatta_ore(self.ore_lavorate or 0)

class ReportPresenze(models.Model):
    dipendente = models.ForeignKey('Dipendenti', on_delete=models.CASCADE)
    mese =  models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    anno = models.IntegerField(validators=[MinValueValidator(2000)])
    ore_totali_float = models.DecimalField(max_digits=5, decimal_places=2) #999.99

    def save(self, *args, **kwargs):
        # Calcola le ore totali direttamente dal DB
        ore_lavorate = Presenze.objects.filter(
            dipendente=self.dipendente,
            data__year=self.anno,
            data__month=self.mese
        ).aggregate(Sum('ore_lavorate_float'))['ore_lavorate_float__sum'] or 0

        self.ore_totali_float = round(ore_lavorate, 2)  # Arrotonda a due decimali
        super().save(*args, **kwargs)  # Salva l'oggetto
    @property
    def ore_totali(self):
        return formatta_ore(self.ore_totali_float or 0)



class Bacheca(models.Model):
    titolo=models.CharField(max_length=100)
    messaggio=models.TextField()
    data_pubblicazione=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titolo 


class BustePaga(models.Model):
    dipendente = models.ForeignKey('Dipendenti', on_delete=models.CASCADE)
    mese =  models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    anno = models.IntegerField(validators=[MinValueValidator(2000)])
    importo = models.DecimalField(max_digits=8, decimal_places=2) #max 999 999.99
    data_emissione=models.DateField(auto_now_add=True)
    documento=models.FileField(upload_to='media/documenti_bustepaga/')

    def __str__(self):
        return f"{self.dipendente} - {self.mese}/{self.anno}"

class Notifiche(models.Model):
    dipendente = models.ForeignKey('Dipendenti', on_delete=models.CASCADE)
    messaggio=models.TextField()
    data_invio=models.DateTimeField(auto_now_add=True)
    letto=models.BooleanField(default=False)



class Certificati(models.Model):
    
    nome= models.CharField(max_length=100)
    descrizione=models.TextField()
    documento=models.FileField(upload_to='media/documenti_certificati/')
    data_emissione=models.DateField()
    data_scadenza=models.DateField(null=True)
    dipendente = models.ForeignKey('Dipendenti', on_delete=models.CASCADE)

    def __str__(self):

        return f"{self.nome} - {self.dipendente}"
    
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