"""riotgears command line interface driver.
"""

import argparse
from riotgear.plugin import Registry


class clidriver(object):

    def __init__(self):
        self._leftover = None
        self.args = None

    def parse_partial(self):
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('--plugindir', nargs='?')
        args, leftover = parser.parse_known_args()
        return args

    def parse(self):
        parser = argparse.ArgumentParser()
        subparser = parser.add_subparsers()
        self._add_subcommands(subparser)
        args = self._leftover if self._leftover else None
        self.args = parser.parse_args(args)
        return self.args

    def _add_subcommands(self, subparser):
        registry = Registry()
        for name, plugin in registry.get_registry_items():
            sub = subparser.add_parser(plugin.get_subfunction())
            sub.set_defaults(cmd=plugin)
            plugin.call_subcommand_args(sub)

    def launch(self):
        kwargs = vars(self.args)
        plugin = kwargs['cmd']
        del kwargs['cmd']

        plugin.create_plugin(**kwargs)
        plugin.enter_plugin()
