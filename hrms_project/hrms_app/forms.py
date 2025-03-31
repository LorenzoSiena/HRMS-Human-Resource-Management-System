from django.contrib.auth import get_user_model

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Dipendenti, Ruoli, Ferie, BustePaga
from random import randint
from datetime import date, timedelta
from django.core.validators import MinValueValidator,MaxValueValidator

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


# Form per la richiesta di ferie o permessi
class RichiediAssenza(forms.ModelForm):    

    data_inizio = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','type': 'date', 'min': date.today}))  
    ora_inizio = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control hidden','type': 'time', 'min': '09:00', 'max': '18:00'}), required = False)
    data_fine = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','type': 'date', 'min': date.today}))
    ora_fine = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control hidden','type': 'time', 'min': '09:00', 'max': '18:00'}), required = False)
    motivo = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control motivo hidden', 'rows': 2}), required = False)

    class Meta:
        model = Ferie
        fields = ['data_inizio', 'ora_inizio', 'data_fine', 'ora_fine', 'motivo']

#class EditUserForm(RegisterForm):
class EditUserForm(forms.ModelForm):
    class Meta:
        model = Dipendenti
        #fields = [field for field in RegisterForm.Meta.fields if field not in ['password1', 'password2']]
        fields = ['first_name', 'last_name','data_nascita','codice_fiscale','email','telefono','indirizzo_completo','data_assunzione', 'ruolo','superiore', 'stipendio', 'documento_contratto']


    first_name = forms.CharField(  
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': '', 'placeholder': 'Nome'})
    )

    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cognome'})
    )
    email = forms.EmailField(
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
            field.widget.attrs['disabled'] = 'disabled'#
            if isinstance(field.widget, forms.TextInput) or isinstance(field.widget, forms.EmailInput):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs.update({'class': 'form-control', 'type': 'date'})
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class': 'form-control'})

class CaricaBustaPaga(forms.ModelForm):

    id = forms.IntegerField(widget=forms.HiddenInput())

    mese = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12, 'placeholder': 'Mese (1-12)', 'disabled': 'disabled'})
    )

    anno = forms.IntegerField(
        validators=[MinValueValidator(2000)],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 2000, 'placeholder': 'Anno (2000+)', 'disabled': 'disabled'})
    )

    importo = forms.DecimalField(
        label="Importo",
        max_digits=10, 
        decimal_places=2,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Importo', 'min': 0, 'disabled': 'disabled'})
    )    
        
    documento = forms.FileField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx', 'disabled': 'disabled'})
    )

    class Meta:
        model = BustePaga
        fields = ['id', 'mese', 'anno', 'importo', 'documento']

    