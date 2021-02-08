from pymdmix.plugin import PluginManager

def test_plugin_manager_load_plugin():
    plugin_manager = PluginManager()
    plugin_manager.load_plugin("pymdmix.plugins.project")
    
    assert "project" in plugin_manager.plugins
    assert plugin_manager.plugins["project"].cosa == "cosa"