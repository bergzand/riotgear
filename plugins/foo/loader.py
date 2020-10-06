from riotgear.plugin import BasePluginLoader


class FooLoader(BasePluginLoader):
    NAME = "Foo"
    SUBFUNCTION = "foo"

    @classmethod
    def subcommand_args(cls, argparser):
        argparser.add_argument('--foo')
