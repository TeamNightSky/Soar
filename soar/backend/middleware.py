import hashlib
from sanic import response


safe_chars = \
    "abcdefghijklmnopqrstuvwxyzABDCEFGHIJKLMNOPQRSTUVWXYZ123456789-_+.,:"


def process_request(request):
    if request.json is None:
        return response.json({"error": "json not provided"})
    return request.json


class Middleware:
    @staticmethod
    def setup(app):
        Middleware.app = app

    @staticmethod
    async def check_auth(request):
        """Channels, Auth"""
        data = process_request(request)
        if not isinstance(data, dict):
            return data

        if "pw" not in data:
            return response.json({"error": "Password not included"})
        elif "un" not in data:
            return response.json({"error": "Username not included"})
        elif not min([c in safe_chars for c in data["un"]]):
            return response.json({"error": "Invalid username"})
        elif not min([c in safe_chars for c in data["pw"]]):
            return response.json({"error": "Invalid password"})

        given = hashlib.sha256(data["pw"].encode("utf-8")).hexdigest()
        correct = (await Middleware.app.ctx.db["users"].find_one({"username": data["un"]}))["password"]

        if given != correct:
            return response.json({"error": "incorrect password"})
        request.ctx.auth = data["un"]

    @staticmethod
    async def get_chat(request):
        """Chat.get_chat"""
        data = process_request(request)
        if not isinstance(data, dict):
            return data

        if not hasattr(request.ctx, "auth"):
            if err := Middleware.check_auth(request):
                return err
        user = request.ctx.auth

        if "channel" not in data:
            return response.json({"error": "channel not included"})
        elif not min([c in safe_chars for c in data["channel"]]):
            return response.json({"error": "Invalid channel name"})
        elif (await Middleware.app.ctx.db["channels"].count_documents({
            "message-tag": data["channel"]
        })) < 1:
            return response.json({"error": "channel not found"})

        channel = await Middleware.app.ctx.db["channels"].find_one({
            "message-tag": data["channel"]
        })

        if channel["scope"] in ["personal", "public"]:
            return

        if user not in channel["members"]:
            return response.json({"error": "channel not found"})
