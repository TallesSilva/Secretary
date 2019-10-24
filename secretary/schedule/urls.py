from django.urls import path

from . import views

urlpatterns = [
    # ex: /schedule/
    path('', views.index, name='index'),
    path('ImportBacklog/', views.ImportBacklog, name='ImportBacklog'),
    path('UploadBacklog/', views.UploadBacklog, name='UploadBacklog'),
    path('Calendario/', views.Calendario, name='Calendario'),
    path('AgendamentoAutomatico/', views.AgendamentoAutomatico, name='AgendamentoAutomatico'),
    path('ContactarCliente/', views.ContactarCliente, name='ContactarCliente'),
    
    
]