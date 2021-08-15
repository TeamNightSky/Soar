from sanic import response, Blueprint
import asyncio
import datetime
import hashlib

from .middleware import Middleware
from .snowflakes import channel_snowflake


class Channels:
    def __init__(self, app):
        self.app = app

        bp = Blueprint("channelsapi", url_prefix="/api/channels")
        bp.middleware(middleware.check_auth, "request")

        bp.add_route(create, "/create")
        app.blueprint(bp)

    async def create(self, request):
        data = request.json

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
            "attrs": {},
            "created-at": date,
            "message-tag": channel_snowflake(data["name"], request.ctx.auth, date),
            "parent": None,
            "roles": {}
        }

        await self.app.ctx.db["channels"].insert_one({**channel})

        return response.json(channel)
