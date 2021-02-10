from typing import Dict, Type
import logging
from argparse import ArgumentParser, Namespace
from abc import abstractmethod
from importlib import import_module
from pymdmix_core.settings import SETTINGS
from pymdmix_core.parser import MDMIX_PARSER, get_plugin_subparsers


logger = logging.getLogger(__name__)


class PluginAction:

    ACTION_NAME: str = "action"

    @abstractmethod
    def run(self, args: Namespace) -> None:
        pass

    def init_parser(self, parser: ArgumentParser):
        pass


class Plugin:

    NAME: str = "plugin"
    HELP_STRING: str = "plugin help"
    LOAD_CONFIG: bool = False
    CONFIG_FILE: str = "pymdmix_core.yml"

    def init_parser(self) -> None:
        """
        override this method to configure options for the plugin parser other than actions parsers.
        plugin parser passed as parameter.
        """
        pass

    def __init__(self) -> None:
        self.load_config()
        self.actions: Dict[str, PluginAction] = {}
        self.parser = None
        self.subparser = None

    def register_action(self, action: PluginAction):
        self.actions[action.ACTION_NAME] = action

    def add_subparser(self, parser: ArgumentParser):
        subparser = get_plugin_subparsers(parser)
        self.parser = subparser.add_parser(self.NAME)
        self.add_actions_parsers()
        self.init_parser()

    def add_actions_parsers(self):
        self.subparser = self.parser.add_subparsers(dest="action")
        for action in self.actions.values():
            parser = self.subparser.add_parser(action.ACTION_NAME)
            action.init_parser(parser)

    def run(self, args: Namespace) -> None:
        action = self.actions.get(args.action)
        if action is not None:
            action.run(args)

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


MDMIX_PLUGIN_MANAGER = PluginManager()
