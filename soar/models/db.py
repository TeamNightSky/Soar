from motor import motor_asyncio
import os


class SoarDB:
    def __init__(self):
        self.client = motor_asyncio.AsyncIOMotorClient(
            f"mongodb+srv://SoarReplit:{os.getenv('MONGO_PW')}@cluster0.n3qeh.mongodb.net/myFirstDatabase?retryWrites"
            f"=true&w=majority "
        )

    @property
    def db(self):
        return self.client["db"]
