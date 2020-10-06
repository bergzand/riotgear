"""
riotgears plugin manager

Manages the plugins
"""

from abc import abstractmethod
import importlib.util
from importlib.util import spec_from_file_location
import inspect
import os.path

from pathlib import Path


class Registry(object):

    # Singleton instance
    _instance = None

    def __new__(cls, default_dirs=None):
        if cls._instance is None:
            cls._instance = super(Registry, cls).__new__(cls)
            self = cls._instance
            self._search_dirs = []
            if default_dirs:
                self._search_dirs = [Path(os.path.abspath(directory))
                                     for directory in default_dirs]
            self._registry = dict()
        return cls._instance

    def add_dir(self, path):
        abspath = os.path.abspath(path)
        if abspath not in self.search_dirs():
            self._search_dirs.append(abspath)

    def search_dirs(self):
        return self._search_dirs

    def load_all(self):
        for directory in self.search_dirs():
            for child in directory.iterdir():
                if child.is_dir():
                    module = Plugin.from_path(child.name, child)
                    if module:
                        self._registry[child.name] = module

    def add_to_registry(self, name, module):
        self._registry[name] = module

    def in_registry(self, name):
        return name in self._registry

    def get_registry(self):
        return self._registry

    def get_registry_items(self):
        return self._registry.items()

    def get_from_registry(self, name):
        return self._registry[name]


class Plugin(object):

    ########################
    # Plugin API specifics #
    ########################
    LOADER = "loader.py"
    ENTRY = "plugin.py"

    @classmethod
    def from_path(cls, name, directory):
        path = directory / cls.LOADER
        spec = spec_from_file_location("{}/loader".format(name), path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return cls(name, module, directory)

    def __init__(self, name, loader, directory):
        self.name = name
        self._loader_mod = loader
        self._dir = directory
        self._plugin_mod = None
        self._loader_class = None
        self._plugin_class = None
        self._plugin = None

        def is_basepluginloader(member):
            return inspect.isclass(member) and \
                   issubclass(member, BasePluginLoader) and \
                   member is not BasePluginLoader

        for name, member in inspect.getmembers(self._loader_mod,
                                               is_basepluginloader):
            self._loader_class = member

    def add_plugin_mod(self, plugin):
        self.plugin = plugin

    def call_subcommand_args(self, argparser):
        if (self._loader_class):
            self._loader_class.subcommand_args(argparser)

    def get_name(self):
        return self._loader_class.name()

    def get_subfunction(self):
        return self._loader_class.subfunction()

    def _load_plugin_module(self):
        if self._plugin_mod:
            return
        module_path = self._dir / type(self).ENTRY
        # TODO: raise exception
        assert(module_path.is_file())
        spec = spec_from_file_location("{}/plugin".format(self.name),
                                       module_path)
        self._plugin_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self._plugin_mod)

        def is_baseplugin(member):
            return inspect.isclass(member) and \
                   issubclass(member, BasePlugin) and \
                   member is not BasePlugin

        mod_class = None

        for name, member in inspect.getmembers(self._plugin_mod,
                                               is_baseplugin):
            mod_class = member

        self._plugin_mod = mod_class

    def _get_plugin_module(self):
        self._load_plugin_module()
        return self._plugin_mod

    def create_plugin(self, **kwargs):
        self._load_plugin_module()
        self._plugin = self._plugin_mod(**kwargs)

    def enter_plugin(self):
        self._plugin.entry()


class BasePluginLoader(object):
    """
    Plugin loader class object
    """

    NAME = None
    SUBFUNCTION = None

    @classmethod
    @abstractmethod
    def subcommand_args(cls, argparser):
        ...

    @classmethod
    def name(cls):
        return cls.NAME if cls.NAME else ""

    @classmethod
    def subfunction(cls):
        return cls.SUBFUNCTION if cls.SUBFUNCTION else None


class BasePlugin(object):
    """
    Plugin class object
    """

    @abstractmethod
    def __init__(self, name: str, **kwargs):
        ...

    @abstractmethod
    def entry(self):
        ...
