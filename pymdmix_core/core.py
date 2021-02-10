from typing import Callable, Dict, Optional
from argparse import ArgumentParser, Namespace
import logging
import sys
from pymdmix_core.plugin import PluginManager, Plugin
from pymdmix_core.settings import SETTINGS
from pymdmix_core.parser import MDMIX_PARSER


logger = logging.getLogger(__name__)


class MDMix:

    def __init__(self, config: Optional[str] = None) -> None:
        if config is not None:
            SETTINGS.update_settings_with_file(config)

        self.plugin_manager = PluginManager()
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


class CorePlugin(Plugin):
    NAME = "core"

    def __init__(self) -> None:
        super().__init__()
        self.actions: Dict[str, Callable] = {
            "load": self.load,
            "show": self.show
        }

    def init_parser(self, parser: ArgumentParser) -> None:
        subparser = parser.add_subparsers(dest="core_action")
        # show_parser = subparser.add_parser("show")
        subparser.add_parser("show")
        load_parser = subparser.add_parser("load")
        load_parser.add_argument("package")

    def run(self, parameters: Namespace):
        self.actions[parameters.core_action](parameters)

    def load(self, parameters: Namespace):
        # TODO
        raise NotImplementedError("This feature is not implemented _yet_")

    def show(self, _: Namespace):
        # TODO
        print(SETTINGS["mdmix_core"]["installed_plugins"])
