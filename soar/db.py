from motor import motor_asyncio
import os


def init():
    global client, db, users, channels, messages
    client = motor_asyncio.AsyncIOMotorClient(
        f"mongodb+srv://SoarReplit:{os.getenv('MONGO_PW')}@cluster0.n3qeh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    )

    db = client["soardb"]

    users = db["users"]
    channels = db["channels"]
    messages = db["messages"]

