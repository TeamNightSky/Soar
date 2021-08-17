from sanic import Sanic
from .db import SoarDB
from .api import Auth, Channels, Chat

app = Sanic("Soar")

app.static('/static', './soar/static/')


@app.listener('before_server_start')
def init(sanic, loop):
    sanic.ctx.db = SoarDB()

    Auth.setup(sanic)
    Chat.setup(sanic)
    Channels.setup(sanic)


app.websocket_enabled = True

app.config.WEBSOCKET_MAX_SIZE = 2 ** 20
app.config.WEBSOCKET_MAX_QUEUE = 32
app.config.WEBSOCKET_READ_LIMIT = 2 ** 16
app.config.WEBSOCKET_WRITE_LIMIT = 2 ** 16
app.config.WEBSOCKET_PING_INTERVAL = 2
app.config.WEBSOCKET_PING_TIMEOUT = 6

