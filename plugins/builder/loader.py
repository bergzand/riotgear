from riotgear.plugin import BasePluginLoader


class FooLoader(BasePluginLoader):
    NAME = "Build"
    SUBFUNCTION = "build"

    @classmethod
    def subcommand_args(cls, argparser):
        # Boards, tree, etc.
        argparser.add_argument('board')
        argparser.add_argument('application')
        argparser.add_argument('-j', '--jobs', nargs='?', default=1)
        argparser.add_argument('-D', '--docker', action='store_true')
