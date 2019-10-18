from django.urls import path

from . import views

urlpatterns = [
    # ex: /schedule/
    path('', views.index, name='index'),
    path('ImportBacklog/', views.ImportBacklog, name='ImportBacklog'),
    path('AgendamentoAutomatico/', views.AgendamentoAutomatico, name='AgendamentoAutomatico'),
    path('UploadBacklog/', views.UploadBacklog, name='UploadBacklog'),
    path('GerarTimetable/', views.GerarTimetable, name='GerarTimetable'),
    path('calendario/', views.Calendario, name='calendario'),
]