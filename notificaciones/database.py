import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URI', 'mongodb://127.0.0.1:27017/'))
db     = client[os.getenv('MONGO_DB', 'notificaciones_db')]
