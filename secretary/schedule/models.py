from django.db import models


class Task(models.Model):
    descricao = models.CharField(max_length=200)
