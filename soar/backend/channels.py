import datetime

from sanic import response, Blueprint

from .middleware import Middleware
from .snowflakes import channel_snowflake


class Channels:
    @staticmethod
    def setup(app):
        Channels.app = app

        bp = Blueprint("channelsapi", url_prefix="/api/channels")
        bp.middleware(Middleware.check_auth, "request")

        bp.add_route(Channels.app.ctx.limiter.limit("1 per second")(Channels.create), "/create")
        app.blueprint(bp)

    @staticmethod
    async def create(request):
        data = request.json

        if data["scope"] in ["dm", "private"]:
            if "members" not in data:
                return response.json({"error": "members not provided"})

        date = datetime.datetime.now()

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

        await Channels.app.ctx.db["channels"].insert_one({**channel})

        return response.json(channel)
