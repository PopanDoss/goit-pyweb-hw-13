import json 
from bson.objectid import ObjectId

from pymongo import MongoClient

client = MongoClient("mongodb://root:765890@localhost:27017")

db = client.Lab10

with open('qoutes.json', 'r', encoding='utf-8' ) as fd:

    quotes = json.load(fd) 

for quotes in quotes:
    author = db.authors.find_one({'fullname': quotes['author']})
    if author:
        db.quotes.insert_one({
            'quote' : quotes['quote'],
            'tags' : quotes['tags'],
            'author' : ObjectId(author['_id'])
            })