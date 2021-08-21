from .auth import Auth
from .channels import Channels
from .chat import Chat


def setup(app, debug):
    auth = Auth(app, debug)
    chat = Chat(app, debug)
    channels = Channels(app)

    modules = [auth, chat, channels]
    for module in modules:
        module.link([x for x in modules if x is not module])
