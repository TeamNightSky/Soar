import time

from .supporters import BackendClass, Error


class Chat(BackendClass):
    async def get_chat(self, slice, channel):
        if slice > 100:
            raise Error("too many messages", "Chat/get_chat")

        messages = self.db["messages"].find({
            "channel-tag": channel
        }).sort("timestamp", 1)

        messages = await messages.to_list(length=slice)

        sending = []

        for message in messages:
            sending.append({k: v for k, v in message.items() if k != "_id"})

        return sending

    async def add_message(self, channel_tag, user, content):
        json = {
            "channel-tag": channel_tag,
            "sender": user,
            "timestamp": time.time(),
            "content": content
        }
        await self.db["messages"].insert_one({**json})
        return json

    async def chat_send_msg(self, user, channel, content):
        channel = await self.db["channels"].find_one({
            "message-tag": channel
        })

        if channel["scope"] == "personal" and channel["creator"] != user:
            raise Error("permission denied", "Chat/chat_send_msg")

        msg = await self.add_message(channel, user, content)

        return msg
