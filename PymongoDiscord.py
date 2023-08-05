import json
from pymongo.mongo_client import MongoClient

resource = open("./HiddenBot-py/resources.json")
data = json.load(resource)
DB_URL = data["mongoDB_URL"]

#Database
DB_Client = MongoClient(DB_URL)
try:
    DB_Client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
def getClient():
    return DB_Client