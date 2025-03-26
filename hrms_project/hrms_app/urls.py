from django.urls import path
from . import views

urlpatterns = [
    
 #-------render delle pagine---------------------------------------------------------------------   
    path("home", views.hrms_app,name="home"),
    path("", views.user_login, name="login"),
    path("registrati",views.registrati,name="registrati"),
    path("logout", views.user_logout, name="logout"),
    path("bacheca",views.bacheca,name="bacheca"),
    path("documenti_personali",views.documenti_personali,name="documenti_personali"),
    path("assenze_personali",views.assenze_personali,name="assenze_personali"),
    path("busta_paga",views.busta_paga,name="busta_paga"),
    path("report",views.report,name="report"),
    path("profilo",views.profilo,name="profilo"),
    path("stipendi",views.stipendi,name="stipendi"),
    path("gestione_dipendenti",views.gestione_dipendenti,name="gestione_dipendenti"),
    path("gestione_assenze",views.gestione_assenze,name="gestione_assenze"),
    path("gestione_busta_paga",views.gestione_busta_paga,name="gestione_busta_paga"),
    path("consulta_documenti",views.consulta_documenti,name="consulta_documenti"),
    path("aggiungi_dipendente",views.aggiungi_dipendente,name="aggiungi_dipendente"),
#----azioni---------------------------------------------------------------------
    path("visualizza_dipendenti",views.visualizza_dipendenti,name="visualizza_dipendenti"),
    
    path("gestione_timbratura",views.gestione_timbratura,name="gestione_timbratura"),
    path("richiedi_ferie",views.richiedi_ferie,name="richiedi_ferie"),
    path("accetta_ferie",views.accetta_ferie,name="accetta_ferie"),
    path("rifiuta_ferie",views.rifiuta_ferie,name="rifiuta_ferie"),
    path("visualizza_busta_paga",views.visualizza_busta_paga,name="visualizza_busta_paga"),
    path("crea_busta_paga",views.crea_busta_paga,name="crea_busta_paga"),
    path("crea_dipendente",views.crea_dipendente,name="crea_dipendente"),


    
    path("modifica_dipendente",views.sviluppo,name="modifica_dipendente"),

   #path("modifica_dipendente/<int:id>",views.modifica_dipendente,name="modifica_dipendente"),
    path("elimina_dipendente/<int:id>",views.elimina_dipendente,name="elimina_dipendente"),

#----azioni Bacheca---------------------------------------------------------------------    
    path("aggiungi_messaggio_bacheca",views.aggiungi_messaggio_bacheca,name="aggiungi_messaggio_bacheca"),
    path("modifica_messaggio_bacheca/<int:id>",views.modifica_messaggio_bacheca,name="modifica_messaggio_bacheca"),
    path("area_modifica_bacheca/<int:id>",views.area_modifica_bacheca,name="area_modifica_bacheca"),
    path("cancella_messaggio_bacheca/<int:id>",views.cancella_messaggio_bacheca,name="cancella_messaggio_bacheca"),
    #path("visualizza_report_mensile",views.report_mensile,name="report_mensile"),
    
    #----------------------- per resettare la password------------
    path('reset_password/', views.CustomPasswordResetView.as_view(), name='reset_password'),
    path('hrms_app/reset_password_done', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset_password_confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
]