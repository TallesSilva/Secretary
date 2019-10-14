from django.urls import path

from . import views

urlpatterns = [
    # ex: /schedule/
    path('', views.index, name='index'),
]