from .model import Model


class Board(Model):
    DEFAULT_DATA = {

    }

    async def add_message(self, channel_tag, user, content, time):
        json = {
            "channel-tag": channel_tag,
            "sender": user,
            "timestamp": time,
            "content": content
        }
        await self.collection["messages"].insert_one({**json})
        return json
