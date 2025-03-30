#Standard imports
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpRequest
from django.contrib import messages

from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Permission
from hrms_app.constant import PERMESSI_APP



from django.contrib.auth.models import User,Group
from .models import *

#Form

from .forms import RegisterForm, RichiediAssenza, EditUserForm, CaricaBustaPaga

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
    # Visualizza i messagi della bacheca
    messaggi_bacheca = Bacheca.objects.all().order_by('data_pubblicazione')
    # Verifico se esiste una timbratura di sola entrata con la data odierna
    dipendente = Dipendenti.objects.get(id = request.user.id)  # Dipendente loggato
    # Se non esiste imposto per la timbrature di entrata
    if Presenze.objects.filter(dipendente = dipendente, data = date.today(), ora_uscita = None).last() is None:
        button_timbra = "Timbra Entrata"
    # Se esiste imposto per la timbrature di uscita
    else:
        button_timbra = "Timbra Uscita"
    # Lista delle timbrature da visualizzare - Solo quelle della data odierna
    lista_presenze = Presenze.objects.filter(dipendente = dipendente, data = date.today()) # Lista timbrature odierna
    # Carico il form per la richiesta di permessi o ferie
    form = RichiediAssenza()
    lista_ferie = Ferie.objects.filter(dipendente = dipendente, stato = "In attesa")
    lista_permessi = Permessi.objects.filter(dipendente = dipendente, stato = "In attesa")
    return render(request,'hrms_app/home.html', {'messaggi_bacheca': messaggi_bacheca, 'button_timbra': button_timbra, 'lista_ferie': lista_ferie, 'lista_permessi': lista_permessi, 'form': form, 'lista_presenze': lista_presenze})

# Funzione per gestire le timbrature
def gestione_timbratura(request: HttpRequest):
    if request.method == "POST":    
        dipendente = Dipendenti.objects.get(id = request.user.id) # Dipendente loggato      
        # Verifico se l'utente ha gia' timbrato l'entrata nella data corrente    
        if Presenze.objects.filter(dipendente = dipendente, data = date.today(), ora_uscita = None).last() is None:
            # Se l'utente non ha ancora timbrato nella data corrente, procedo con la inserimento dell'entrata
            try:
                Presenze.objects.create(data = date.today(), ora_ingresso = datetime.now().time(), dipendente = dipendente)
            except Exception as e:
                messages.success(request,f"⚠️ Errore nella creazione dell'entrata!, errore: " + str(e))
        else:
            # Se l'utente ha gia' timbrato nella data corrente, proseguo con l'inserimento della data di uscita
            try:
                presenza = Presenze.objects.filter(dipendente = dipendente, data = date.today()).last() # Prendo l'ultima riga generata con la data corrente
                presenza.ora_uscita = datetime.now().time() # Aggiorno l'orario di uscita
                presenza.save()
            except Exception as e:
                messages.success(request,f"⚠️ Errore nella creazione dell'uscita!, errore: " + str(e))
    return redirect('home')

def profilo(request:HttpRequest):
    return render(request,'hrms_app/profilo.html')


def crea_dipendente(request: HttpRequest):
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






def report(request:HttpRequest):
    return render(request,'hrms_app/report.html')


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
            return redirect('bacheca') 
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


def aggiungi_dipendente(request:HttpRequest):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Creazione completata con successo!")
            return redirect("gestione_dipendenti")  
        else:
            messages.error(request, "Errore nella creazione. Controlla i dati inseriti.")
    else:
        form = RegisterForm()  # Creazione di un form vuoto se è una GET

    return render(request, "hrms_app/aggiungi_dipendente.html", {"form": form})
    

def modifica_dipendente(request: HttpRequest, id):
    dipendente = Dipendenti.objects.get(id=id)  # Recupera l'utente esistente
    if request.method == "POST":
        form = EditUserForm(request.POST, request.FILES, instance=dipendente)  # Passa l'istanza
        if form.is_valid():
            form.save()  # Modifica solo i campi cambiati
            messages.success(request,f" Dipendente '{dipendente.nome} {dipendente.cognome}' modificato con successo!")
            return redirect('gestione_dipendenti')
        else:
            messages.error(request,f" Campi errati!",)


    else:
        form = EditUserForm(instance=dipendente)  # Precompila il form
    return render(request, 'hrms_app/modifica_dipendente.html', {'form': form, 'dipendente': dipendente})






def elimina_dipendente(request: HttpRequest, id):
    dipendente = get_object_or_404(Dipendenti, id=id)
    dipendente.delete()
    messages.success(request, f"🗑️ Dipendente '{dipendente.nome} {dipendente.cognome}' eliminato con successo!")
    return redirect('gestione_dipendenti')





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


