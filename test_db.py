from backend.models.db import users

res = users.insert_one({"name": "final_test"})
print("Inserted:", res.inserted_id)