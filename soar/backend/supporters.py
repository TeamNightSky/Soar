
class BackendClass:
    def __init__(self, ctx, debug=False):
        self.debug = debug
        if self.debug:
            print(f"Initiating backend:{self.__class__.__name__}")

        self.ctx = ctx
        self.db = ctx.db.db


class Error(Exception):
    def __init__(self, message, location):
        self.message = message
        self.location = location
        super().__init__(self.message)
