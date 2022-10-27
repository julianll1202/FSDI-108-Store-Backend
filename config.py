import pymongo
import certifi

con_str = "mongodb+srv://julianll:chasenjord@cluster0.fz7wook.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_str,tlsCAFile=certifi.where())

db = client.get_database("GamifyCh31")
me = {
    "name":"Julian",
    "last_name":"Lopez",
    "age": 19,
}

def hello():
    print("Hello there")
