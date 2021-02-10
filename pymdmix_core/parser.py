from argparse import ArgumentParser, _SubParsersAction


def get_mdmix_parser():
    parser = ArgumentParser("MDMix")
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

    return parser


MDMIX_PARSER = get_mdmix_parser()


def get_mdmix_subparsers():
    parser = MDMIX_PARSER
    actions = parser._subparsers._actions if parser._subparsers is not None else []
    return next(
        iter(
            [action for action in actions if isinstance(action, _SubParsersAction)],
        ),
        parser.add_subparsers(title="plugin", dest="plugin")
    )
