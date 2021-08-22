from .db import SoarDB
from .user import User
from .creation import Creation
from .board import Board


def setup(ctx):
    ctx.db = SoarDB()
