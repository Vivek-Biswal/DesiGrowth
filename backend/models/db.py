from pymongo import MongoClient, ASCENDING
import os

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise Exception("❌ MONGO_URI not found")

client = MongoClient(MONGO_URI)

db = client["desigrowth"]

# Collections
users = db["users"]
campaigns = db["campaigns"]
ads = db["ads"]
analytics = db["analytics"]

# ✅ INDEXES (IMPORTANT)

# Unique email
users.create_index([("email", ASCENDING)], unique=True)

# Fast queries
campaigns.create_index("user_id")
ads.create_index("campaign_id")
analytics.create_index("ad_id")