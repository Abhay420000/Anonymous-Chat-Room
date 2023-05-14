from pymongo import MongoClient

client = MongoClient('mongodb+srv://abhay:bTrwP8qXKazGpBQ@cluster0.guhulof.mongodb.net/?retryWrites=true&w=majority')
db = client['ACR']

#Getting Collections
chats = db["chats"]
rooms = db["rooms"]
