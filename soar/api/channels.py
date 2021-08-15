from sanic import response, Blueprint
import asyncio
import datetime
import hashlib
from . import middleware
from . import snowflakes


server = None


def setup(app):
    global server
    server = app

    bp = Blueprint("channelsapi", url_prefix="/api/channels")
    bp.middleware(middleware.channels, "request")

    bp.add_route(create, "/create")

    app.blueprint(bp)


async def create(request):
    data = request.json

    attrs = {}

    if data["scope"] in ["dm", "private"]:
        if "members" not in data:
            return json({"error": "members not provided"})

    date = datetime.datetime()

    channel = {
        "name": data["name"],
        "scope": data["scope"],
        "public": data["public"],
        "members": [] if data.get("members") is None else data["members"],
        "creator": request.ctx.auth,
        "attrs": attrs,
        "created-at": date,
        "message-tag": snowflakes.channel(data["name"], request.ctx.auth, date),
        "parent": None,
        "roles": {}
    }

    await server.ctx.channels.insert_one({**channel})

    return response.json(channel)
