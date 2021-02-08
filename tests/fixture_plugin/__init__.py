from pymdmix_core.plugin import Plugin


class FixturePlugin(Plugin):

    NAME = "fixtureplugin"

    def run(self, parameters) -> None:
        pass


def get_plugin_class():
    return FixturePlugin
