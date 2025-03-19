# Gestione delle Risorse Umane con Django
## Descrizione del Progetto:  
Il progetto consiste nella creazione di un sistema di gestione delle risorse umane (HRMS - Human Resource Management System) per aziende di piccole e medie dimensioni.  
L’applicazione web consentirà di amministrare i dipendenti, registrare presenze, gestire ferie e stipendi, oltre a generare report sulle performance.   
Obiettivi del Progetto   
Centralizzare la gestione del personale.   
Automatizzare la registrazione delle presenze e la gestione delle ferie.   
Fornire un'interfaccia web intuitiva per dipendenti e amministratori.   

### Funzionalità Principali   
## 1. Gestione Dipendenti
Creazione, modifica e rimozione di dipendenti.
Definizione di ruoli aziendali e livelli di accesso.
Archiviazione di documenti (contratti, certificati).

## 2. Presenze e Ferie
Registrazione delle ore di lavoro giornaliere.
Richiesta e approvazione di ferie direttamente dal sito.

## 3. Gestione Buste Paga
Creazione e visualizzazione delle buste paga.
Accesso riservato ai dipendenti per consultare il proprio stipendio.
## 4. Report e Statistiche
Report mensili sulle presenze e le ore lavorate.
Andamento delle ferie e permessi concessi.


## 5. Notifiche e Comunicazioni
Sezione bacheca per comunicazioni aziendali.
Notifiche via email per ferie approvate o nuovi documenti disponibili.

### Tecnologie Utilizzate
Backend: Django
Frontend: HTML, CSS, JavaScript
Database: SQLite
Autenticazione: Django Authentication
Struttura del Progetto Django

hrms_project/           
│── manage.py   
│── hrms_app/    
│   │── models.py  [Modelli per dipendenti, presenze, stipendi]       
│   │── views.py   [Logica di gestione delle richieste]          
│   │── urls.py    [Routing delle pagine]            
│   │── forms.py   [Moduli Django per gestire input utenti]           
│   │── templates/          
│   │   │── base.html          
│   │   │── home.html         
│   │   │── dipendenti.html      
│   │   │── presenze.html       
│   │   │── stipendi.html         
│── static/   [File CSS, JS e immagini]          
│── db.sqlite3  Database locale          


## MODIFICA 1:
Modifica templates/x.html->templates/hrms_app/x.html
per rispettare il namespace
