""" from django.contrib import admin
from .models import Dipendenti
# Register your models here.
admin.site.register(Dipendenti) """
#Test e debug!
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Dipendenti,Ruoli,Bacheca

class DipendentiAdmin(UserAdmin):
    model = Dipendenti
    list_display = ('email', 'nome', 'cognome', 'ruolo', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informazioni personali', {'fields': ('nome', 'cognome', 'telefono', 'data_assunzione', 'ruolo', 'stipendio', 'documento_contratto')}),
        ('Permessi', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Date importanti', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome', 'cognome', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'nome', 'cognome')
    ordering = ('email',)

#admin.site.register(Dipendenti, DipendentiAdmin)
admin.site.register(Dipendenti)
admin.site.register(Ruoli)
admin.site.register(Bacheca)