from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from datetime import datetime,date
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from django.db.models import Sum
from .utils import calcola_ore_lavorate,formatta_ore  # Importiamo la funzione per il calcolo delle ore lavorate

class Dipendenti(AbstractUser):
    #email == username!!!
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    data_assunzione = models.DateField()
    superiore = models.ForeignKey("Dipendenti", on_delete=models.SET_NULL, null=True)
    ruolo = models.ForeignKey("Ruoli", on_delete=models.SET_NULL, null=True)
    stipendio = models.DecimalField(max_digits=10, decimal_places=2)
    documento_contratto = models.FileField( upload_to='media/documenti_contratti/', null=True, blank=True)
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





class Autorizzazioni(models.Model):
    nome=models.CharField(max_length=100,unique=True) #: 'gestione_dipendenti', 'approva_ferie'
    descrizione=models.TextField()




class Ruoli(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    livello_accesso = models.IntegerField(validators=[MinValueValidator(1)]) #solo positivi
    descrizione = models.TextField()
    autorizzazioni = models.ManyToManyField(Autorizzazioni)








# FIXARE IL CALCOLO DEL TEMPO


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

class Permessi(Ferie): 
    retribuito=models.BooleanField()
    orario_inizio=models.DateTimeField()
    orario_fine=models.DateTimeField()

#report permessi
class ReportPermessi(models.Model):
    dipendente = models.ForeignKey('Dipendenti', on_delete=models.CASCADE)
    mese =  models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    anno = models.IntegerField(validators=[MinValueValidator(2000)])
    #TODO calcolo permessi totali nel mese
    permessi_totali = models.DecimalField(max_digits=5, decimal_places=2) #999.99
    









#------------------------------------2test------------------------------------------------
#OK MA DA TESTARE
class Presenze(models.Model):

    data = models.DateField()
    ora_ingresso=models.TimeField()  #'14:30:00'
    ora_uscita=models.TimeField(null=True,blank=True) #'17:30:00'
    dipendente = models.ForeignKey('Dipendenti', on_delete=models.CASCADE)
    ore_lavorate = models.FloatField(null=True, blank=True) 

    def save(self, *args, **kwargs):
        self.ore_lavorate = calcola_ore_lavorate(self.ora_ingresso, self.ora_uscita)
        super().save(*args, **kwargs)


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
        ).aggregate(Sum('ore_lavorate'))['ore_lavorate__sum'] or 0

        self.ore_totali_float = round(ore_lavorate, 2)  # Arrotonda a due decimali
        super().save(*args, **kwargs)  # Salva l'oggetto
    @property
    def ore_totali(self):
        return formatta_ore(self.ore_totali_float or 0)
#------------------------------------2test------------------------------------------------




class Bacheca(models.Model):
    titolo=models.CharField(max_length=100)
    messaggio=models.TextField()
    data_pubblicazione=models.DateTimeField(auto_now_add=True)




class BustePaga(models.Model):
    dipendente = models.ForeignKey('Dipendenti', on_delete=models.CASCADE)
    mese =  models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    anno = models.IntegerField(validators=[MinValueValidator(2000)])
    importo = models.DecimalField(max_digits=8, decimal_places=2) #max 999 999.99
    data_emissione=models.DateField(auto_now_add=True)
    documento=models.FileField(upload_to='media/documenti_bustepaga/')

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