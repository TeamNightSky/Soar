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

    async def reload(self):
        if self._id:
            new_data = await self.client[self.target].find_one({"_id": self._id})
            self.data.update(new_data)

    async def remove(self):
        if self._id:
            await self.client[self.target].remove({"_id": self._id})
            await self.client[self.target].clear()

    async def exists(self):
        # TODO: Write out if an entry is in self.client[self.target]
        pass

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
    def __init__(self, client, stuff, foo, bar):
        snowflake = get_snowflake(stuff, foo, bar)
        super().__init__(client, 'users', snowflake)

    async def setup(self):
        if not await self.exists():
            self.data.update({
                'name': None,

            })
            await self.save()
        else:
            await self.reload()


class Creation(Model):
    pass


class Board(Model):
    pass


class Message:
    # I hesitate to write this class because messages aren't stored in their own database.
    # They are stored inside boards meaning that self.target probably wouldn't work
    # Subclass maybe?
    pass
