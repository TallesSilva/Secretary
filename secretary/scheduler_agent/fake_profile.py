from datetime import (datetime, timedelta)
from faker import Faker
from interfaces import *

fake = Faker('pt_BR')


class CreateFake():
    def __init__(self):
        super(CreateFake, self).__init__()

    def get_fake_supplier():
        payload_supplier = {
            "nome": fake.name(),
            u"cpf": fake.cpf(),
            "disponibilidade": "Integral",
            "cargo": "estagiario",
            "empresa": None,
            "endereco": {
                "rua": fake.street_name(),
                "numero": fake.building_number(),
                "complemento": None,
                "bairro": fake.bairro(),
                "cep": fake.postcode(),
                "cidade": fake.city(),
                "estado": fake.estado_sigla(),
                "latitude": None,
                "longitude": None
            },
            "contato": {
                "fixo": fake.cellphone_number(),
                "celular": fake.cellphone_number(),
                "email": "tallesr@kyros.com.br",
                "site": "http://192.168.1.3:8080/suppliers/",
                "whatsapp": fake.cellphone_number(),
                "telegram": fake.cellphone_number()
            }
        }
        return payload_supplier

    def get_fake_customer():
        payload_customer = {
            "nome": fake.name(),
            u"cpf": fake.cpf(),
            "dia_preferencia": None,
            "hora_preferencia": None,
            "empresa": None,
            "endereco": {
                "rua": fake.street_name(),
                "numero": fake.building_number(),
                "complemento": None,
                "bairro": fake.bairro(),
                "cep": fake.postcode(),
                "cidade": fake.city(),
                "estado": fake.estado_sigla(),
                "latitude": None,
                "longitude": None
            },
            "contato": {
                "fixo": fake.cellphone_number(),
                "celular": fake.cellphone_number(),
                "email": "tallesr@kyros.com.br",
                "site": None,
                "whatsapp": fake.cellphone_number(),
                "telegram": fake.cellphone_number()
            }
        }
        return payload_customer

    def get_fake_visit_none():
        payload_timetable = {
            "data": None,
            "status": None,
            "observacao": "",
            "task": None,
            "supplier": None,
            "customer": None,
            "company": None
        }
        return payload_timetable

    def get_fake_visit_date(status, observacao, task, supplier, customer, company):
        payload_timetable = {
            "data": get_fake_date(),
            "status": status,
            "observacao": observacao,
            "task": task,
            "supplier": supplier,
            "customer": customer,
            "company": company
        }
        return payload_timetable


if __name__ == '__main__':
    fakes = [
        #get_fake_customer(),
        #get_fake_supplier(),
        #get_fake_visit_date(),
        #get_fake_date()
    ]
    for f in fakes:
        print(f)