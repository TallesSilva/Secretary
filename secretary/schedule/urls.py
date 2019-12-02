from django.urls import path

from . import views

urlpatterns = [
    # ex: /schedule/
    path('', views.index, name='index'),
    path('ImportBacklog/', views.ImportBacklog, name='ImportBacklog'),
    path('UploadBacklog/', views.UploadBacklog, name='UploadBacklog'),
    path('Calendario/', views.Calendario, name='Calendario'),
    path('AgendamentoAutomatico/', views.AgendamentoAutomatico, name='AgendamentoAutomatico'),    
    path('Clientes/', views.Clientes, name='Clientes'),
    path('Formulario/'), views.Form, name='Formulario'
]