safechars = \
"abcdefghijklmnopqrstuvwxyzABDCEFGHIJKLMNOPQRSTUVWXYZ123456789-_+.,"

chatsafechars = \
"abcdefghijklmnopqrstuvwxyzABDCEFGHIJKLMNOPQRSTUVWXYZ123456789-_+.,:"


async def auth(request):
    if request.json is None:
        return response.json({"error": "json not provided"})

    data = request.json

    if "pw" not in data:
        return response.json({"error": "Password not included"})
    elif "un" not in data:
        return response.json({"error": "Username not included"})
    elif not min([c in safechars for c in data["un"]]):
        return response.json({"error": "Invalid username"})
    elif not min([c in safechars for c in data["pw"]]):
        return response.json({"error": "Invalid password"})


async def channels(request):
        if request.json is None:
            return response.json({"error": "json not provided"})

        data = request.json

        if not hasattr(request.ctx, "auth"):
            if "pw" not in data:
                return response.json({"error": "Password not included"})
            elif "un" not in data:
                return response.json({"error": "Username not included"})
            elif not min([c in safechars for c in data["un"]]):
                return response.json({"error": "Invalid username"})
            elif not min([c in safechars for c in data["pw"]]):
                return response.json({"error": "Invalid password"})

            given = hashlib.sha256(data["pw"].encode("utf-8")).hexdigest()
            correct = (await server.ctx.users.find_one({"username": data["un"]}))["password"]

            if given != correct:
                return response.json({"error": "incorrect password"})

            request.ctx.auth = data["un"]


async def chat(request):
    if request.json is None:
        return response.json({"error": "json not provided"})

    data = request.json

    if not hasattr(request.ctx, "auth"):
        if "pw" not in data:
            return response.json({"error": "Password not included"})
        elif "un" not in data:
            return response.json({"error": "Username not included"})
        elif not min([c in safechars for c in data["un"]]):
            return response.json({"error": "Invalid username"})
        elif not min([c in safechars for c in data["pw"]]):
            return response.json({"error": "Invalid password"})

        given = hashlib.sha256(data["pw"].encode("utf-8")).hexdigest()
        correct = (await server.ctx.users.find_one({"username": data["un"]}))["password"]

        if given != correct:
            return response.json({"error": "incorrect password"})

        request.ctx.auth = data["un"]

    user = request.ctx.auth

    if "channel" not in data:
        return response.json({"error": "channel not included"})
    elif not min([c in chatsafechars for c in data["channel"]]):
        return response.json({"error": "Invalid channel name"})
    elif (await server.ctx.channels.count_documents({
        "message-tag": data["channel"]
    })) < 1:
        return response.json({"error": "channel not found"})
    
    channel = await server.ctx.channels.find_one({
        "message-tag": data["channel"]
    })

    if channel["scope"] == "personal":
        return
    elif channel["scope"] == "public":
        return

    if user not in channel["attrs"]["members"]:
        return response.json({"error": "channel not found"})

