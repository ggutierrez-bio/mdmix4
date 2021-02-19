from argparse import ArgumentParser
import os
import shutil
import yaml
from unittest.mock import patch

from pymdmix_core.settings import SETTINGS, Settings
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
    action.run(args)
    assert len(plugin_manager.plugins) == 2


@patch("pymdmix_core.parser.MDMIX_PARSER", get_mdmix_parser())
def test_action_add_and_remove(tmpdir):
    def _get_config(filename):
        with open(filename, 'r') as input_config_file:
            return yaml.full_load(input_config_file)
        
    src_config = os.path.join("defaults", "pymdmix_core.yml")
    tmp_config = os.path.join(tmpdir, "pymdmix_core.yml")
    shutil.copyfile(src_config, tmp_config)
    mocked_settings = Settings(tmp_config)
    
    # this horrible syntax is fixed in python3.9
    # https://github.com/we-like-parsers/pegen/issues/229
    
    with \
        patch("tests.test_core.SETTINGS", mocked_settings), \
        patch("pymdmix_core.core.SETTINGS",  mocked_settings) \
    :
        assert SETTINGS.defaults_filename == tmp_config
        assert "tests.fixture_plugin" not in _get_config(tmp_config)["pymdmix_core"]["installed_plugins"]
        parser = get_mdmix_parser()
        plugin_manager = PluginManager(parser=parser)
        plugin_manager.load_plugin("pymdmix_core")
        plugin = plugin_manager.plugins["plugin"]
        
        # add the fixture plugin to installed plugins
        args = parser.parse_args(["plugin", "add", "tests.fixture_plugin"])
        plugin.run(args)
        assert "tests.fixture_plugin" in _get_config(tmp_config)["pymdmix_core"]["installed_plugins"]

        # remove the fixture plugin from installed plugins
        args = parser.parse_args(["plugin", "remove", "tests.fixture_plugin"])
        plugin.run(args)
        assert "tests.fixture_plugin" not in _get_config(tmp_config)["pymdmix_core"]["installed_plugins"]
