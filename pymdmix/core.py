from typing import List, Optional
from pymdmix.plugin import PluginManager
from pymdmix.settings import SETTINGS


class MDMix:

    def __init__(self, config: Optional[str] = None) -> None:
        if config is not None:
            SETTINGS.update_settings_with_file(config)

        self.plugin_manager = PluginManager()
        for plugin in SETTINGS["mdmix"]["installed_plugins"]:
            self.plugin_manager.load_plugin(plugin)
    
    def run(self, plugin_name: str, parameters: List[str]):
        plugin = self.plugin_manager.plugins[plugin_name]
        plugin.run(parameters)