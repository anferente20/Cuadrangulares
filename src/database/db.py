#Import Mongo
from pymongo import MongoClient

#Import connection to environment
from dotenv import load_dotenv
load_dotenv()
import os

def db_connection():
        client = MongoClient("mongodb+srv://"+os.getenv("DB_USER")+":"+os.getenv("DB_PASS")+"@cluster0.ndjcc.mongodb.net/?retryWrites=true&w=majority")
        db = client.Cuadrangulares
        print("Connected to database.")
        return db