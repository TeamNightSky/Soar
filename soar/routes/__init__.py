from .auth import Auth
from .channels import Channels
from .chat import Chat
from .middleware import Middleware
from . import frontend


def setup(app):
    Middleware.setup(app)

    Auth.setup(app)
    Chat.setup(app)
    Channels.setup(app)
    frontend.setup(app)
