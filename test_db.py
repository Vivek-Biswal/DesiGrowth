from backend.models.db import users

res = users.insert_one({"name": "vivek_final"})
print("Inserted:", res.inserted_id)