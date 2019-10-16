from datetime import (datetime, timedelta)
from constants import (MONGO_DEFAULT_DB, MONGO_HOST, MONGO_PASS, MONGO_PORT, MONGO_USER)
from faker import Faker
from find_manage import *
from interfaces import *
from insert_manage import *
from fake_profile import *
import random

fake = Faker('pt_BR')


class Manage:
    def __init__(self):
        super(Manage, self).__init__()

    def generate_timetable(start_create: datetime, finished_create: datetime):
        """Inicializa variaveis necessarias e lista todos os customers sem visita e cria visitas."""
        start_date = start_create
        start_date = Manage.available_date(start_date)

        customer_available = Manage.find_available_customer()
        for customer in customer_available:
            """start_date = finished_create o sistema para de gerar visitas."""
            suppliers = None
            suppliers = Manage.find_available_suppliers(start_date)
            while suppliers is None:
                """Percorre as datas a procura de supplier != None."""
                start_date = Manage.date_sum_hour(start_date, 1)
                start_date = Manage.available_date(start_date)
                suppliers = Manage.find_available_suppliers(start_date)
            """atualiza as condições para gerar as visitas ou não"""
            condition_finish_create_visits = start_date >= finished_create
            conditon_continue_create_visits = start_date < finished_create
            if condition_finish_create_visits:
                break
            else:
                end_date = Manage.date_sum_hour(start_date, 1)
                x = len(suppliers)
                x = random.randint(0, (x-1))
                payload = Manage.generate_available_payload_visit(customer, supplier, 'Confirmada', 'Instalação de Modem', start_date, end_date)
                Manage.insert_payload(payload)
        return True

    def insert_payload(data):
        """Insere o payload de visita no db."""
        try:
            f = Insert_Timetable_Payload()
            f.generate(data)
            f.insert_to_mongo()
            return True
        except:
            return False

    def find_available_customer():
        """Retorna customers que não possuem visitas."""
        list_customers = Manage.get_registered_customers()
        list_customers_has_visit = Getter.get_all_visits('customer')
        return [x for x in list_customers if x not in list_customers_has_visit]
        
    def find_available_suppliers(start_date):
        """Retorna supplier que não tem visita marcada nesse horario."""
        date = start_date.strftime("%Y-%m-%dT%H")
        list_supplier = Manage.get_registered_suppliers()
        list_supplier_has_visit = Getter.get_all_suppliers_has_visit(date)
        suppliers = [x for x in list_supplier if x not in list_supplier_has_visit]
        if not suppliers:
            return None
        return suppliers

    def generate_available_payload_visit(customer, supplier, status, task, start_date, end_date):
        """Retorna um payload da visita."""
        try:
            payload_timetable = {
            "start_date": start_date.strftime("%Y-%m-%dT%H"),
            "end_date": end_date.strftime("%Y-%m-%dT%H"),
            "status": status,
            "observacao": task,
            "task": task,
            "supplier": supplier,
            "customer": customer,
            "company": "5d6020abd12e66a47a7888ed"
            }
            print(payload_timetable)
            return payload_timetable
        except:
            print("exception has found")

    def generate_none_payload_visit(customer, supplier, task):
        """Retorna um payload da visita."""
        try:
            payload_timetable = {
            "start_date": None,
            "end_date": None,
            "status": 'Backlog',
            "observacao": '',
            "task": task,
            "supplier": supplier,
            "customer": customer,
            "company": "5d6020abd12e66a47a7888ed"
            }
            print(payload_timetable)
            return payload_timetable
        except:
            print("exception has found")

    def date_sum_hour(start_date, value):
        """Retorna a data de entrada acrescida de value horas."""  
        return (start_date + timedelta(hours=value))

    def available_date(date):
        """Avalia horario entre 8 e 18 horas."""
        if date.hour < 8 or date.hour > 17:
            date = Manage.date_sum_hour(date, 1)
            date = Manage.available_date(date)
        return date

    def customer_has_visit(customer_id: str):
        """Retorna todos os ids de customers que possuem visitas."""
        valida = []
        valida = Getter.get_visit('customer', customer_id)
        if valida is None:
            return False
        else:
            return True

    def get_registered_customers():
        """Retorna todos os customers."""
        return Getter.get_all_customer('_id')

    def get_registered_suppliers():
        """Retorna todos os suppliers."""
        return Getter.get_all_supplier('_id')

if __name__ == '__main__':
    """ 
        Testa a função em uma data aleatoria
    gera uma data de inicio de criação de visitas
    e uma data de finalização da criação das visitas.
    """
    start_create = fake.future_datetime("+10h")
    finished_create = Manage.date_sum_hour(start_create, 19)
    print("A visitas serão geradas de {} até {}".format(start_create.strftime("%Y-%m-%dT%H"), finished_create.strftime("%Y-%m-%dT%H")))
    Manage.generate_timetable(start_create, finished_create)
