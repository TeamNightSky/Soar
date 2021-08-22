from .model import Model
from ..snowflakes import board_snowflake


class Board(Model):
    DEFAULT_DATA = {
        "title": "",
        "author": None,
        "attachments": [],
        "created-at": None
    }

    def __init__(self, client, title, owner, time):
        snowflake = board_snowflake(title, owner, time)
        super().__init__(client, "boards", snowflake)

    async def add_message(self, channel_tag, user, content, time):
        json = {
            "channel-tag": channel_tag,
            "sender": user,
            "timestamp": time,
            "content": content
        }
        await self.collection["messages"].insert_one({**json})
        return json
