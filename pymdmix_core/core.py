from typing import Optional
from argparse import ArgumentParser
import logging
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
        plugin = self.plugin_manager.plugins[args.plugin]
        if plugin is None:
            plugin_name = args.plugin
            plugins_list = list(self.plugin_manager.plugins.keys())
            msg = f"Plugin f{plugin_name} is not in the list of available plugins: {plugins_list}"
            logger.critical(msg)
            raise KeyError(msg)

        plugin.run(args)

        if args.plugin is None:
            self.print_help()
            return


class CorePlugin(Plugin):
    NAME = "plugin"

    def __init__(self) -> None:
        super().__init__()

    def init_parser(self, parser: ArgumentParser) -> None:
        pass
