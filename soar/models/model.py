class Model:
    DEFAULT_DATA = {}

    def __init__(self, client, database_target=None, snowflake=None):
        self.collection = client.get_collection(database_target)
        self._id = snowflake

        self.data = {
            "_id": self._id
        }

        self.data.update(self.DEFAULT_DATA)

    async def save(self):
        if not self._id:
            await self.collection.insert(self.data)
        else:
            await self.collection.update(
                {"_id": self._id},
                self.data
            )

    async def reload(self):
        if self._id and await self.exists():
            new_data = await self.collection.find_one({"_id": self._id})
            self.data.update(new_data)

    async def remove(self):
        if self._id:
            await self.collection.remove({"_id": self._id})
            await self.collection.clear()

    async def exists(self):
        if self._id:
            count = await self.collection.count_documents({"_id": self._id})
            return bool(count)

    async def __aenter__(self):
        await self.reload()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        del self.data
        self.data = {'_id': self._id}
