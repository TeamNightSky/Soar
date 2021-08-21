
class BackendClass:
    def __init__(self, app, debug=False):
        self.debug = debug
        if self.debug:
            print(f"Initiating {self.__class__.__name__} backend class.")
        self.app = app
        self.db = app.ctx.db.db
        self.modules = {}

    def link(self, modules):
        self.modules = {}
        for module in modules:
            self.modules[module.__class__.__name__] = module
        if self.debug:
            print(f"{self.__class__.__name__} has been linked to {len(modules)} other backend classes.")


class Error(Exception):
    def __init__(self, message, location):
        self.message = message
        self.location = location
        super().__init__(self.message)
