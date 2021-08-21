import hashlib
import datetime

from .supporters import BackendClass, Error


class Auth(BackendClass):
    async def register(self, username, password):
        users = self.db["users"]

        count = await users.count_documents({"username": username})

        if count > 0:
            raise Error("Username taken", "Auth/register")

        await users.insert_one({
            "username": username,
            "password": hashlib.sha256(password.encode("utf-8")).hexdigest(),
            "created-at": datetime.datetime.now(),
            "friends": [],
            "friend-reqs": []
        })

        return {"un": username}

    async def login(self, username, password):
        users = self.db["users"]

        dig = hashlib.sha256(password.encode("utf-8")).hexdigest()
        if dig != (await users.find_one({"username": username}))["password"]:
            raise Error("incorrect username and/or password", "Auth/login")

        return {"un": username}