from django.urls import reverse

def vai_all_admin(request):
    return redirect(reverse('admin:index'))  # Ricava l'URL dinamicamente






# Login
def user_login(request: HttpRequest):
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

# Funzione per la richiesta permessi e ferie
def richiesta_permessi_ferie(request: HttpRequest):
    if request.method == "POST":
        tipo_permesso = request.POST.get("tipo_permesso", "Nessuna selezione") # Prende il valore dal radio button selezionato nel form
        form = RichiediAssenza(request.POST)
        if form.is_valid():
            data_inizio = form.cleaned_data['data_inizio']
            ora_inizio = form.cleaned_data['ora_inizio']
            data_fine = form.cleaned_data['data_fine']
            ora_fine = form.cleaned_data['ora_fine']
            motivo = form.cleaned_data['motivo']
            dipendente = Dipendenti.objects.get(id = request.user.id)
            # Controllo che la data fine sia maggiore o uguale alla data inizio
            if not(data_inizio < data_fine):
                messages.error(request, 'Errore nella richiesta: La data fine deve essere maggiore o uguale alla data inizio.')
                return redirect('home')
            if tipo_permesso == "ferie":
                Ferie.objects.create(dipendente = dipendente, data_inizio = data_inizio, data_fine = data_fine, stato = "In attesa") 
                messages.success(request, 'Assenza per Ferie richiesta con successo!')               
            elif tipo_permesso == "permesso" or tipo_permesso == "permesso_nr":
                # Controllo che le ore di ingresso e uscita siano tra le 9.00 e le 18.00
                if ora_inizio < datetime.strptime('09:00', '%H:%M').time() or ora_inizio > datetime.strptime('18:00', '%H:%M').time():
                    messages.error(request, 'Errore nella richiesta: Le ore di ingresso devono essere tra le 9.00 e le 18.00.')
                    return redirect('home')
                if ora_fine < datetime.strptime('09:00', '%H:%M').time() or ora_fine > datetime.strptime('18:00', '%H:%M').time():
                    messages.error(request, 'Errore nella richiesta: Le ore di uscita devono essere tra le 9.00 e le 18.00.')
                    return redirect('home')
                # Controllo che l'ora di uscita sia maggiore dell'ora di ingresso nei permessi dello stesso giorno
                if data_inizio == data_fine and ora_inizio > ora_fine:
                    messages.error(request, "Errore nella richiesta: Le ore di uscita deve essere maggiore dell'ora di entrata")
                    return redirect('home')
                retribuito = (tipo_permesso == "permesso")
                Permessi.objects.create(dipendente = dipendente, data_ora_inizio = datetime.combine(data_inizio, ora_inizio), data_ora_fine = datetime.combine(data_fine, ora_fine), stato = "In attesa", retribuito = retribuito, motivo = motivo)
                messages.success(request, 'Permesso richiesto con successo!')
        return redirect('home')        

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


#-------------------------navigazione e render delle pagine---------------------------------------------------------------------

def documenti_personali(request:HttpRequest):
    return render(request,'hrms_app/documenti_personali.html')



def busta_paga(request:HttpRequest):
    return render(request,'hrms_app/busta_paga.html')

def gestione_dipendenti(request:HttpRequest):
    if request.method == "POST":
        dipendente = request.POST.get("dipendente")
        origine_form = request.POST.get("origine_form")
        #ricerca incrociata su nome e cognome dove %dipendente%
        #lista_dipendenti = Dipendenti.objects.filter(nome=dipendente,cognome=dipendente)
        lista_dipendenti = Dipendenti.objects.filter(Q(first_name__icontains=dipendente) | Q(last_name__icontains=dipendente))
        if lista_dipendenti:
            messages.success(request, "Utenti trovati")
        else:
            messages.error(request, "Nessun dipendente trovato")    

        if origine_form == "ruoli":
            ruoli = Ruoli.objects.all()
            return render(request, "hrms_app/gestione_ruoli.html", {"dipendenti": lista_dipendenti, "ruoli": ruoli})
        elif origine_form == "report":
            return render(request, "hrms_app/report.html", {"dipendenti": lista_dipendenti})
        else:
            return render(request, "hrms_app/gestione_dipendenti.html", {"dipendenti": lista_dipendenti})
        

    return render(request, "hrms_app/gestione_dipendenti.html")



