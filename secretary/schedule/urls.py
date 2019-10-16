from django.urls import path

from . import views

urlpatterns = [
    # ex: /schedule/
    path('', views.index, name='index'),
    path('impt_backlog/', views.impt_backlog, name='impt_backlog'),
    path('AgendamentoAutomatico/', views.AgendamentoAutomatico, name='AgendamentoAutomatico')
       
]