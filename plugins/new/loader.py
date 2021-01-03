from riotgear.plugin import BasePluginLoader


class NewLoader(BasePluginLoader):
    NAME = "new-application"
    SUBFUNCTION = "new"

    @classmethod
    def subcommand_args(cls, argparser):
        argparser.add_argument('application', help='the application name')
        argparser.add_argument('-b', '--board', required=False, help='the board to use for the application. (default: `native`)')
        argparser.add_argument('-r', '--riotbase', required=False, help='abosulte path to the RIOT base directory. (default: `$(CURDIR)/../RIOT`)')