def assegna_ruolo(request:HttpRequest):
    if request.method == "POST":
        id_dipendente = request.POST.get("dipendente")
        id_ruolo = request.POST.get("ruolo")
        dipendente = Dipendenti.objects.get(id=id_dipendente)
        dipendente.ruolo = Ruoli.objects.get(id=id_ruolo)
        dipendente.save()
        messages.success(request, f"Ruolo assegnato con successo {dipendente.nome} {dipendente.cognome} -> {dipendente.ruolo}")
    return redirect("gestione_ruoli")



    
def gestione_assenze(request:HttpRequest):
    return render(request,'hrms_app/gestione_assenze.html')

def gestione_busta_paga(request: HttpRequest):
    if request.method == "POST":
        dipendente = request.POST.get("dipendente")        
        #Ricerca incrociata su nome e cognome dove %dipendente%    
        lista_dipendenti = Dipendenti.objects.filter(Q(first_name__icontains=dipendente) | Q(last_name__icontains=dipendente))
        if lista_dipendenti:
            messages.success(request, "Utenti trovati")
        else:
            messages.error(request, "Nessun dipendente trovato")
        form_carica_busta = CaricaBustaPaga(request.POST)       

        return render(request, 'hrms_app/gestione_busta_paga.html', {"lista_dipendenti": lista_dipendenti, "form_carica_busta": form_carica_busta})        
    return render(request, 'hrms_app/gestione_busta_paga.html')

def salva_busta_paga(request: HttpRequest):  
    if request.method == "POST":
        form_carica_busta = CaricaBustaPaga(request.POST)
        if form_carica_busta.is_valid():
            mese = form_carica_busta.cleaned_data['mese']
            anno = form_carica_busta.cleaned_data['anno']
            importo = form_carica_busta.cleaned_data['importo']
            documento = form_carica_busta.cleaned_data['documento']
            dipendente = Dipendenti.objects.get(id = id)
            
            #busta_paga = form_carica_busta.save(commit=False)
            #busta_paga.save()
            messages.success(request, "Busta paga caricata con successo")
            return redirect('gestione_busta_paga' , 'dipendente' , dipendente , 'anno' , anno , 'mese' , mese, 'documento' , documento, 'importo' , importo)
        else:
            messages.error(request, "Errore nel caricamento della busta paga")
            return redirect('gestione_busta_paga')
    return redirect('gestione_busta_paga')

def consulta_documenti(request:HttpRequest):
    return render(request,'hrms_app/consulta_documenti.html')

def cerca_report_mensile(request:HttpRequest):
    report_mensile = []
    if request.method == "POST":
        # Assicurati che i parametri 'id', 'month', e 'year' siano presenti
        if request.POST.get('dipendente') and request.POST.get('month') and request.POST.get('year'):
            dipendente_id = request.POST.get('dipendente')
            month = int(request.POST.get('month'))
            year = int(request.POST.get('year'))

            # Filtro il dipendente
            dipendente = Dipendenti.objects.get(id=dipendente_id)

            # Recupero i report per ferie, permessi e presenze
            ferie = ReportFerie.objects.filter(dipendente=dipendente, mese=month, anno=year)
            permessi = ReportPermessi.objects.filter(dipendente=dipendente, mese=month, anno=year)
            presenze = ReportPresenze.objects.filter(dipendente=dipendente, mese=month, anno=year)

            # Preparo i dati da passare alla vista
            report_mensile = [{
                'dipendente': dipendente,
                'giorni_totali_ferie': ferie.giorni_totali if ferie else 0,
                'ore_totali_permessi': permessi.ore_totali_permessi if permessi else 0,
                'ore_totali_presenze': presenze.ore_totali if presenze else 0,
            }]

    return render(request, 'hrms_app/report.html', {'report_mensile': report_mensile})


# def aggiungi_dipendente(request:HttpRequest):
#     return render(request,'hrms_app/aggiungi_dipendente.html')




def gestione_ruoli(request:HttpRequest):
    ruoli = Ruoli.objects.all()
    return render(request,'hrms_app/gestione_ruoli.html',{'ruoli':ruoli})

#controllare validation!

def crea_ruolo(request: HttpRequest):


    if request.method == "POST":
        ruolo = request.POST.get("name") # testo
        livello_accesso = request.POST.get("livello_accesso") #numero

        if not ruolo or not livello_accesso:

            messages.error(request, f"Errore nella creazione del ruolo. {ruolo} livello {livello_accesso} Controlla i dati inseriti.")
            return redirect("gestione_ruoli")

        # Controlla se esiste già un Group con quel nome
        gruppo_esistente = Group.objects.filter(name=ruolo).first()

        if gruppo_esistente and Ruoli.objects.filter(ruolo=gruppo_esistente).exists():
            messages.error(request, "Ruolo già esistente.")
            return redirect("gestione_ruoli")

        # Crea il gruppo se non esiste
        if not gruppo_esistente:
            gruppo_esistente = Group.objects.create(name=ruolo)

        # Crea il ruolo associato
        Ruoli.objects.create(ruolo=gruppo_esistente, livello_accesso=int(livello_accesso))
        messages.success(request, f"Creazione ruolo {ruolo} avvenuta con successo!")
        #return render(request,'hrms_app/gestione_ruoli.html') 
        return redirect("gestione_ruoli") 

    return render(request,'hrms_app/gestione_ruoli.html')

