from ..snowflakes import user_snowflake
from .model import Model


class User(Model):
    DEFAULT_DATA = {
        "username": "",
        "creations": [],
        "friends": [],
        "friend-reqs": [],
        "logins": [],
        "online": False
    }

    def __init__(self, client, username, time):
        snowflake = user_snowflake(username, time)
        self.username = username
        self.time = time
        super().__init__(client, 'users', snowflake)

    async def signup(self, password_hash):
        if not await self.exists():
            self.data.update({
                "username": self.username,
                "password": password_hash,
                "created-at": self.time
            })
            await self.save()
        else:
            await self.reload()

    async def login(self, password_hash):
        pass
