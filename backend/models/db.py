from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI"))

db = client["desigrowth"]

users = db["users"]
campaigns = db["campaigns"]
ads = db["ads"]