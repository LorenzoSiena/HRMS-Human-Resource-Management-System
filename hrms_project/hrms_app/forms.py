from django.contrib.auth import get_user_model

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Dipendenti,Ruoli
from random import randint

class RegisterForm(UserCreationForm):
    nome = forms.CharField(max_length=100)
    cognome = forms.CharField(max_length=100)
    indirizzo_email = forms.EmailField(required=True)
    data_assunzione = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    ruolo = forms.ModelChoiceField(queryset=Ruoli.objects.all(), required=False)
    stipendio = forms.DecimalField(max_digits=10, decimal_places=2,min_value=0)
    documento_contratto = forms.FileField(required=False)
    
    superiore = forms.ModelChoiceField(queryset=Dipendenti.objects.all(), required=False) #da filtrare

    telefono = forms.CharField(max_length=15)
    indirizzo_completo = forms.CharField(max_length=200)
    codice_fiscale = forms.CharField(max_length=16)
    data_nascita = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Dipendenti
        fields = ['nome', 'cognome','data_nascita','codice_fiscale','indirizzo_email','telefono','indirizzo_completo','data_assunzione', 'ruolo','superiore', 'stipendio', 'documento_contratto','password1', 'password2']

    def save(self, commit=True):
        # Creiamo l'istanza del modello senza salvarla nel database
        dipendente: Dipendenti = super().save(commit=False)

        # Assegnazione dei campi personalizzati
        dipendente.nome = self.cleaned_data['nome']
        dipendente.cognome = self.cleaned_data['cognome']
        dipendente.indirizzo_email = self.cleaned_data['indirizzo_email']
        dipendente.telefono = self.cleaned_data['telefono']
        dipendente.indirizzo_completo = self.cleaned_data['indirizzo_completo']
        dipendente.codice_fiscale = self.cleaned_data['codice_fiscale']
        dipendente.data_nascita = self.cleaned_data['data_nascita']
        dipendente.data_assunzione = self.cleaned_data['data_assunzione']
        dipendente.ruolo = self.cleaned_data.get('ruolo')
        dipendente.superiore = self.cleaned_data.get('superiore')
        dipendente.stipendio = self.cleaned_data['stipendio']
        dipendente.username = dipendente.nome + "." + dipendente.cognome+ str(randint(0, 9999999999))

        # Gestione del file caricato
        if self.cleaned_data.get('documento_contratto'):
            dipendente.documento_contratto = self.cleaned_data['documento_contratto']

        # Impostazione della password
        dipendente.set_password(self.cleaned_data["password1"])

        # Salvataggio nel database se commit=True
        if commit:
            dipendente.save()

        return dipendente
