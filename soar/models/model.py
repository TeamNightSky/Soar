import hashlib
from ..snowflakes import user_snowflake


class Model:
    def __init__(self, client, database_target=None, snowflake=None):
        self.client = client
        self.target = database_target
        self.data = {
            '_id': snowflake
        }

    @property
    def _id(self):
        return self.data.get('_id', None)

    async def save(self):
        if not self._id:
            await self.client[self.target].insert(self.data)
        else:
            await self.client[self.target].update(
                {"_id": self._id},
                self.data
            )
        self.data = {"_id": self._id}

    async def reload(self):
        if self._id:
            new_data = await self.client[self.target].find_one({"_id": self._id})
            self.data.update(new_data)

    async def remove(self):
        if self._id:
            await self.client[self.target].remove({"_id": self._id})
            await self.client[self.target].clear()

    async def exists(self):
        if self._id:
            count = await self.client[self.target].count_documents({"_id": self._id})
            return bool(count)


"""yaml
users:
    - name: <str>
        creations:
            - <creation>
        friends:
            - <user2>
      id: <snowflake>
        logins:
            - date: <datetime>
        context:
            ip: <str>
            user-agent: <str>
boards:
    - title: <str>
      scope: <scope>
      owner: <user>
      messages:
            - snowflake: <snowflake>
              created-at: <datetime>
              contents: <str>
              author: <user>
              editted-at: <datetime>
              board-id: <snowflake>
      _id: <snowflake>
      created-at: <datetime>

creations:
    - title: <str>
      author: <user>
      attachments:
            - <file-cdn-link>
      _id: <snowflake>
      created-at: <datetime>
"""


class User(Model):
    # Subject to change
    def __init__(self, client, username, password, time):
        snowflake = user_snowflake(username, time)
        self.username, self.password, self.time = username, password, time
        super().__init__(client, 'users', snowflake)

    async def setup(self):
        if not await self.exists():
            self.data.update({
                "username": self.username,
                "password": hashlib.sha256(self.password.encode("utf-8")).hexdigest(),
                "created-at": self.time,
                "friends": [],
                "friend-reqs": [],  # Inbound
                "logins": []
            })
            await self.save()
        else:
            await self.reload()


class Creation(Model):
    pass


class Board(Model):
    async def add_message(self, channel_tag, user, content, time):
        json = {
            "channel-tag": channel_tag,
            "sender": user,
            "timestamp": time,
            "content": content
        }
        await self.client[self.target]["messages"].insert_one({**json})
        return json

