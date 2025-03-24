from django.contrib.auth import get_user_model

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Dipendenti,Ruoli


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
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['nome']
        user.last_name = self.cleaned_data['cognome']
        user.email = self.cleaned_data['indirizzo_email']
        
        if commit:
            user.save()
        return user


