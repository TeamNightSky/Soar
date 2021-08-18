from .db import SoarDB


def setup(app):
    app.ctx.db = SoarDB()
