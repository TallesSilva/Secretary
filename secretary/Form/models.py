from django.db import models


class Bot(models.Model):
    nome = models.TextField(blank=True)
    data = models.DateTimeField('date published')
    assunto = models.TextField(blank=True)
    pergunta = models.TextField(blank=True)
    resposta = models.TextField(blank=True)

