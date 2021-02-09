from typing import Dict, Type
import logging
import argparse
from abc import abstractmethod
from importlib import import_module
from pymdmix_core.settings import SETTINGS
from pymdmix_core.parser import MDMIX_PARSER


logger = logging.getLogger(__name__)


class Plugin:

    NAME: str = "plugin"
    HELP_STRING: str = "plugin help"
    LOAD_CONFIG: bool = False
    CONFIG_FILE: str = "pymdmix_core.yml"

    def __init__(self) -> None:
        self.load_config()
        pass

    def add_subparser(self, parser: argparse.ArgumentParser):
        subparser = parser.add_subparsers(dest='plugin')
        parser = subparser.add_parser(self.NAME)
        self.init_parser(parser)

    def init_parser(self, parser: argparse.ArgumentParser) -> None:
        """
        configure here options for the plugin parser, passed as parameter
        """
        pass

    @abstractmethod
    def run(self, parameters: argparse.Namespace) -> None:
        pass

    def load_config(self) -> None:
        if self.LOAD_CONFIG:
            SETTINGS.update_settings_with_file(SETTINGS.get_defaults_filename(self.CONFIG_FILE))


class PluginManager:

    def __init__(self) -> None:
        self.plugins: Dict[str, Plugin] = {}

    def load_plugin(self, plugin_name: str):
        mod = import_module(plugin_name)
        plugin_class: Type[Plugin] = mod.get_plugin_class()
        self.plugins[plugin_class.NAME] = plugin_class()
        self.plugins[plugin_class.NAME].add_subparser(MDMIX_PARSER)
