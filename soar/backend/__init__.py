from .auth import Auth
from .channels import Channels
from .chat import Chat


def setup(app, debug):
    Auth(app, debug)
    Chat(app, debug)
    Channels.setup(app)
