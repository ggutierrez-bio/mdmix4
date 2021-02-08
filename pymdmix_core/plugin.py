from typing import Dict, List, Type
from abc import abstractmethod
from importlib import import_module
from pymdmix_core.settings import SETTINGS


class Plugin:

    NAME: str = "plugin"
    LOAD_CONFIG: bool = True
    CONFIG_FILE: str = "pymdmix_core.yml"

    def __init__(self) -> None:
        self.load_config()
        pass

    @abstractmethod
    def run(self, parameters: List[str]) -> None:
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
