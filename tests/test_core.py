from argparse import ArgumentParser
from unittest.mock import patch, Mock
import pytest

from pymdmix_core.core import ActionList, ActionLoad
from pymdmix_core.parser import MDMIX_PARSER, get_mdmix_parser, get_plugin_subparsers
from pymdmix_core.plugin.base import MDMIX_PLUGIN_MANAGER, PluginManager


@patch.object(MDMIX_PLUGIN_MANAGER, 'plugins', {"test_plugin1": None, "test_plugin2": None})
def test_list_action(capfd):
    parser = ArgumentParser()
    subparser = parser.add_subparsers(dest="action")
    action = ActionList(subparser)
    action.run(None)
    output, _ = capfd.readouterr()
    expected_output = "Available plugins:\n\t- test_plugin1\n\t- test_plugin2\n"
    assert output == expected_output


@patch("pymdmix_core.parser.MDMIX_PARSER", get_mdmix_parser())
def test_load_action():
    plugin_manager = PluginManager()
    plugin_manager.load_plugin("pymdmix_core")
    subparser = get_plugin_subparsers()
    action = ActionLoad(subparser, plugin_manager)
    args = MDMIX_PARSER.parse_args(["plugin", "load", "tests.fixture_plugin"])
    with pytest.raises(NotImplementedError):
        action.run(args)


def test_load_action_parser():
    parser = ArgumentParser()
    subparser = parser.add_subparsers(dest="action")
    action = ActionLoad(subparser)
    parser = ArgumentParser(subparser)
    action.init_parser()
    # TODO: add asserts, and or parametrize the test


def test_core_plugin():
    pass
