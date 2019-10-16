from pymongo import MongoClient
from constants import (
    MONGO_HOST,
    MONGO_PORT,
    MONGO_USER,
    MONGO_PASS, 
    MONGO_DEFAULT_DB #aia
)

def get_mongo_database():
    client = MongoClient(host=MONGO_HOST,
                         port=MONGO_PORT,
                         username=MONGO_USER,
                         password=MONGO_PASS)
    return client[MONGO_DEFAULT_DB]

def star_query_collection(collection_name):
    database = get_mongo_database()
    collection = database[collection_name]
    return list(collection.find({}))
   
