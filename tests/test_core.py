from argparse import ArgumentParser
from unittest.mock import patch
import pytest

from pymdmix_core.core import ListAction, LoadAction
from pymdmix_core.plugin.base import MDMIX_PLUGIN_MANAGER


@patch.object(MDMIX_PLUGIN_MANAGER, 'plugins', {"test_plugin1": None, "test_plugin2": None})
def test_list_action(capfd):
    parser = ArgumentParser()
    subparser = parser.add_subparsers(dest="action")
    action = ListAction(subparser)
    action.run(None)
    output, _ = capfd.readouterr()
    expected_output = "Available plugins:\n\t- test_plugin1\n\t- test_plugin2\n"
    assert output == expected_output


def test_load_action():
    parser = ArgumentParser()
    subparser = parser.add_subparsers(dest="action")
    action = LoadAction(subparser)
    with pytest.raises(NotImplementedError):
        action.run(None)


def test_load_action_parser():
    parser = ArgumentParser()
    subparser = parser.add_subparsers(dest="action")
    action = LoadAction(subparser)
    parser = ArgumentParser(subparser)
    action.init_parser()
    # TODO: add asserts, and or parametrize the test


def test_core_plugin():
    pass
