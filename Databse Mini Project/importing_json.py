import json
import pymongo
from pprint import pprint 


connection = pymongo.MongoClient('mongodb://localhost:27017/')
db = connection.book
record1 = db.book_collection
page = open("airports.json", 'r')
parsed = json.load(page)

record1.insert_many(parsed)