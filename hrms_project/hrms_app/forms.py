from django.contrib.auth import get_user_model

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Dipendenti,Ruoli
from random import randint

class RegisterForm(UserCreationForm):
    nome = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': '', 'placeholder': 'Nome'})
    )

    cognome = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cognome'})
    )
    indirizzo_email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
        
    )
                                       
    data_assunzione = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','type': 'date'}))

    ruolo = forms.ModelChoiceField(
        queryset=Ruoli.objects.all(), 
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    stipendio = forms.DecimalField(
        max_digits=10, 
        decimal_places=2,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stipendio'})
    )
    documento_contratto = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    
    superiore = forms.ModelChoiceField(
        queryset=Dipendenti.objects.all(), 
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    ) #da filtrare

    telefono = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefono'})
    )
    indirizzo_completo = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Indirizzo Completo'})
    )
    
    codice_fiscale = forms.CharField(max_length=16,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Codice Fiscale'})
    )
    
    data_nascita = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control','type': 'date'})
    )
    
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


    def __init__(self, *args, **kwargs):
            super(RegisterForm, self).__init__(*args, **kwargs)

            # Aggiunge classi Bootstrap ai campi generati automaticamente
            for field_name, field in self.fields.items():
                if isinstance(field.widget, forms.TextInput) or isinstance(field.widget, forms.EmailInput) or isinstance(field.widget, forms.PasswordInput):
                    field.widget.attrs.update({'class': 'form-control'})
                elif isinstance(field.widget, forms.Select):
                    field.widget.attrs.update({'class': 'form-select'})
                elif isinstance(field.widget, forms.DateInput):
                    field.widget.attrs.update({'class': 'form-control', 'type': 'date'})
                elif isinstance(field.widget, forms.FileInput):
                    field.widget.attrs.update({'class': 'form-control'})



class EditUserForm(RegisterForm):
    class Meta:
        model = Dipendenti
        #fields = [field for field in RegisterForm.Meta.fields if field not in ['password1', 'password2']]
        fields = ['first_name', 'last_name','data_nascita','codice_fiscale','email','telefono','indirizzo_completo','data_assunzione', 'ruolo','superiore', 'stipendio', 'documento_contratto']

    def save(self, commit=True):
        dipendente: Dipendenti = super().save(commit=False)

        # Se commit è True, salva le modifiche nel database
        if commit:
            dipendente.save()

        return dipendente

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)

        # Aggiunge classi Bootstrap ai campi per uniformare lo stile con RegisterForm
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput) or isinstance(field.widget, forms.EmailInput):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs.update({'class': 'form-control', 'type': 'date'})
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class': 'form-control'})

