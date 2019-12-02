from django.db import models
from django.utils import timezone
from datetime import datetime
from mongoengine import Document, fields, EmbeddedDocument

ESTADOS = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG',
           'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']

STATUS = ['Backlog', 'Finalizado', 'Revogado', 'Aberto', 'Interrompido', 'Reagendado', 'Inconclusivo']

DIAS = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']

class Endereco(EmbeddedDocument):
    meta = {'strict': False}

    rua = fields.StringField(required=True)
    numero = fields.StringField(required=True)
    complemento = fields.StringField(required=True)
    bairro = fields.StringField(required=True)
    cep = fields.StringField(required=True)
    cidade = fields.StringField(required=True)
    estado = fields.StringField(required=True)
    latitude = fields.StringField(required=True)
    longitude = fields.StringField(required=True)
    

class Contato(EmbeddedDocument):
    meta = {'strict': False}

    fixo = fields.StringField(required=True)
    celular = fields.StringField(required=True)
    email = fields.EmailField(required=True)
    site = fields.StringField(required=True)
    whatsapp = fields.StringField(required=True)
    telegram = fields.StringField(required=True)

# ------------------------------------------------------------

class Template(Document):
    meta = {'strict': False}

    name = fields.StringField(required=True, unique=True)
    file = fields.StringField(required=True, null=True)
    fields = fields.ListField()

class Documento(Document):
    meta = {'strict': False}

    template = fields.ReferenceField('Template', required=False)
    active = fields.BooleanField(default=True)
    name = fields.StringField(required=True, unique=True)
    format = fields.StringField(required=False, null=True)
    created = fields.DateTimeField(default=timezone.now)
    fields = fields.DynamicField(required=False)

class Company(Document):
    meta = {'strict': False}

    nome = fields.StringField(required=True)
    nome_responsavel = fields.StringField(required=False)
    razao_social = fields.StringField(required=True)
    cnpj = fields.StringField(required=True, unique=True)
    endereco = fields.EmbeddedDocumentField(Endereco, required=True)
    contato = fields.EmbeddedDocumentField(Contato, required=True)

class Supplier(Document):
    meta = {'strict': False}

    nome = fields.StringField(required=True)
    cpf = fields.StringField(required=True, unique=True)
    disponibilidade = fields.StringField(required=True)
    endereco = fields.EmbeddedDocumentField(Endereco, required=True)
    empresa = fields.ReferenceField('Company', required=True)
    cargo = fields.StringField(required=False)
    contato = fields.EmbeddedDocumentField(Contato, required=True)

class Customer(Document):
    meta = {'strict': False}

    nome = fields.StringField(required=True)
    cpf = fields.StringField(required=True, unique=True)
    endereco = fields.EmbeddedDocumentField(Endereco, required=True)
    contato = fields.EmbeddedDocumentField(Contato, required=True)
    empresa = fields.ReferenceField('Company', required=True)
    dia_preferencia = fields.StringField(required=True)
    hora_preferencia = fields.StringField(required=True)

class Task(Document):
    meta = {'strict': False}

    descricao = fields.StringField(required=True)
    company = fields.ReferenceField('Company', required=True)

class TimeTable(Document):
    meta = {'strict': False}

    start_date = fields.StringField(required=True)
    end_date = fields.StringField(required=True)
    status = fields.StringField(required=True)
    task = fields.StringField(required=True)
    supplier = fields.ReferenceField('Supplier', required=True)
    customer = fields.ReferenceField('Customer', required=True)
    company = fields.ReferenceField('Company', required=True)
    observacao = fields.StringField(required=True)

class Backlog(Document):
    meta = {'strict': False}

    start_date = fields.StringField(required=False)
    status = fields.StringField(required=True)
    task = fields.StringField(required=True)
    supplier = fields.ReferenceField('Supplier', required=True)
    customer = fields.ReferenceField('Customer', required=True)
    company = fields.ReferenceField('Company', required=True)
    observacao = fields.StringField(required=False)
    deadline_start_date = fields.StringField(required=False)
    deadline_end_date = fields.StringField(required=False)


class Form(Document):
    meta = {'strict': False}

    Assunto = fields.StringField(required=True)
    Pergunta = fields.StringField(required=True)
    Resposta = fields.StringField(required=True)
