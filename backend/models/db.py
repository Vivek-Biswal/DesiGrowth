from tinydb import TinyDB

db = None

def init_db(path):
    global db
    db = TinyDB(path)

def get_db():
    return db