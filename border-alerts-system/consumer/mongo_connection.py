import os
from pymongo import MongoClient


mongo_client = MongoClient(os.getenv("MONGO_URI"))
db = mongo_client["border_system"]
collection = db["alerts"]