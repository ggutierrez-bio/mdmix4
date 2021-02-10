import logging
from argparse import Namespace, ArgumentParser
from pymdmix_core.plugin.base import PluginAction
from typing import Callable, Type
from pymdmix_core.orm import BaseModel

from pymdmix_core.plugin import Plugin

logger = logging.getLogger(__name__)


class CreateAction(PluginAction):

    def __init__(self, factory: Callable[[Namespace], BaseModel]) -> None:
        super().__init__()
        self.factory = factory

    def run(self, args: Namespace) -> None:
        self.factory(args)


class ReadAction(PluginAction):
    pass


class UpdateAction(PluginAction):
    pass


class DeleteAction(PluginAction):
    pass


class ListAction(PluginAction):
    pass


class CRUDPlugin(Plugin):

    NAME = "crud_plugin"
    CLASS: Type[BaseModel] = BaseModel

    FACTORY: Callable[[Namespace], CLASS] = None

    def __init__(self) -> None:
        super().__init__()
        self.register_action(CreateAction(self.FACTORY))
        self.register_action(ReadAction())
        self.register_action(UpdateAction())
        self.register_action(DeleteAction())
        self.register_action(ListAction())

    def init_parser(self, parser: ArgumentParser) -> None:
        super().init_parser(parser)
