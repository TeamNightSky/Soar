from .model import Model
from ..snowflakes import creation_snowflake


class Creation(Model):
    DEFAULT_DATA = {
        "title": "",
        "scope": "",
        "owner": None,
        "messages": [],
        "created-at": None
    }

    def __init__(self, client, title, author, time):
        snowflake = creation_snowflake(title, author, time)
        super().__init__(client, "creations", snowflake)
