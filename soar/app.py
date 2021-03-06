from sanic import Sanic
from soar import backend, frontend, db
from sanic_limiter import Limiter, get_remote_address


app = Sanic('Soar')

app.static('/static', './soar/static/')


@app.listener('before_server_start')
def init(sanic, loop):
    sanic.ctx.db = db.SoarDB().db
    sanic.router.reset()

    sanic.ctx.limiter = Limiter(app, global_limits=[], key_func=get_remote_address)

    backend.setup(sanic)
    frontend.setup(sanic)

    sanic.router.finalize()


app.websocket_enabled = True

app.config.WEBSOCKET_MAX_SIZE = 2 ** 20
app.config.WEBSOCKET_MAX_QUEUE = 32
app.config.WEBSOCKET_READ_LIMIT = 2 ** 16
app.config.WEBSOCKET_WRITE_LIMIT = 2 ** 16
app.config.WEBSOCKET_PING_INTERVAL = 2
app.config.WEBSOCKET_PING_TIMEOUT = 6
