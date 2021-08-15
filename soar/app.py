from sanic import Sanic
import os
import importlib
import db


app = Sanic("Soar")

app.static('/static', './soar/static/')

@app.listener('before_server_start')
def init(sanic, loop):
    db.init()

    app.ctx.dbclient = db.client
    app.ctx.db = db.db

    app.ctx.users = db.users
    app.ctx.channels = db.channels
    app.ctx.messages = db.messages


app.websocket_enabled = True

app.config.WEBSOCKET_MAX_SIZE = 2 ** 20
app.config.WEBSOCKET_MAX_QUEUE = 32
app.config.WEBSOCKET_READ_LIMIT = 2 ** 16
app.config.WEBSOCKET_WRITE_LIMIT = 2 ** 16
app.config.WEBSOCKET_PING_INTERVAL = 2
app.config.WEBSOCKET_PING_TIMEOUT = 6


extensions = [
    'api.auth',
    'api.chat',
    'api.channels',
    'frontend.frontend'
]

for pkg in extensions:
    module = importlib.import_module(pkg)
    module.setup(app)


ssl = {"cert": "certificate.crt", "key": "private.key"}


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        #ssl=ssl,  (replit doesnt support ssl)
        workers=11  # Cranking it up to 11  ;)
    )

