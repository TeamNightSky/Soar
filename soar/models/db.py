from motor import motor_asyncio
import os


class SoarDB:
    def __init__(self, db_user=None, db_passw=None):
        if db_user is None:
            db_user = 'SoarReplit'
        if db_passw is None:
            db_passw = os.getenv('MONGO_PW')

        self.client = motor_asyncio.AsyncIOMotorClient(
            f"mongodb+srv://{db_user}:{db_passw}@cluster0.n3qeh.mongodb.net/myFirstDatabase"
            "?retryWrites=true&w=majority"
        )

    @property
    def users(self):
        return self.client['users']

    @property
    def creations(self):
        return self.client['creations']

    @property
    def boards(self):
        return self.client['boards']
