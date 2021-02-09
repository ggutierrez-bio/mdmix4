from argparse import ArgumentParser
import sys


class MDMixParser(ArgumentParser):

    """
    This class inherits from ArgumentParser to override the error function
    """

    def error(self, message: str) -> None:
        self.print_help(sys.stderr)
        return super().error(message)


def get_mdmix_parser():
    parser = MDMixParser("MDMix")
    parser.add_argument(
        "-c", "--config",
        help=(
            "location of additional configuration file. "
            "if no config file is provided, all the config values will be the default ones. "
            "default is config.yml"
        ),
        default=None
    )
    parser.add_argument(
        "-v", "--verbosity",
        help="set verbosity level. default is INFO",
        default="INFO",
        choices=["INFO", "WARNING", "ERROR", "CRITICAL"]
    )
    parser.add_argument(
        "-l", "--log",
        help="send the logging output to the specified file",
        default=None
    )
    parser.add_argument(
        "plugin",
        help="name of the plugin to execute. use mdmix plugin list to get a list of available plugins"
    )
    return parser


MDMIX_PARSER = get_mdmix_parser()
