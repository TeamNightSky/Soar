import time

from sanic import response, Blueprint

from .middleware import Middleware


class Chat:
    @staticmethod
    def setup(app):
        Chat.app = app

        bp = Blueprint("chatapi", url_prefix="/api/chat")

        bp.middleware(Middleware.get_chat, 'request')

        bp.add_route(Chat.get_chat, "/hist")
        bp.add_route(Chat.chat_send_msg, "/send")
        Chat.app.blueprint(bp)

    @staticmethod
    async def get_chat(request):
        data = request.json

        if "slice" not in data:
            return response.json({"error": "message slice not found"})
        if data["slice"] > 100:
            return response.json({"error": "too many messages"})

        messages = Chat.app.db["messages"].find({
            "channel-tag": data["channel"]
        }).sort("timestamp", 1)

        messages = await messages.to_list(length=data["slice"])

        sending = []

        for message in messages:
            sending.append({k: v for k, v in message.items() if k != "_id"})

        return response.json({
            "messages": sending
        })

    @staticmethod
    async def add_message(channel_tag, user, content):
        json = {
            "channel-tag": channel_tag,
            "sender": user,
            "timestamp": time.time(),
            "content": content
        }
        await Chat.app.ctx.db["messages"].insert_one({**json})
        return json

    @staticmethod
    async def chat_send_msg(request):
        user = request.ctx.auth
        data = request.json

        channel = await Chat.app.ctx.db["channels"].find_one({
            "message-tag": data["channel"]
        })

        if channel["scope"] == "personal" and channel["creator"] != user:
            return response.json({"error": "permission denied"})

        msg = await Chat.add_message(data["channel"], user, str(data.get("content")))

        return response.json(msg)
