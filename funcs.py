import pymongo
from pymongo.errors import DuplicateKeyError
import os
# ------------Database----------
DB_URL = "mongodb+srv://admin:admin@myusers.jw5vph4.mongodb.net/?retryWrites=true&w=majority"

DB_URL=os.environ.get("DB_URL")
myclient = pymongo.MongoClient(DB_URL)
mydb = myclient["myusers"]
mycol = mydb["users"]
users_collection = myclient["myusers"]["users"]


def add_user(message):
    try:
        userDATA = {"_id": message.id, "name": message.first_name}
        mycol.insert_one(userDATA)
    except DuplicateKeyError:
        pass
    except Exception as ex:
        print(ex)
