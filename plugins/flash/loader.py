from riotgear.plugin import BasePluginLoader


class FlasherLoader(BasePluginLoader):
    NAME = "flasher"
    SUBFUNCTION = "flash"

    @classmethod
    def subcommand_args(cls, argparser):
        argparser.add_argument('--board')
        argparser.add_argument('--example')
