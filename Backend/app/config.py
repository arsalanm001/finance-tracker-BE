import os
from dotenv import load_dotenv
# from pymongo import MongoClient
# from pymongo.errors import ConnectionFailure

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default-secret")
    AUTH_DB = os.getenv("AUTH_DB")
    AUTH_COLLECTION = os.getenv("AUTH_COLLECTION")


# def test_mongo_connection():
#     try:
#         client = MongoClient(Config.MONGO_URI)
#         client.server_info()
#         print("MongoDB connection successful.")
#     except ConnectionFailure as e:
#         print(f"MongoDB connection failed: {e}")