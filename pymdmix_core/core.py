from typing import List, Optional
import logging
from pymdmix_core.plugin import PluginManager
from pymdmix_core.settings import SETTINGS


logger = logging.getLogger(__name__)


class MDMix:

    def __init__(self, config: Optional[str] = None) -> None:
        if config is not None:
            SETTINGS.update_settings_with_file(config)

        self.plugin_manager = PluginManager()
        for plugin in SETTINGS["mdmix_core"]["installed_plugins"]:
            logger.info(f"loading plugin: {plugin}")
            self.plugin_manager.load_plugin(plugin)

    def run(self, plugin_name: str, parameters: List[str]):
        plugin = self.plugin_manager.plugins[plugin_name]
        plugin.run(parameters)
