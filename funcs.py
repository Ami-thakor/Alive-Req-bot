import os
import motor.motor_asyncio

DB_URL = os.environ.get(
    "DB_URL", "mongodb+srv://admin:rahul@myusers.qsyvptv.mongodb.net/?retryWrites=true&w=majority")
myclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
mydb = myclient["KingReqBot"]
mycol = mydb["users"]
users_collection = mydb["users"]


async def add_user(message):
    try:
        userDATA = {"_id": message.id, "name": message.first_name}
        await mycol.insert_one(userDATA)
    except:
        pass


async def getid():
    values = []
    async for key in mycol.find():
        id_ = key["_id"]
        values.append((id_))
    return values
