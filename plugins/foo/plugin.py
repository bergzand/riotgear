from riotgear.plugin import BasePlugin


class FooPlugin(BasePlugin):

    def __init__(self, foo):
        self.foo = foo

    def entry(self):
        print("FOOO: {}".format(self.foo))
