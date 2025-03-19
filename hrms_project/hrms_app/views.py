# TODO: CONTROLLARE E ADATTARE
 

#Standard imports
from django.shortcuts import render,redirect
from django.http import HttpRequest
from django.contrib import messages


#Model user 
from django.contrib.auth.models import User

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