from sanic import response, Blueprint
import asyncio
import hashlib
import time
from .middleware import Middleware


class Auth:
    def __init__(self, app):
        self.app = app
        self.middleware = Middleware(app)
        self.setup()

    def setup(self):
        bp = Blueprint("authapi", url_prefix="/api/auth")

        bp.middleware(self.middleware.check_auth, 'request')

        bp.add_route(register, '/register')
        bp.add_route(login, '/login')

        self.app.blueprint(bp)

    async def register(self, request):
        data = request.json

        count = await users.count_documents({"username": data["un"]})

        if count > 0:
            return response.json({"error": "Username taken"})

        await users.insert_one({
            "username": data["un"],
            "password": hashlib.sha256(data["pw"].encode("utf-8")).hexdigest(),
            "created-at": time.time(),
            "friends": [],
            "friend-reqs": []  # Inbound
        })

        request.ctx.auth = data["un"]

        return response.json({"un": data["un"]})

    async def login(self, request):
        data = request.json
        users = self.app.ctx["users"]

        await asyncio.sleep(0.1)

        if hashlib.sha256(data["pw"].encode("utf-8")).hexdigest() != (await users.find_one({"username": data["un"]}))["password"]:
            return response.json({"error": "incorrect password"})

        request.ctx.auth = data["un"]

        return response.json({"un": data["un"]})
