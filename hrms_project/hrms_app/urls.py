from django.urls import path
from . import views

urlpatterns = [
    
    
    path("home", views.hrms_app,name="home"),

    path("", views.user_login, name="login"),
    path("registrati",views.registrati,name="registrati"),
    path("logout", views.user_logout, name="logout"),
    path("bacheca",views.bacheca,name="bacheca"),



    path("presenza",views.presenze,name="presenze"),
    path("dipendenti",views.dipendenti,name="dipendenti"),
    path("stipendi",views.stipendi,name="stipendi"),
    path("gestione_timbratura",views.gestione_timbratura,name="gestione_timbratura"),
    path("richiedi_ferie",views.richiedi_ferie,name="richiedi_ferie"),
    path("accetta_ferie",views.accetta_ferie,name="accetta_ferie"),
    path("rifiuta_ferie",views.rifiuta_ferie,name="rifiuta_ferie"),
    path("visualizza_busta_paga",views.visualizza_busta_paga,name="visualizza_busta_paga"),
    path("crea_busta_paga",views.crea_busta_paga,name="crea_busta_paga"),
    path("inserisci_dipendente",views.inserisci_dipendente,name="inserisci_dipendente"),
    path("modifica_dipendente",views.modifica_dipendente,name="modifica_dipendente"),
    path("elimina_dipendente",views.elimina_dipendente,name="elimina_dipendente"),


    path("aggiungi_messaggio_bacheca",views.aggiungi_messaggio_bacheca,name="aggiungi_messaggio_bacheca"),
    path("modifica_messaggio_bacheca/<int:id>",views.modifica_messaggio_bacheca,name="modifica_messaggio_bacheca"),

    path("area_modifica_bacheca/<int:id>",views.area_modifica_bacheca,name="area_modifica_bacheca"),

    path("cancella_messaggio_bacheca/<int:id>",views.cancella_messaggio_bacheca,name="cancella_messaggio_bacheca"),
    #path("visualizza_report_mensile",views.report_mensile,name="report_mensile"),
    
    # per resettare la password
    path('reset_password/', views.CustomPasswordResetView.as_view(), name='reset_password'),
    path('hrms_app/reset_password_done', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset_password_confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
]