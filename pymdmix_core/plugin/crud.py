import logging
from argparse import Namespace, ArgumentParser
from typing import Type
from pymdmix_core.orm import BaseModel

from pymdmix_core.plugin import Plugin

logger = logging.getLogger(__name__)


class CRUDPlugin(Plugin):

    NAME = "crud_plugin"
    CLASS: Type[BaseModel] = BaseModel

    def __init__(self) -> None:
        super().__init__()

    def run(self, args: Namespace):
        pass

    def init_parser(self, parser: ArgumentParser) -> None:
        super().init_parser(parser)
