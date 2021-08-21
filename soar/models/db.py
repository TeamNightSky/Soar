from motor import motor_asyncio
import os
from .model import User, Board, Creation


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

        self.user = User
        self.board = Board
        self.creation = Creation

    @property
    def _users(self):
        return self.client['users']

    @property
    def _creations(self):
        return self.client['creations']

    @property
    def _boards(self):
        return self.client['boards']
