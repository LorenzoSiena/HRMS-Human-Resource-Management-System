# TODO: CONTROLLARE E ADATTARE
 

#Standard imports
from django.shortcuts import render,redirect
from django.http import HttpRequest
from django.contrib import messages


#Model user 
from django.contrib.auth.models import User
from .models import Dipendenti
from .models import Permessi
from .models import Ruoli
from .models import Ferie
from .models import Presenze
from .models import Bacheca
from .models import ReportPresenze
from .models import BustePaga
from .models import Notifiche

#Form
from .forms import RegisterForm
from django.contrib.auth import authenticate,login,logout

#Password reset
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordResetForm




#User register,login and logout


def hrms_app(request: HttpRequest):
    return render(request,'hrms_app/home.html')

def dipendenti(request:HttpRequest):
    return render(request,'hrms_app/dipendenti.html')



def inserisci_dipendente(request:HttpRequest):
   if request.method =="POST":
    dipendente = Dipendenti.objects.create(
        nome=nome,
        cognome=cognome,
        email=email,
        ruolo=ruolo,
        data_assunzione=data_assunzione,
        livello_accesso=livello_accesso
    )
    messages.success( request , f"✏️ Dipendente '{nome} {cognome}' aggiunto con successo!")
    return redirect ('dipendente')

   



def modifica_dipendente( nome, cognome, email, ruolo, data_assunzione, livello_accesso):
   try:
    dipendente = Dipendenti.objects.get(id = id_dipendente)
    dipendente.nome = nuovo_nome
    dipendente.cognome = nuovo_cognome
    dipendente.email = nuovo_email
    dipendente.ruolo = nuovo_ruolo
    dipendente.data_assunzione = nuovo_data_assunzione
    dipendente.livello_accesso = nuovo_livello_accesso
    dipendente.save()
    print(f"✏️ Dipendente '{id_dipendente}' modificato con successo!")
   except Bacheca.DoesNotExist:
        print(f"⚠️ Dipendente '{id_dipendente}' non trovato.")


def elimina_dipendente():
    pass

def presenze(request:HttpRequest):
    return render(request,'hrms_app/presenze.html')


def stipendi(request:HttpRequest):
    return render(request,'hrms_app/stipendi.html')
    
def richiedi_ferie():
    pass

def archivia_documenti():
    pass

def notifiche_mail():
    pass

def aggiungi_messaggio_bacheca(request:HttpRequest):
    titolo=request.POST.get('titolo')
    messaggio=request.POST.get('messaggio')
    nuovo_messaggio = Bacheca.objects.create(titolo=titolo, messaggio=messaggio)
    messages.success(request,f"✅ Messaggio '{titolo}' aggiunto con successo!")
    return render(request ,'hrms_app/home.html')

def leggi_messaggio_bacheca():
    messaggio = Bacheca.objects.all().order_by('data_pubblicazione')
    if not messaggio:
      return render('hrms_app/home.html',f"La tua Bacheca è vuota!")
    else:
        for msg in messaggio:
         return render(f"[{msg.data_pubblicazione}] {msg.titolo}: {msg.messaggio}")

def modifica_messaggio(msg_id, nuovo_titolo, nuovo_messaggio):
    try:
        messaggio = Bacheca.objects.get(id=msg_id)
        messaggio.titolo = nuovo_titolo
        messaggio.messaggio = nuovo_messaggio
        messaggio.save()
        print(f"✏️ Messaggio '{msg_id}' modificato con successo!")
    except Bacheca.DoesNotExist:
        print(f"⚠️ Messaggio '{msg_id}' non trovato.")

def cancella_messaggio(msg_id):
    try:
        messaggio = Bacheca.objects.get(id=msg_id)
        messaggio.delete()
        print(f"🗑️ Messaggio '{msg_id}' eliminato con successo!")
    except Bacheca.DoesNotExist:
        print(f"⚠️ Messaggio '{msg_id}' non trovato.")

def crea_busta_paga():
    pass

def visualizza_busta_paga():
    pass

def report_mensile():
    pass




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



def user_login(request: HttpRequest):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Utente non trovato o password sbagliata')
    return render(request,'hrms_app/login.html',{'login':login})

def user_logout(request: HttpRequest):
    logout(request)
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