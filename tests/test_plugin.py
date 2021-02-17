from pymdmix_core.plugin.base import Plugin, PluginAction
from pymdmix_core.plugin import PluginManager
from pymdmix_core.parser import get_mdmix_parser


class Action1(PluginAction):

    ACTION_NAME = "action1"


class PluginFixture(Plugin):

    NAME: str = "test"
    HELP_STRING: str = "plugin help"
    LOAD_CONFIG: bool = False
    CONFIG_FILE: str = "pymdmix_core.yml"

    def init_parser(self) -> None:
        self.parser.add_argument("--foo", "-f", default=3)


def test_plugin_manager_load_plugin():
    plugin_manager = PluginManager()
    plugin_manager.load_plugin("tests.fixture_plugin")

    assert "fixtureplugin" in plugin_manager.plugins


def test_plugin():
    # define una clase plugin y una clase accion
    # crea un mdmix parser
    parser = get_mdmix_parser()
    _ = PluginFixture(parser)
    # TODO:
    #   * add asserts
    #   * make the plugin do something
