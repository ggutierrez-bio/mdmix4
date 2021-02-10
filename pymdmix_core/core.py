from pymdmix_core.plugin.base import PluginAction
from typing import Optional
from argparse import ArgumentParser, Namespace
import logging
import sys
from pymdmix_core.plugin import Plugin
from pymdmix_core.settings import SETTINGS
from pymdmix_core.parser import MDMIX_PARSER
from pymdmix_core.plugin.base import MDMIX_PLUGIN_MANAGER

logger = logging.getLogger(__name__)


class MDMix:

    def __init__(self, config: Optional[str] = None) -> None:
        if config is not None:
            SETTINGS.update_settings_with_file(config)

        self.plugin_manager = MDMIX_PLUGIN_MANAGER
        for plugin in SETTINGS["mdmix_core"]["installed_plugins"]:
            logger.info(f"loading plugin: {plugin}")
            self.plugin_manager.load_plugin(plugin)

    def run(self) -> None:
        args = MDMIX_PARSER.parse_args()
        plugin = self.plugin_manager.plugins.get(args.plugin)
        if plugin is None:
            plugin_name = args.plugin
            plugins_list = list(self.plugin_manager.plugins.keys())
            msg = f"Plugin f{plugin_name} is not in the list of available plugins: {plugins_list}"
            logger.critical(msg)
            MDMIX_PARSER.print_help(sys.stderr)
            raise KeyError(msg)

        plugin.run(args)

        if args.plugin is None:
            self.print_help()
            return


class ListAction(PluginAction):

    ACTION_NAME = "list"

    def init_parser(self, parser: ArgumentParser):
        pass

    def run(self, args: Namespace) -> None:
        print("Available plugins:")
        for plugin_name in MDMIX_PLUGIN_MANAGER.plugins:
            print(f"\t- {plugin_name}")


class LoadAction(PluginAction):

    ACTION_NAME = "load"

    def init_parser(self, parser: ArgumentParser):
        parser.add_argument("plugin_module")

    def run(self, args: Namespace) -> None:
        raise NotImplementedError("This feature is not implemented _yet_")


class CorePlugin(Plugin):

    NAME = "plugin"

    def __init__(self) -> None:
        super().__init__()
        self.register_action(ListAction())
        self.register_action(LoadAction())
