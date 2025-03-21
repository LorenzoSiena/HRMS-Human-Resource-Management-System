from django.contrib.auth import get_user_model

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Dipendenti,Ruoli


class RegisterForm(UserCreationForm):
    nome = forms.CharField(max_length=100)
    cognome = forms.CharField(max_length=100)
    indirizzo_email = forms.EmailField(required=True)

    #set null? 
    #superiore = models.ForeignKey("Dipendenti", on_delete=models.SET_NULL, null=True)
   
    data_assunzione = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    ruolo = forms.ModelChoiceField(queryset=Ruoli.objects.all(), required=False)
    stipendio = forms.DecimalField(max_digits=10, decimal_places=2)
    documento_contratto = forms.FileField(required=False)

    class Meta:
        model = Dipendenti
        fields = ['indirizzo_email', 'nome', 'cognome', 'password1', 'password2', 'data_assunzione', 'ruolo', 'stipendio', 'documento_contratto']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['nome']
        user.last_name = self.cleaned_data['cognome']
        user.email = self.cleaned_data['indirizzo_email']
        
        if commit:
            user.save()
        return user



""" <form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Registrati</button>
</form>
 """