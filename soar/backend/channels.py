import datetime

from ..snowflakes import channel_snowflake
from .supporters import BackendClass, Error


class Channels(BackendClass):
    async def create(self, name, scope, public, creator, members=None):
        if scope in ["dm", "private"]:
            if "members" is None:
                raise Error("members not provided", "Channels/create")

        date = datetime.datetime.now()

        channel = {
            "name": name,
            "scope": scope,
            "public": public,
            "members": [] if members is None else members,
            "creator": creator,
            "attrs": {},
            "created-at": date,
            "message-tag": channel_snowflake(name, creator, date),
            "parent": None,
            "roles": {}
        }

        await self.db["channels"].insert_one({**channel})

        return channel
