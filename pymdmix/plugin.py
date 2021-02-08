from typing import Dict, List, Type
from abc import abstractmethod
from importlib import import_module

class Plugin:

    NAME: str = "Plugin"

    def __init__(self) -> None:
        self.cosa = "cosa"
        pass

    @abstractmethod
    def run(self, parameters: List[str]) -> None:
        pass


class PluginManager:

    def __init__(self) -> None:
        self.plugins: Dict[str, Plugin] = {}

        
    def load_plugin(self, plugin_name: str):
        mod = import_module(plugin_name)
        plugin_class: Type[Plugin] = mod.get_plugin_class()
        self.plugins[plugin_class.NAME] =  plugin_class()