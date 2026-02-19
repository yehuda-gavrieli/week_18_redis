import os
from pymongo import MongoClient

def get_mongo_client():
    mongo_client = MongoClient(os.getenv("MONGO_URI"))
    db = mongo_client["borderDB"]
    collection = db["alerts"]   
    return collection
