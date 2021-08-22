class Model:
    DEFAULT_DATA = {}

    def __init__(self, client, database_target=None, snowflake=None):
        self.collection = client.get_collection(database_target)
        self.data = {
            '_id': snowflake
        }
        self.data.update(self.DEFAULT_DATA)

    @property
    def _id(self):
        return self.data.get('_id', None)

    async def save(self):
        if not self._id:
            await self.collection.insert(self.data)
        else:
            await self.collection.update(
                {"_id": self._id},
                self.data
            )
        del self.data
        self.data = {"_id": self._id}

    async def reload(self):
        if self._id:
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
