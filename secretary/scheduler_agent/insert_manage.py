import logging
import json
from interfaces import get_mongo_database
from constants import (
    MONGO_HOST,
    MONGO_PORT,
    MONGO_USER,
    MONGO_PASS, 
    MONGO_DEFAULT_DB 
)
from fake_profile import *

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Insert:
    def __init__(self):
        self.data = []

    def insert_to_mongo(self):
        response = None
        try:
            db = get_mongo_database()
            collection = db[self.collection]
            response = collection.insert_one(self.data)
        except Exception as ex:
            logger.error(ex.__name__)
            logger.error("Falha ao inserir no mongo: {}".format(str(ex)))
        return response


class Insert_Supplier_Payload(Insert):
    def __init__(self):
        super(Insert_Supplier_Payload, self).__init__()
        self.collection = 'supplier'

    def generate(self):
        try:
            self.data = CreateFake.get_fake_supplier()
            return self.data
        except Exception as falha:
            logger.error(falha.__name__)
            logger.error("Falha ao atualizar supplier fake: {}".format(str(falha)))

class Insert_Customer_Payload(Insert):
    def __init__(self):
        super(Insert_Customer_Payload, self).__init__()
        self.collection = 'customer'
    
    def generate(self):
        try:
            self.data = CreateFake.get_fake_customer()
            return self.data
        except Exception as falha:
            logger.error(falha.__name__)
            logger.error("Falha ao atualizar customer fake: {}".format(str(falha)))

class Insert_Timetable_Payload(Insert):
    def __init__(self):
        super(Insert_Timetable_Payload,self).__init__()
        self.collection = 'time_table'

    def generate(self, data):
        try: 
            self.data = data
            return self.data
        except Exception as falha:
            logger.erro(falha.__name__)
            logger.erro("falha ao criar timetable sem a data: {}".format(str(falha)))            

class Insert_Backlog_Payload(Insert):
    def __init__(self):
        super(Insert_Backlog_Payload,self).__init__()
        self.collection = 'backlog'

    def generate(self, data):
        try: 
            self.data = data
            return self.data
        except Exception as falha:
            logger.erro(falha.__name__)
            logger.erro("falha ao criar timetable sem a data: {}".format(str(falha)))            


if __name__ == '__main__':
    generators = [
        #Insert_Supplier_Payload(),
        #Insert_Customer_Payload(),
        #GeneratorTimetableNone(),
        #Insert_Timetable_Payload(),
        #Insert_Backlog(),
    ]
    while(1):        
        for g in generators:
            g.generate()
            g.insert_to_mongo()
            