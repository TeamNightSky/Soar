from sanic import response, Blueprint
import asyncio
import time
import hashlib
from . import middleware


server = None

def setup(app):
    global server
    server = app

    bp = Blueprint("chatapi", url_prefix="/api/chat")

    bp.middleware(middleware.chat, 'request')

    bp.add_route(getchat, "/hist")
    bp.add_route(chat_send_msg, "/send")

    app.blueprint(bp)


async def getchat(request):
    user = request.ctx.auth
    data = request.json

    if "slice" not in data:
        return response.json({"error": "message slice not found"})
    if data["slice"] > 100:
        return response.json({"error": "too many messages"})

    messages = server.ctx.messages.find({
            "channel-tag": data["channel"]
    }).sort("timestamp", 1)

    messages = await messages.to_list(length=data["slice"])

    sending = []

    for message in messages:
        sending.append({k:v for k, v in message.items() if k != "_id"})

    return response.json({
        "messages": sending
    })


async def add_message(channel_tag, user, content):
    json = {
        "channel-tag": channel_tag,
        "sender": user,
        "timestamp": time.time(),
        "content": content
    }
    await server.ctx.messages.insert_one({**json})
    return json


async def chat_send_msg(request):
    user = request.ctx.auth
    data = request.json

    channel = await server.ctx.channels.find_one({
        "message-tag": data["channel"]
    })

    if channel["scope"] == "personal" and channel["creator"] != user:
        return response.json({"error": "permission denied"})

    msg = await add_message(data["channel"], user, str(data.get("content")))

    return response.json(msg)

