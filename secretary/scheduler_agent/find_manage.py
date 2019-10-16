import logging
import json
import random
from interfaces import get_mongo_database
from constants import (
    MONGO_HOST,
    MONGO_PORT,
    MONGO_USER,
    MONGO_PASS, 
    MONGO_DEFAULT_DB 
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Find:
    def __init__(self):
        self.data = []
        self.data_type = []
        self.collection = []
        self.returns = []
        
    def find_one_to_mongo(self):
            response = None
            try:
                db = get_mongo_database()
                collection = db[self.collection]
                doc = collection.find({self.data_type: self.data}) # self.data_type é o tipo de dado que vai ser
                for response in doc:                                   # usado para fazer a busca na DB
                    return response
            except Exception as ex: 
                logger.error(ex.__name__)
                logger.error("Falha ao inserir no mongo: {}".format(str(ex)))

    def find_all_to_mongo(self):
        vetor = []
        i=0
        try:
            db = get_mongo_database()
            collection = db[self.collection]
            doc = collection.find({},{self.data_type: self.data})
            for response in doc:
                vetor.insert(i, response[self.data_type])
                i+=1
            return vetor
        except Exception as ex: 
            logger.error(ex.__name__)
            logger.error("Falha ao inserir no mongo: {}".format(str(ex)))

    def find_to_mongo(self):
        vetor = []
        i=0
        try:
            db = get_mongo_database()
            collection = db[self.collection]
            doc = collection.find({self.data_type: self.data})
            for response in doc:
                vetor.insert(i, response[self.returns]) 
                i+=1                                  
            return vetor
        except Exception as ex: 
            logger.error(ex.__name__)
            logger.error("Falha ao inserir no mongo: {}".format(str(ex)))


class FindOne(Find):
    def __init__(self):
        super(FindOne,self).__init__()
        self.collection = []
        self.ref = []
        self.data = []

    def find(self, data_type, data, collection, returns):
        try: 
            self.collection = collection
            self.data_type = data_type
            self.data = data
            self.returns = returns
            return self.data
        except Exception as falha:
            logger.erro(falha.__name__)
            logger.erro("falha ao buscar: {}".format(str(falha)))


class Getter:
    def __init__(self):
        super(Getter, self).__init__()

    def _get_one_something(collection, data_type, data, returns):
        # retorna um dado especifico
        f = FindOne()
        f.find(data_type, data, collection, returns)
        response = f.find_one_to_mongo()
        return response

    def _get_all_something(collection, data_type, data, returns):
        # retorna um conjunto de dados dentro de uma coleção
        f = FindOne()
        f.find(data_type, data, collection, returns)
        response = f.find_all_to_mongo()
        return response

    def _get_all_data(collection, data_type, data, returns):
        # retorna todos os dados da coleção
        f = FindOne()
        f.find(data_type, data, collection, returns)
        response = f.find_to_mongo()
        return response

    def get_supplier(data_type, data): # através de um dado de supplier retorna todos os outros dados dele
        return Getter._get_one_something('supplier', data_type, data, 1)

    def get_supplier_in_backlog(data_type, data): # procura um supplier no backlog atraves do customer
        return Getter._get_all_data('backlog', data_type, data, 'supplier')

    def get_customer(data_type, data): # através de um dado de supplier retorna todos os outros dados dele
        return Getter._get_one_something('customer', data_type, data, 1)

    def get_company(data_type, data): # através de um dado de supplier retorna todos os outros dados dele
        return Getter._get_one_something('company', data_type, data, 1)

    def get_visit(data_type, data): # através de um dado de supplier retorna todos os outros dados dele
        return Getter._get_one_something('time_table', data_type, data, 1)

    def get_backlog(data_type, data): # através de um dado de supplier retorna todos os outros dados dele
        return Getter._get_one_something('backlog', data_type, data, 1)

    def get_all_supplier(data_type): # através de um tipo de dado de supplier retorna todos suppliers
        return Getter._get_all_something('supplier', data_type, 1, 1)

    def get_all_customer(data_type): # através de um tipo de dado de supplier retorna todos suppliers
        return Getter._get_all_something('customer', data_type, 1, 1)

    def get_all_company(data_type): # através de um tipo de dado de supplier retorna todos suppliers
        return Getter._get_all_something('company', data_type, 1, 1)

    def get_all_visits(data_type): # através de um tipo de dado de supplier retorna todos suppliers
        return Getter._get_all_something('time_table', data_type, 1, 1)

    def get_all_backlog(data_type): # através de um tipo de dado retorna todos esses dados do backlog
        return Getter._get_all_something('backlog', data_type, 1, 1)

    def get_all_suppliers_has_visit(data):
        return Getter._get_all_data('time_table', 'start_date', data, 'supplier')

    def get_random_visit():
        list_visits = Getter._get_all_something('time_table', '_id', 1, 1)
        x = len(list_visits)
        x = random.randint(0, (x-1))
        random_visit = Getter.get_visit('_id', list_visits[x])
        return random_visit

    def find_all_suppliers_in_this_date(collection, data):
        return Getter._get_all_data(collection, 'start_date', data, 'supplier' )
    
    def find_all_customer_have_date(collection, data):
        return Getter._get_all_data(collection, 'start_date', data, 'customer' )
    
    def find_start_date_in_backlog(data_type, data):
        return Getter._get_all_data('backlog', data_type, data, 'start_date')


if __name__ == '__main__':
    generators = [
        #Getter.get_all_suppliers_has_visit('2019-09-26T08')
        #Getter.get_all_visits('start_data'),
        #Getter.get_all_company(data)
        #Getter.get_all_customer(data)
        #Getter.get_all_supplier(data)
        #Getter.get_visit(type, data)
        #Getter.get_customer(type, data)
        #Getter.get_supplier(type, data)
        #Getter.get_random_visit()
        #Getter.find_date_supplier('backlog', 'José1')
        Getter.find_all_customer_have_date('backlog', None)
    ]
    for g in generators:
        print(g)