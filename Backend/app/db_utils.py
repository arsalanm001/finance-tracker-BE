from pymongo import MongoClient
from .config import Config

client = MongoClient(Config.MONGO_URI)

def get_db_collection(db_name: str, collection_name: str):
    db = client[db_name]
    return  db[collection_name]