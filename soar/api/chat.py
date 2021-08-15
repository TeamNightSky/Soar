import time

from sanic import response, Blueprint

from .middleware import Middleware


class Chat:
    def __init__(self, app):
        self.app = app
        self.middleware = Middleware(self.app)
        self.setup()

    def setup(self):
        bp = Blueprint("chatapi", url_prefix="/api/chat")

        bp.middleware(self.middleware.get_chat, 'request')

        bp.add_route(self.get_chat, "/hist")
        bp.add_route(self.chat_send_msg, "/send")
        self.app.blueprint(bp)

    async def get_chat(self, request):
        data = request.json

        if "slice" not in data:
            return response.json({"error": "message slice not found"})
        if data["slice"] > 100:
            return response.json({"error": "too many messages"})

        messages = self.app.db["messages"].find({
            "channel-tag": data["channel"]
        }).sort("timestamp", 1)

        messages = await messages.to_list(length=data["slice"])

        sending = []

        for message in messages:
            sending.append({k: v for k, v in message.items() if k != "_id"})

        return response.json({
            "messages": sending
        })

    async def add_message(self, channel_tag, user, content):
        json = {
            "channel-tag": channel_tag,
            "sender": user,
            "timestamp": time.time(),
            "content": content
        }
        await self.app.ctx.db["messages"].insert_one({**json})
        return json

    async def chat_send_msg(self, request):
        user = request.ctx.auth
        data = request.json

        channel = await self.app.ctx.db["channels"].find_one({
            "message-tag": data["channel"]
        })

        if channel["scope"] == "personal" and channel["creator"] != user:
            return response.json({"error": "permission denied"})

        msg = await self.add_message(data["channel"], user, str(data.get("content")))

        return response.json(msg)
