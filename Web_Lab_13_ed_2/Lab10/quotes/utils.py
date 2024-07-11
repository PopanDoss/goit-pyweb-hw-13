from pymongo import MongoClient

def get_mongodb():
    
    client = MongoClient("mongodb://root:765890@localhost:27017")

    db = client.Lab10

    return db