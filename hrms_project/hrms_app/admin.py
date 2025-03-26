""" from django.contrib import admin
from .models import Dipendenti
# Register your models here.
admin.site.register(Dipendenti) """
#Test e debug!
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Dipendenti,Ruoli

class DipendentiAdmin(UserAdmin):
    model = Dipendenti
    list_display = ('email', 'first_name', 'last_name', 'ruolo', 'is_staff', 'is_active')


    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informazioni personali', {'fields': ('first_name', 'last_name', 'telefono', 'data_assunzione', 'ruolo', 'stipendio', 'documento_contratto')}),
        ('Permessi', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Date e Log', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    def save_model(self, request, obj, form, change):
        """Hash della password solo se viene modificata manualmente"""
        if form.cleaned_data.get('password') and not obj.password.startswith('pbkdf2_'):
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

admin.site.register(Dipendenti, DipendentiAdmin)
admin.site.register(Ruoli)