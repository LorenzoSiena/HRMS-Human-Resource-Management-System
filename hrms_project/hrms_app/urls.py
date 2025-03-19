from django.urls import path
from . import views

urlpatterns = [
    path("", views.hrms_app,name="home"),
    path("register", views.register, name="register"),
    path("login", views.user_login, name="login"),
    path("logout", views.user_logout, name="logout"),
    path("presenza",views.presenze,name="presenze"),
    path("dipendenti",views.dipendenti,name="dipendenti"),
    path("stipendi",views.stipendi,name="stipendi"),

    # per resettare la password
    path('reset_password/', views.CustomPasswordResetView.as_view(), name='reset_password'),
    path('hrms_app/reset_password_done', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset_password_confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
]