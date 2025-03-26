#Standard imports
from django.shortcuts import render,redirect
from django.http import HttpRequest
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect



from django.contrib.auth.models import User,Group
from .models import *

#Form
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout

#Password reset
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordResetForm

#Date
from datetime import datetime ,date , time

# Funzione per gestire il caricamento della HOME
def hrms_app(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('login')
    # Verifico se esiste una timbratura di sola entrata con la data odierna
    dipendente = Dipendenti.objects.get(id = request.user.id)  # Dipendente loggato
    # Se non esiste imposto per la timbrature di entrata
    if Presenze.objects.filter(dipendente = dipendente, data = date.today(), ora_uscita = None).last() is None:
        text_button = "Timbra Entrata"
    # Se esiste imposto per la timbrature di uscita
    else:
        text_button = "Timbra Uscita"
    # Lista delle timbrature da visualizzare - Solo quelle della data odierna
    lista_presenze = Presenze.objects.filter(dipendente = dipendente, data = date.today()) # Lista timbrature odierna
    # Visualizza i messagi della bacheca
    messaggi_bacheca = Bacheca.objects.all().order_by('data_pubblicazione')    

    return render(request,'hrms_app/home.html', {'text_button': text_button, 'lista_presenze': lista_presenze, 'messaggi_bacheca': messaggi_bacheca })

# Funzione per gestire le timbrature
def gestione_timbratura(request: HttpRequest):
    if request.method == "POST":    
        dipendente = Dipendenti.objects.get(id = request.user.id) # Dipendente loggato
        lista_presenze = Presenze.objects.filter(dipendente = dipendente, data = date.today()) # Lista timbrature odierna
        messaggio_errore = ""
        # Verifico se l'utente ha gia' timbrato l'entrata nella data corrente    
        if Presenze.objects.filter(dipendente = dipendente, data = date.today(), ora_uscita = None).last() is None:
            # Se l'utente non ha ancora timbrato nella data corrente, procedo con la inserimento dell'entrata
            try:
                Presenze.objects.create(data = date.today(), ora_ingresso = datetime.now().time(), dipendente = dipendente)
                text_button = "Timbra Uscita"
            except Exception as e:
                messaggio_errore = f"⚠️ Errore nella creazione dell'entrata!, errore: " + str(e)
        else:
            # Se l'utente ha gia' timbrato nella data corrente, proseguo con l'inserimento della data di uscita
            try:
                presenza = Presenze.objects.filter(dipendente = dipendente, data = date.today()).last() # Prendo l'ultima riga generata con la data corrente
                presenza.ora_uscita = datetime.now().time() # Aggiorno l'orario di uscita
                presenza.save()
                text_button = "Timbra Entrata"
            except Exception as e:
                messaggio_errore = f"⚠️ Errore nella creazione dell'uscita!, errore: " + str(e)
        return redirect('home')       
    return render(request, 'hrms_app/home.html', {'text_button': text_button, 'lista_presenze' : lista_presenze, 'messaggio_errore': messaggio_errore})
   

def profilo(request:HttpRequest):
    return render(request,'hrms_app/profilo.html')


def inserisci_dipendente(request: HttpRequest):
    if request.method == "POST":
        nome = request.POST.get('nome', '').strip()
        cognome = request.POST.get('cognome', '').strip()
        email = request.POST.get('email', '').strip()
        ruolo = request.POST.get('ruolo', '').strip()
        data_assunzione = request.POST.get('data_assunzione', '').strip()
        livello_accesso = request.POST.get('livello_accesso', '').strip()

        if nome and cognome and email and ruolo and data_assunzione and livello_accesso:
            Dipendenti.objects.create(
                nome=nome,
                cognome=cognome,
                email=email,
                ruolo=ruolo,
                data_assunzione=data_assunzione,
                livello_accesso=livello_accesso
            )
            messages.success(request, f"✅ Dipendente '{nome} {cognome}' aggiunto con successo!")
        else:
            messages.error(request, "⚠️ Tutti i campi sono obbligatori!")

    return redirect('dipendenti')

def modifica_dipendente(request: HttpRequest, id_dipendente):
    dipendente = get_object_or_404(Dipendenti, id=id_dipendente)

    if request.method == "POST":
        nome = request.POST.get('nome', '').strip()
        cognome = request.POST.get('cognome', '').strip()
        email = request.POST.get('email', '').strip()
        ruolo = request.POST.get('ruolo', '').strip()
        data_assunzione = request.POST.get('data_assunzione', '').strip()
        livello_accesso = request.POST.get('livello_accesso', '').strip()

        if nome and cognome and email and ruolo and data_assunzione and livello_accesso:
            dipendente.nome = nome
            dipendente.cognome = cognome
            dipendente.email = email
            dipendente.ruolo = ruolo
            dipendente.data_assunzione = data_assunzione
            dipendente.livello_accesso = livello_accesso
            dipendente.save()
            messages.success(request, f"✅ Dipendente '{nome} {cognome}' modificato con successo!")
        else:
            messages.error(request, "⚠️ Tutti i campi sono obbligatori!")

def elimina_dipendente(request: HttpRequest, id_dipendente):
    dipendente = get_object_or_404(Dipendenti, id=id_dipendente)
    dipendente.delete()
    messages.success(request, f"🗑️ Dipendente '{dipendente.nome} {dipendente.cognome}' eliminato con successo!")
    return redirect('dipendenti')

def presenze(request:HttpRequest):
    return render(request,'hrms_app/presenza.html')


def stipendi(request:HttpRequest):
    return render(request,'hrms_app/stipendi.html')
    




def richiedi_ferie():
    pass

def accetta_ferie():
    pass

def rifiuta_ferie():
    pass

def archivia_documenti():
    pass

def notifiche_mail():
    pass

def bacheca(request:HttpRequest):
    messaggi = Bacheca.objects.all().order_by('data_pubblicazione')
    if not messaggi.exists():
      messages.info(request,f"La tua Bacheca è vuota!")
      return render(request,"hrms_app/bacheca.html")
                    
    else:
         return render(request,"hrms_app/bacheca.html",{'messaggi':messaggi})

def area_modifica_bacheca(request:HttpRequest,id):
    messaggio = Bacheca.objects.get(id=id)
    return render(request,'hrms_app/modifica_bacheca.html', {'messaggio': messaggio})

def modifica_messaggio_bacheca(request:HttpRequest,id):
    messaggio = Bacheca.objects.get(id=id)
    if request.method == "POST":
        nuovo_titolo = request.POST.get('titolo', '').strip()
        nuovo_messaggio = request.POST.get('messaggio', '').strip()

        if nuovo_titolo and nuovo_messaggio:
            messaggio.titolo = nuovo_titolo
            messaggio.messaggio = nuovo_messaggio
            messaggio.save()
            messages.success(request, "✏️ Messaggio  modificato con successo!")
            return redirect('bacheca') # serve???
        else:
            messages.error(request, "⚠️ Titolo e messaggio sono obbligatori!")

    return render(request, 'hrms_app/bacheca.html', {'messaggio': messaggio})



def aggiungi_messaggio_bacheca(request:HttpRequest):
    if request.method == "POST":
        titolo=request.POST.get('titolo').strip()
        messaggio=request.POST.get('messaggio').strip()
        if titolo and messaggio:
            Bacheca.objects.create(titolo=titolo, messaggio=messaggio)
            messages.success(request,f"✅ Messaggio '{titolo}' aggiunto con successo!")
        else:
            messages.error(request,"⚠️ Titolo e messaggio sono obbligatori!") 
            return render(request,'hrms_app/bacheca.html')        
    return redirect('bacheca')


def cancella_messaggio_bacheca(request: HttpRequest,id):
    messaggio = Bacheca.objects.get(id=id)
    messaggio.delete()
    messages.success(request, "🗑️ Messaggio  eliminato con successo!")
    return redirect('bacheca')

def crea_busta_paga():
    pass

def visualizza_busta_paga():
    pass





def visualizza_report_presenze(request:HttpRequest):
    pass

def visualizza_report_ferie(request:HttpRequest):
    pass

def visualizza_report_permessi(request:HttpRequest):
    pass



def visualizza_report_mensile(request:HttpRequest):
    pass




def registrati(request: HttpRequest):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # Salva l'utente
            # login(request, user)  # (Opzionale) Logga l'utente automaticamente
            messages.success(request, "Registrazione completata con successo!")
            return redirect("login")  
        else:
            messages.error(request, "Errore nella registrazione. Controlla i dati inseriti.")
    else:
        form = RegisterForm()  # Creazione di un form vuoto se è una GET

    return render(request, "hrms_app/register_forms.html", {"form": form})
"""
OLD REGISTER

 def register(request: HttpRequest):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            form.add_error('email','Questa mail è già in uso')
        if form.is_valid():
            user = form.save() #salva l'user e ne crea una copia dummy
            login(request,user) #Effettua il login automatico
            return redirect('home')
    else:
        form = RegisterForm() 
    return render(request,'hrms_app/register.html',{'form':form})
"""

# Login
def user_login(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('home')
    if request.user.is_authenticated:   
        return redirect('home')

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request,username=email,password=password)        
        if user is not None:
            login(request, user)            
            return redirect('home')                  
        else:
            messages.error(request,'Utente non trovato o password sbagliata:')
    return render(request,'hrms_app/login.html',{'login':login})

def user_logout(request: HttpRequest):
    logout(request)
    return redirect('home')

def richiesta_permessi_ferie(request: HttpRequest):
    if request.method == "POST":       
        # tipo_permesso = request.POST.get("tipo_permesso", "Nessuna selezione") # Prende il valore dal radio button selezionato nel form
        tipo_permesso=""
        data_inizio = request.POST.get("data_inizio", "nessuna selezione") # Prende il valore dal input del form
        ora_inizio = request.POST.get("ora_inizio") # Prende il valore dal input del form
        data_fine = request.POST.get("data_fine") # Prende il valore dal input del form
        ora_fine = request.POST.get("ora_fine") # Prende il valore dal input del form
        motivo = request.POST.get("motivo") # Prende il valore dal input del form
        dipendente = Dipendenti.objects.get(id = request.user.id) # Dipendente loggato

        return render(request, 'hrms_app/home.html', {"tipo_permesso": tipo_permesso, "data_inizio": data_inizio, "ora_inizio": ora_inizio, "data_fine": data_fine, "ora_fine": ora_fine, "motivo": motivo, "dipendente": dipendente})

#RESETTO LA PASSWORD

class CustomPasswordResetView(PasswordResetView):
    template_name = "hrms_app/reset_password.html"  # Il template per richiedere il reset
    # password_reset_done deve essere il nome del name in urls
    success_url = reverse_lazy('password_reset_done')  # Deve reindirizzare dopo la richiesta
    email_template_name = 'hrms_app/reset_password_email.html'  # Il template dell'email
    form_class = PasswordResetForm

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'hrms_app/reset_password_done.html'  # Template di conferma richiesta

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'hrms_app/reset_password_confirm.html'  # Template per inserire la nuova password
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'hrms_app/reset_password_complete.html'  # Messaggio di avvenuto reset




