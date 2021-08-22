import hashlib

from ..snowflakes import user_snowflake
from .model import Model


class User(Model):
    DEFAULT_DATA = {

    }

    def __init__(self, client, username, password, time):
        snowflake = user_snowflake(username, time)
        self.username, self.password, self.time = username, password, time
        super().__init__(client, 'users', snowflake)

    async def setup(self):
        if not await self.exists():
            self.data.update({
                "username": self.username,
                "password": hashlib.sha256(self.password.encode("utf-8")).hexdigest(),
                "created-at": self.time,
                "friends": [],
                "friend-reqs": [],  # Inbound
                "logins": []
            })
            await self.save()
        else:
            await self.reload()
