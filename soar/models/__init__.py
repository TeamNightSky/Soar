from .db import SoarDB
from .model import User, Creation, Board


def setup(app):
    app.ctx.db = SoarDB()