""" 
SELECT *
FROM ruoli JOIN Group 
ON ruoli.ruolo_id = Group.id
WHERE Group.name = 'Contabile';
"""          



""" 
Gestione dipendenti (crea,modifica,visualizza,elimina)
Gestire Ruoli(crea,modifica,visualizza,elimina)
Gestire Autorizzazioni(assegna a ruolo,rimuovi da ruolo,visualizza autorizzazioni per ruolo)
Gestire Ferie/Permessi(accetta,rifiuta,visualizza)
Visualizza Report(ferie,permessi,presenze)
Gestire messaggi bacheca (Crea,modifica,elimina)
Gestire Buste paga (Crea,carica file,elimina,visualizza)
Gestire documenti [contratti e certificati] (visualizza,modifica,elimina)
 """


def cerca_ruolo_id(request:HttpRequest):
    ruoli = Ruoli.objects.all()
    if request.method == "GET":    
        id = request.GET.get("id")
        if id:
            ruolo = Ruoli.objects.get(id=id)
            if not ruolo:
                messages.error(request, f"Ruolo non trovato.")
                return redirect("gestione_ruoli")

            permessi_disponibili = {}
            permessi_ruolo = set(ruolo.ruolo.permissions.values_list('codename', flat=True))

            for nome_permesso, permessi_richiesti in PERMESSI_APP.items():
                permessi_disponibili[nome_permesso] = all(p in permessi_ruolo for p in permessi_richiesti)
            
            return render(request,'hrms_app/gestione_ruoli.html',{"ruolo":ruolo,'permessi_disponibili': permessi_disponibili,'ruoli':ruoli}) 

    return redirect('gestione_ruoli')

def cerca_ruolo(request:HttpRequest):

    if request.method == "GET":    
        name = request.GET.get("name")
        if name:
            ruolo = Ruoli.objects.filter(ruolo__name__icontains=name).first()
            if not ruolo:
                messages.error(request, f"Ruolo non trovato.")
                return redirect("gestione_ruoli")

            permessi_disponibili = {}
            permessi_ruolo = set(ruolo.ruolo.permissions.values_list('codename', flat=True))

            for nome_permesso, permessi_richiesti in PERMESSI_APP.items():
                permessi_disponibili[nome_permesso] = all(p in permessi_ruolo for p in permessi_richiesti)
            
            return render(request,'hrms_app/gestione_ruoli.html',{"ruolo":ruolo,'permessi_disponibili': permessi_disponibili}) 

    return redirect('gestione_ruoli')




def modifica_autorizzazioni(request: HttpRequest, id):
    ruoli = Group.objects.all()
    if request.method == "POST":

        permessi_selezionati = request.POST.getlist("permessi")  # Ottieni solo quelli selezionati
        permessi_nuovi = []

        for gruppo, permessi_richiesti in PERMESSI_APP.items():
            if gruppo in permessi_selezionati:
                # Aggiungi i permessi richiesti per il gruppo selezionato
                permessi_nuovi.extend(Permission.objects.filter(codename__in=permessi_richiesti))

        ruolo = Group.objects.get(id=id) 
        ruolo.permissions.set(permessi_nuovi)
        messages.success(request, f"✅ Ruolo aggiornato con successo!")
        return render(request,'hrms_app/gestione_ruoli.html',{'ruoli':ruoli})

    return render(request, 'hrms_app/gestione_ruoli.html', {
        'ruolo': ruolo,'ruoli':ruoli
    })








@login_required
def mostra_permessi(request):
    permessi_individuali = request.user.get_all_permissions()  # Restituisce un set di permessi (app_label.codename)

    permessi_ruolo = set()
    ruolo=request.user.ruolo
    if ruolo:  # Se l'utente ha un ruolo assegnato
        permessi_ruolo = set(request.user.ruolo.ruolo.permissions.values_list('codename', flat=True))
    
    
    return render(request, 'hrms_app/debug_permessi.html', {'permessi_individuali': permessi_individuali, 'permessi_ruolo':permessi_ruolo,'ruolo': ruolo})

def notifiche(request:HttpRequest):
    return render(request,'hrms_app/notifiche.html')

