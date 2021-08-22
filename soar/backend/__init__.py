from .auth import Auth
from .channels import Channels
from .chat import Chat


def setup(ctx, debug):
    ctx.auth = Auth(ctx, debug)
    ctx.chat = Chat(ctx, debug)
    ctx.channels = Channels(ctx, debug)
